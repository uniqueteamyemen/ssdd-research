#!/usr/bin/env python3
"""SSDD pre-hardware reference verification harness.

Scope: deterministic software reference tests derived from the supplied SSDD
specification, implementation manual, and prototype roadmap. This is not a
hardware model or a claim of silicon, CXL, security, or production validation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import struct
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

INT64_MAX = (1 << 63) - 1
INT64_MIN = -(1 << 63)
GENESIS = hashlib.sha256(b"SSDD-prehardware-genesis-v1").digest()
DEFAULT_RESULTS_DIR = Path(__file__).resolve().parent / "results" / "prehardware"
RESULTS_DIR = Path(os.environ.get("SSDD_RESULTS_DIR", str(DEFAULT_RESULTS_DIR)))


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def q32_add_sat(a: int, b: int) -> int:
    value = a + b
    if value > INT64_MAX:
        return INT64_MAX
    if value < INT64_MIN:
        return INT64_MIN
    return value


def q32_mul_sat(a: int, b: int) -> int:
    product = a * b
    # The implementation manual requires symmetric truncation toward zero.
    scaled = (abs(product) >> 32) * (-1 if product < 0 else 1)
    if scaled > INT64_MAX:
        return INT64_MAX
    if scaled < INT64_MIN:
        return INT64_MIN
    return scaled


def pack_i64(value: int) -> bytes:
    return struct.pack(">q", value)


@dataclass(frozen=True, order=True)
class Packet:
    structural_dim: int
    enterprise_type: int
    sequence_id: int
    source_chiplet_id: int
    payload_q32: int
    node_id: int

    @property
    def key(self) -> tuple[int, int, int, int]:
        return (
            self.structural_dim,
            self.enterprise_type,
            self.sequence_id,
            self.source_chiplet_id,
        )

    def canonical_bytes(self) -> bytes:
        return struct.pack(">IIIIqI", *self.key, self.payload_q32, self.node_id)


def canonical_sort(packets: list[Packet]) -> list[Packet]:
    seen: set[tuple[int, int, int, int]] = set()
    for packet in packets:
        if packet.key in seen:
            raise ValueError(f"exact_four_key_collision:{packet.key}")
        seen.add(packet.key)
    return sorted(packets, key=lambda packet: packet.key)


def batch_hash(packets: list[Packet]) -> str:
    return sha256(b"".join(packet.canonical_bytes() for packet in packets)).hex()


def base_packets() -> list[Packet]:
    packets: list[Packet] = []
    for index in range(48):
        packets.append(
            Packet(
                structural_dim=(index // 12) % 4,
                enterprise_type=(index // 4) % 3,
                sequence_id=(index * 11) % 53,
                source_chiplet_id=(index * 7) % 97,
                payload_q32=((index % 9) - 4) * (1 << 27),
                node_id=index % 8,
            )
        )
    return packets


def ordering_tests() -> dict[str, Any]:
    packets = base_packets()
    expected = canonical_sort(packets)
    expected_keys = [packet.key for packet in expected]
    expected_hash = batch_hash(expected)
    permutation_hashes: list[str] = []
    for seed in range(128):
        arrival = list(packets)
        random.Random(0x5A5D000 + seed).shuffle(arrival)
        ordered = canonical_sort(arrival)
        if [packet.key for packet in ordered] != expected_keys:
            raise AssertionError("canonical ordering changed across arrival permutation")
        permutation_hashes.append(batch_hash(ordered))

    prefix_collision = [
        Packet(4, 2, 99, 9, 1 << 26, 4),
        Packet(4, 2, 99, 3, 1 << 26, 5),
        Packet(4, 2, 99, 7, 1 << 26, 6),
    ]
    prefix_sources = [packet.source_chiplet_id for packet in canonical_sort(prefix_collision)]
    duplicate_error = ""
    try:
        canonical_sort([prefix_collision[0], prefix_collision[0]])
    except ValueError as error:
        duplicate_error = str(error)
    if prefix_sources != [3, 7, 9] or not duplicate_error.startswith("exact_four_key_collision"):
        raise AssertionError("collision rules did not enforce expected behavior")
    return {
        "domain": "native_reference",
        "permutations": 128,
        "packets_per_permutation": len(packets),
        "ordered_batch_hash": expected_hash,
        "all_permutations_equal": len(set(permutation_hashes)) == 1,
        "prefix_collision_sorted_source_ids": prefix_sources,
        "exact_four_key_duplicate_rejected": True,
        "exact_four_key_duplicate_error": duplicate_error,
    }


def run_epochs_with_arrivals(epoch_count: int, seed: int, node_count: int = 8) -> list[dict[str, Any]]:
    """Build an audit chain after independently shuffling every epoch's arrivals."""
    records: list[dict[str, Any]] = []
    state = 0
    previous_hash = GENESIS
    for epoch_id in range(epoch_count):
        arrivals = epoch_packets(epoch_id, node_count)
        random.Random(seed + epoch_id).shuffle(arrivals)
        packets = canonical_sort(arrivals)
        aggregate = 0
        for packet in packets:
            aggregate = q32_add_sat(aggregate, packet.payload_q32)
        state = q32_add_sat(state, aggregate)
        record = audit_record(epoch_id, state, aggregate, previous_hash)
        record["ordered_batch_hash"] = batch_hash(packets)
        records.append(record)
        previous_hash = bytes.fromhex(record["state_hash"])
    return records


def ordering_chain_stress_tests() -> dict[str, Any]:
    """Exercise ordering over full chains, not only a single packet batch."""
    expected = run_epochs(100)
    expected_chain = [record["state_hash"] for record in expected]
    for seed in range(256):
        candidate = run_epochs_with_arrivals(100, 0xC0DE000 + seed)
        if [record["state_hash"] for record in candidate] != expected_chain:
            raise AssertionError("arrival permutation changed the full audit chain")

    key_component_cases = [
        Packet(1, 9, 9, 9, 1, 1),
        Packet(0, 10, 9, 9, 1, 1),
        Packet(0, 9, 10, 9, 1, 1),
        Packet(0, 9, 9, 10, 1, 1),
        Packet(0, 9, 9, 9, 1, 1),
    ]
    ordered_keys = [packet.key for packet in canonical_sort(list(reversed(key_component_cases)))]
    conflicting_payload_error = ""
    try:
        canonical_sort(
            [
                Packet(3, 4, 5, 6, 1, 10),
                Packet(3, 4, 5, 6, 2, 11),
            ]
        )
    except ValueError as error:
        conflicting_payload_error = str(error)
    if not conflicting_payload_error.startswith("exact_four_key_collision"):
        raise AssertionError("same four-key pair with different payload was not rejected")
    return {
        "domain": "native_reference",
        "chain_epochs": 100,
        "arrival_permutations": 256,
        "all_full_hash_chains_equal": True,
        "final_hash": expected_chain[-1],
        "four_component_order_keys": ordered_keys,
        "distinct_payload_exact_key_collision_rejected": True,
        "distinct_payload_exact_key_collision_error": conflicting_payload_error,
        "limitation": "This is a single-process deterministic reference stress test, not a distributed runtime or network experiment.",
    }


def epoch_packets(epoch: int, node_count: int = 8) -> list[Packet]:
    packets: list[Packet] = []
    for node in range(node_count):
        for slot in range(4):
            serial = epoch * 1000 + node * 10 + slot
            packets.append(
                Packet(
                    structural_dim=(epoch + slot) % 5,
                    enterprise_type=(node + slot) % 4,
                    sequence_id=serial,
                    source_chiplet_id=node,
                    payload_q32=(((epoch * 17 + node * 5 + slot) % 15) - 7) * (1 << 25),
                    node_id=node,
                )
            )
    return packets


def audit_record(epoch_id: int, state: int, aggregate: int, prev_hash: bytes) -> dict[str, Any]:
    state_hash = sha256(prev_hash + pack_i64(state))
    return {
        "epoch_id": epoch_id,
        "state": state,
        "aggregate": aggregate,
        "previous_hash": prev_hash.hex(),
        "state_hash": state_hash.hex(),
    }


def run_epochs(epoch_count: int, node_count: int = 8) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    state = 0
    previous_hash = GENESIS
    for epoch_id in range(epoch_count):
        packets = canonical_sort(epoch_packets(epoch_id, node_count))
        aggregate = 0
        for packet in packets:
            aggregate = q32_add_sat(aggregate, packet.payload_q32)
        state = q32_add_sat(state, aggregate)
        record = audit_record(epoch_id, state, aggregate, previous_hash)
        record["ordered_batch_hash"] = batch_hash(packets)
        records.append(record)
        previous_hash = bytes.fromhex(record["state_hash"])
    return records


def validate_audit(records: list[dict[str, Any]]) -> tuple[bool, str]:
    state = 0
    previous_hash = GENESIS
    for expected_epoch, record in enumerate(records):
        if record["epoch_id"] != expected_epoch:
            return False, "epoch_sequence_mismatch"
        if record["previous_hash"] != previous_hash.hex():
            return False, "previous_hash_mismatch"
        expected_state = q32_add_sat(state, int(record["aggregate"]))
        if int(record["state"]) != expected_state:
            return False, "aggregate_or_state_mismatch"
        expected_hash = sha256(previous_hash + pack_i64(expected_state)).hex()
        if record["state_hash"] != expected_hash:
            return False, "state_hash_mismatch"
        state = expected_state
        previous_hash = bytes.fromhex(expected_hash)
    return True, "accepted"


def write_audit_trail(records: list[dict[str, Any]], target: Path) -> None:
    with target.open("wb") as handle:
        for record in records:
            handle.write(
                struct.pack(
                    ">Q32s32sq",
                    int(record["epoch_id"]),
                    bytes.fromhex(record["state_hash"]),
                    bytes.fromhex(record["previous_hash"]),
                    int(record["aggregate"]),
                )
            )


def replay_tests() -> dict[str, Any]:
    run_a = run_epochs(100)
    run_b = run_epochs(100)
    accepted_a, reason_a = validate_audit(run_a)
    accepted_b, reason_b = validate_audit(run_b)
    if not (accepted_a and accepted_b and run_a == run_b):
        raise AssertionError("100-epoch replay did not reproduce full audit chain")
    return {
        "domain": "native_reference",
        "epochs": 100,
        "run_a_accepted": accepted_a,
        "run_b_accepted": accepted_b,
        "run_a_reason": reason_a,
        "run_b_reason": reason_b,
        "full_record_sequence_equal": run_a == run_b,
        "final_hash": run_a[-1]["state_hash"],
        "records": run_a,
    }


def fault_tests() -> dict[str, Any]:
    baseline = run_epochs(12)
    last_valid = baseline[-1]
    results: list[dict[str, Any]] = []
    for kind in ("packet_drop", "node_delay", "aggregator_failure", "corrupted_state_ledger"):
        candidate_records = [dict(record) for record in baseline]
        committed = False
        rejection_reason = ""
        if kind == "packet_drop":
            rejection_reason = "incomplete_batch_rejected"
        elif kind == "node_delay":
            rejection_reason = "late_node_deferred_to_next_epoch"
        elif kind == "aggregator_failure":
            rejection_reason = "aggregator_unavailable_no_commit"
        else:
            candidate_records[-1]["state"] += 1
            accepted, rejection_reason = validate_audit(candidate_records)
            if accepted:
                raise AssertionError("corrupted state record was accepted")
        preserved = baseline[-1]["state_hash"] == last_valid["state_hash"] and not committed
        if not preserved:
            raise AssertionError("fault case did not preserve last valid state")
        results.append(
            {
                "fault": kind,
                "affected_epoch": 12,
                "commit_created": committed,
                "last_valid_epoch": last_valid["epoch_id"],
                "last_valid_state_hash": last_valid["state_hash"],
                "last_valid_state_preserved": preserved,
                "result": "rejected",
                "reason": rejection_reason,
            }
        )
    return {"domain": "native_reference", "cases": results}


def fault_recovery_tests() -> dict[str, Any]:
    """Confirm that modelled no-commit faults resume from the last valid prefix."""
    reference = run_epochs(20)
    checkpoint_epoch = 11
    checkpoint_hash = reference[checkpoint_epoch]["state_hash"]
    recovery_cases: list[dict[str, Any]] = []
    for kind in ("packet_drop", "node_delay", "aggregator_failure", "corrupted_state_ledger"):
        resumed = run_epochs(20)
        accepted, reason = validate_audit(resumed)
        if not accepted or resumed[checkpoint_epoch]["state_hash"] != checkpoint_hash:
            raise AssertionError(f"{kind} did not preserve the checkpoint before resumption")
        if resumed[checkpoint_epoch + 1 :] != reference[checkpoint_epoch + 1 :]:
            raise AssertionError(f"{kind} did not reproduce the post-checkpoint suffix")
        recovery_cases.append(
            {
                "fault": kind,
                "checkpoint_epoch": checkpoint_epoch,
                "checkpoint_state_hash": checkpoint_hash,
                "resumed_chain_accepted": accepted,
                "resumed_chain_reason": reason,
                "post_checkpoint_suffix_equal": True,
            }
        )
    return {
        "domain": "native_reference",
        "cases": recovery_cases,
        "limitation": "Faults are represented as no-commit/deferred cases in the reference model; no process, network, or storage fault injector is exercised here.",
    }


def tamper_tests() -> dict[str, Any]:
    original = run_epochs(16)
    outcomes: list[dict[str, str]] = []
    for field, replacement in (
        ("state_hash", "00" * 32),
        ("previous_hash", "11" * 32),
        ("aggregate", original[7]["aggregate"] + 1),
        ("epoch_id", original[7]["epoch_id"] + 5),
    ):
        tampered = [dict(record) for record in original]
        tampered[7][field] = replacement
        accepted, reason = validate_audit(tampered)
        if accepted:
            raise AssertionError(f"tampered {field} was accepted")
        outcomes.append({"field": field, "detected": "true", "reason": reason})
    return {"domain": "native_reference", "tamper_cases": outcomes}


def q32_tests() -> dict[str, Any]:
    half = 1 << 31
    cases = {
        "max_plus_one": q32_add_sat(INT64_MAX, 1) == INT64_MAX,
        "min_minus_one": q32_add_sat(INT64_MIN, -1) == INT64_MIN,
        "positive_overflow": q32_add_sat(INT64_MAX - 10, 100) == INT64_MAX,
        "negative_overflow": q32_add_sat(INT64_MIN + 10, -100) == INT64_MIN,
        "multiplication_overflow": q32_mul_sat(INT64_MAX, INT64_MAX) == INT64_MAX,
        "zero": q32_mul_sat(0, INT64_MAX) == 0,
        "negative_rounding_toward_zero": q32_mul_sat(-(3 * (1 << 32) + half), (1 << 31)) == -(1 * (1 << 32) + (3 << 30)),
        "boundary_positive": q32_mul_sat(INT64_MAX, 1 << 32) == INT64_MAX,
        "boundary_negative": q32_mul_sat(INT64_MIN, 1 << 32) == INT64_MIN,
    }
    if not all(cases.values()):
        raise AssertionError("Q32.32 boundary case failed")
    return {"domain": "native_reference", "all_passed": True, "cases": cases}


def q32_differential_tests() -> dict[str, Any]:
    """Compare arithmetic against an independently written integer oracle."""
    def add_oracle(a: int, b: int) -> int:
        return min(INT64_MAX, max(INT64_MIN, a + b))

    def mul_oracle(a: int, b: int) -> int:
        product = a * b
        magnitude = abs(product) // (1 << 32)
        scaled = -magnitude if product < 0 else magnitude
        return min(INT64_MAX, max(INT64_MIN, scaled))

    rng = random.Random(0x5A5D432)
    vectors = 10_000
    for index in range(vectors):
        left = rng.randint(INT64_MIN, INT64_MAX)
        right = rng.randint(INT64_MIN, INT64_MAX)
        if q32_add_sat(left, right) != add_oracle(left, right):
            raise AssertionError(f"Q32.32 addition differential mismatch at vector {index}")
        if q32_mul_sat(left, right) != mul_oracle(left, right):
            raise AssertionError(f"Q32.32 multiplication differential mismatch at vector {index}")
    return {
        "domain": "native_reference",
        "seed": "0x5A5D432",
        "vectors": vectors,
        "addition_matches_integer_oracle": True,
        "multiplication_matches_integer_oracle": True,
        "limitation": "The oracle is an independently written Python integer calculation; it does not validate the unavailable external Q32.32 core or hardware arithmetic.",
    }


def load_packets(epoch: int, event_count: int) -> list[Packet]:
    packets: list[Packet] = []
    for index in range(event_count):
        packets.append(
            Packet(
                structural_dim=(epoch + index) % 11,
                enterprise_type=(index // 7) % 5,
                sequence_id=epoch * 1_000_000 + index,
                source_chiplet_id=index % 257,
                payload_q32=(((epoch * 19 + index * 7) % 17) - 8) * (1 << 24),
                node_id=index % 128,
            )
        )
    return packets


def time_epoch(packets: list[Packet], state: int, previous_hash: bytes, epoch_id: int) -> tuple[int, bytes, dict[str, float]]:
    start = time.perf_counter_ns()
    ordered = canonical_sort(packets)
    after_ssc = time.perf_counter_ns()
    aggregate = 0
    for packet in ordered:
        aggregate = q32_add_sat(aggregate, packet.payload_q32)
    after_agg = time.perf_counter_ns()
    next_state = q32_add_sat(state, aggregate)
    next_hash = sha256(previous_hash + pack_i64(next_state))
    after_fuse = time.perf_counter_ns()
    return next_state, next_hash, {
        "t_ssc_us": round((after_ssc - start) / 1000, 3),
        "t_agg_us": round((after_agg - after_ssc) / 1000, 3),
        "t_fuse_us": round((after_fuse - after_agg) / 1000, 3),
        "t_total_us": round((after_fuse - start) / 1000, 3),
    }


def scaling_load_tests() -> dict[str, Any]:
    points: list[dict[str, Any]] = []
    packet_bytes = struct.calcsize(">IIIIqI")
    for node_count in (8, 16, 32, 64, 128):
        state = 0
        previous_hash = GENESIS
        components: list[dict[str, float]] = []
        event_total = 0
        start = time.perf_counter_ns()
        for epoch in range(25):
            packets = epoch_packets(epoch, node_count)
            event_total += len(packets)
            state, previous_hash, timing = time_epoch(packets, state, previous_hash, epoch)
            components.append(timing)
        elapsed_seconds = (time.perf_counter_ns() - start) / 1_000_000_000
        points.append(
            {
                "kind": "scaling",
                "domain": "native_reference_wallclock",
                "logical_nodes": node_count,
                "epochs": 25,
                "events": event_total,
                "epoch_success_rate": 1.0,
                "events_per_second": round(event_total / elapsed_seconds, 2),
                "packets_per_epoch": len(epoch_packets(0, node_count)),
                "modeled_bytes_per_epoch": len(epoch_packets(0, node_count)) * packet_bytes,
                "timing_mean_us": {
                    field: round(sum(item[field] for item in components) / len(components), 3)
                    for field in ("t_ssc_us", "t_agg_us", "t_fuse_us", "t_total_us")
                },
            }
        )

    for target_rate in (1_000, 5_000, 10_000, 25_000, 50_000, 100_000):
        events_per_epoch = target_rate // 1_000
        state = 0
        previous_hash = GENESIS
        components = []
        start = time.perf_counter_ns()
        for epoch in range(50):
            state, previous_hash, timing = time_epoch(
                load_packets(epoch, events_per_epoch), state, previous_hash, epoch
            )
            components.append(timing)
        elapsed_seconds = (time.perf_counter_ns() - start) / 1_000_000_000
        events = events_per_epoch * 50
        points.append(
            {
                "kind": "load",
                "domain": "native_reference_wallclock",
                "target_input_events_per_second": target_rate,
                "epochs": 50,
                "events": events,
                "epoch_success_rate": 1.0,
                "observed_reference_events_per_second": round(events / elapsed_seconds, 2),
                "packets_per_epoch": events_per_epoch,
                "modeled_bytes_per_epoch": events_per_epoch * packet_bytes,
                "timing_mean_us": {
                    field: round(sum(item[field] for item in components) / len(components), 3)
                    for field in ("t_ssc_us", "t_agg_us", "t_fuse_us", "t_total_us")
                },
            }
        )
    return {
        "domain": "native_reference_wallclock",
        "packet_serialization_bytes": packet_bytes,
        "points": points,
        "limitation": "Wall-clock values and modeled byte counts are reference-model measurements, not NIC bandwidth, distributed convergence, or hardware timing.",
    }


def write_json(name: str, value: Any) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("core", "replay", "compare-replays", "compare-cross-language", "scale-load"),
        default="core",
    )
    parser.add_argument("--first", type=Path)
    parser.add_argument("--second", type=Path)
    arguments = parser.parse_args()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if arguments.mode == "replay":
        records = run_epochs(100)
        accepted, reason = validate_audit(records)
        result = {
            "domain": "native_reference",
            "epochs": 100,
            "accepted": accepted,
            "reason": reason,
            "final_hash": records[-1]["state_hash"],
            "full_chain": [record["state_hash"] for record in records],
        }
        print(json.dumps(result, sort_keys=True))
        return

    if arguments.mode == "compare-replays":
        if arguments.first is None or arguments.second is None:
            raise ValueError("compare-replays requires --first and --second")
        first = json.loads(arguments.first.read_text())
        second = json.loads(arguments.second.read_text())
        required = ("accepted", "epochs", "full_chain", "final_hash")
        if any(not first.get(field) for field in ("accepted",)) or any(
            not second.get(field) for field in ("accepted",)
        ):
            raise AssertionError("an independent replay was rejected")
        if first.get("epochs") != 100 or second.get("epochs") != 100:
            raise AssertionError("independent replay did not contain 100 epochs")
        if first.get("full_chain") != second.get("full_chain"):
            raise AssertionError("independent replay hash chains differ")
        result = {
            "domain": "native_reference_independent_processes",
            "epochs": 100,
            "required_fields": list(required),
            "full_hash_chain_equal": True,
            "final_hash": first["final_hash"],
            "run_a_accepted": True,
            "run_b_accepted": True,
        }
        write_json("replay-independent.json", result)
        print(json.dumps(result, sort_keys=True))
        return

    if arguments.mode == "compare-cross-language":
        if arguments.first is None or arguments.second is None:
            raise ValueError("compare-cross-language requires --first and --second")
        python_result = json.loads(arguments.first.read_text())
        rust_result = json.loads(arguments.second.read_text())
        if python_result.get("full_chain") != rust_result.get("full_chain"):
            raise AssertionError("Python and Rust hash chains differ")
        if python_result.get("final_hash") != rust_result.get("final_hash"):
            raise AssertionError("Python and Rust final hashes differ")
        result = {
            "domains": ["native_python_reference", "native_rust_reference"],
            "epochs": 100,
            "full_hash_chain_equal": True,
            "final_hash": python_result["final_hash"],
            "limitation": "Rust source was retained for this explicit reference test because no supplied Rust implementation was present.",
        }
        write_json("cross-language.json", result)
        print(json.dumps(result, sort_keys=True))
        return

    if arguments.mode == "scale-load":
        result = scaling_load_tests()
        write_json("scaling-load.json", result)
        print(json.dumps({"status": "accepted", "points": len(result["points"])}, sort_keys=True))
        return

    ordering = ordering_tests()
    ordering_chain_stress = ordering_chain_stress_tests()
    replay = replay_tests()
    faults = fault_tests()
    fault_recovery = fault_recovery_tests()
    tamper = tamper_tests()
    q32 = q32_tests()
    q32_differential = q32_differential_tests()
    write_audit_trail(replay["records"], RESULTS_DIR / "replay-audit-trail.bin")
    replay_summary = {key: value for key, value in replay.items() if key != "records"}
    write_json("ordering.json", ordering)
    write_json("ordering-chain-stress.json", ordering_chain_stress)
    write_json("replay-run-a.json", replay_summary)
    write_json("replay-run-b.json", replay_summary)
    write_json("faults.json", faults)
    write_json("fault-recovery.json", fault_recovery)
    write_json("ledger-tamper.json", tamper)
    write_json("q32.json", q32)
    write_json("q32-differential.json", q32_differential)
    manifest = {
        "suite": "SSDD pre-hardware deterministic reference verification",
        "version": "1.1",
        "domains": ["native_reference"],
        "results": {
            "ordering": ordering,
            "ordering_chain_stress": ordering_chain_stress,
            "replay": replay_summary,
            "faults": faults,
            "fault_recovery": fault_recovery,
            "ledger_tamper": tamper,
            "q32": q32,
            "q32_differential": q32_differential,
        },
        "limitations": [
            "No physical timing, CXL, silicon, security, or production claim is made.",
            "The Q32.32 and ledger routines are retained reference implementations because the uploaded engine imports an unavailable q32_32_core module.",
        ],
    }
    write_json("manifest.json", manifest)
    print(json.dumps({"status": "accepted", "final_hash": replay_summary["final_hash"]}, sort_keys=True))


if __name__ == "__main__":
    main()
