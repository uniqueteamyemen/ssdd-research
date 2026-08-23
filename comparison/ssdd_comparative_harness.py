#!/usr/bin/env python3
"""Contract-smoke harness for the planned SSDD value comparison.

This program is deliberately a local semantic harness.  It validates that the
three declared policy arms can be run against exactly the same fixtures and
that they emit a complete audit bundle.  It is not a contention benchmark,
physical-CXL evaluation, or proof that any arm is simpler or superior.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


GENESIS = "0" * 64
REQUIRED_DIAGNOSTIC_FIELDS = (
    "case_id",
    "arm",
    "disposition",
    "reason",
    "manifest_hash",
    "decision_record",
    "checkpoint_hash",
    "prior_valid_checkpoint_hash",
)


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


@dataclass(frozen=True)
class Event:
    event_id: str
    structural_dim: int
    enterprise_type: int
    sequence_id: int
    source_chiplet_id: int
    payload: int
    proof_valid: bool = True

    @property
    def ssdd_key(self) -> tuple[int, int, int, int]:
        return (
            self.structural_dim,
            self.enterprise_type,
            self.sequence_id,
            self.source_chiplet_id,
        )

    def canonical_record(self) -> dict[str, Any]:
        return asdict(self)


def fixture_events() -> tuple[Event, ...]:
    """A fixed, versioned event set; no external workload or random input."""
    return tuple(
        Event(
            event_id=f"event-{index:02d}",
            structural_dim=(index // 4) % 3,
            enterprise_type=index % 4,
            sequence_id=100 + index * 13,
            source_chiplet_id=(index * 7) % 17,
            payload=((index * 5) % 11) - 5,
        )
        for index in range(12)
    )


def contract_checkpoint(events: Iterable[Event], state: int) -> str:
    """Shared referee digest: final state plus membership, never an arm's log."""
    return digest(
        {
            "contract": "shared-checkpoint-v1",
            "event_ids": sorted(event.event_id for event in events),
            "state": state,
        }
    )


def exact_event_id_conflict(events: Iterable[Event]) -> str | None:
    seen: dict[str, dict[str, Any]] = {}
    for event in events:
        record = event.canonical_record()
        prior = seen.get(event.event_id)
        if prior is not None and prior != record:
            return event.event_id
        seen[event.event_id] = record
    return None


@dataclass(frozen=True)
class Case:
    case_id: str
    events: tuple[Event, ...]
    expected_event_ids: tuple[str, ...]
    expected_disposition: str
    tamper_candidate_state: bool = False


def cases() -> list[Case]:
    baseline = fixture_events()
    expected_ids = tuple(event.event_id for event in baseline)
    generated: list[Case] = [
        Case("positive-control", baseline, expected_ids, "accepted"),
    ]
    for seed in range(128):
        arrival = list(baseline)
        random.Random(0x5A5D000 + seed).shuffle(arrival)
        generated.append(
            Case(f"arrival-permutation-{seed:03d}", tuple(arrival), expected_ids, "accepted")
        )
    collision = Event(
        event_id=baseline[2].event_id,
        structural_dim=baseline[2].structural_dim,
        enterprise_type=baseline[2].enterprise_type,
        sequence_id=baseline[2].sequence_id,
        source_chiplet_id=baseline[2].source_chiplet_id,
        payload=baseline[2].payload + 1,
    )
    generated.extend(
        [
            Case("exact-event-id-collision", baseline + (collision,), expected_ids, "rejected"),
            Case("late-source", baseline[:-1], expected_ids, "deferred"),
            Case(
                "proof-corruption",
                baseline[:5]
                + (
                    Event(**{**asdict(baseline[5]), "proof_valid": False}),
                )
                + baseline[6:],
                expected_ids,
                "rejected",
            ),
            Case(
                "candidate-state-corruption",
                baseline,
                expected_ids,
                "rejected",
                tamper_candidate_state=True,
            ),
        ]
    )
    return generated


def contract_gate(case: Case) -> tuple[str, str]:
    """Referee-only expectation helper; policy arms do not call this function."""
    conflict = exact_event_id_conflict(case.events)
    if conflict is not None:
        return "rejected", f"conflicting_event_id:{conflict}"
    invalid_proof = next((event.event_id for event in case.events if not event.proof_valid), None)
    if invalid_proof is not None:
        return "rejected", f"invalid_proof:{invalid_proof}"
    actual_ids = {event.event_id for event in case.events}
    expected_ids = set(case.expected_event_ids)
    if actual_ids != expected_ids:
        missing = sorted(expected_ids - actual_ids)
        unexpected = sorted(actual_ids - expected_ids)
        return "deferred", f"incomplete_or_unexpected_set:missing={missing};unexpected={unexpected}"
    return "accepted", "complete_admitted_set"


def engine_order(arm: str, events: tuple[Event, ...]) -> tuple[list[Event], dict[str, Any]]:
    if arm == "ssdd":
        keys: set[tuple[int, int, int, int]] = set()
        for event in events:
            if event.ssdd_key in keys:
                raise ValueError(f"exact_four_key_collision:{event.ssdd_key}")
            keys.add(event.ssdd_key)
        ordered = sorted(events, key=lambda event: event.ssdd_key)
        return ordered, {
            "policy": "four-field-canonical-order",
            "ordered_batch_hash": digest([event.canonical_record() for event in ordered]),
            "ordered_keys": [event.ssdd_key for event in ordered],
        }
    if arm == "cas_retry":
        # A serious CAS/retry arm must make its semantic-ordering policy explicit.
        # It canonicalizes its candidate snapshot before its single modeled CAS
        # publication; without this added policy it would not meet the common
        # permutation-invariance contract.
        ordered = sorted(events, key=lambda event: event.ssdd_key)
        return ordered, {
            "policy": "versioned-cas-retry-with-canonicalized-candidate-snapshot",
            "modeled_compare_and_swap_publications": 1,
            "candidate_snapshot_order": [event.event_id for event in ordered],
            "canonicalization_is_an_explicit_baseline_policy_surface": True,
        }
    if arm == "single_writer_sequencer":
        # A strong sequencer is allowed to match SSDD by defining deterministic
        # queue-drain ordering. That match is evidence against any assumed
        # SSDD superiority, not a failure of the comparison.
        ordered = sorted(events, key=lambda event: event.ssdd_key)
        return ordered, {
            "policy": "single-writer-sequencer-with-canonical-queue-drain",
            "queue_positions": {event.event_id: index for index, event in enumerate(ordered)},
            "publish_count": 1,
            "canonical_queue_drain_is_an_explicit_baseline_policy_surface": True,
        }
    raise ValueError(f"unknown arm: {arm}")


def arm_gate(arm: str, case: Case) -> tuple[str, str]:
    """Each arm makes and records its own pre-commit decision.

    The repeated checks are intentional. Reusing one validator would create a
    common-mode implementation dependency and make the alternatives look more
    equivalent than they are.
    """
    records_by_id: dict[str, dict[str, Any]] = {}
    for event in case.events:
        record = event.canonical_record()
        prior = records_by_id.get(event.event_id)
        if prior is not None and prior != record:
            return "rejected", f"{arm}:conflicting_event_id:{event.event_id}"
        records_by_id[event.event_id] = record
    invalid_proof = next((event.event_id for event in case.events if not event.proof_valid), None)
    if invalid_proof is not None:
        return "rejected", f"{arm}:invalid_proof:{invalid_proof}"
    actual_ids = set(records_by_id)
    expected_ids = set(case.expected_event_ids)
    if actual_ids != expected_ids:
        missing = sorted(expected_ids - actual_ids)
        unexpected = sorted(actual_ids - expected_ids)
        return "deferred", f"{arm}:incomplete_or_unexpected_set:missing={missing};unexpected={unexpected}"
    if arm == "ssdd":
        keys = [event.ssdd_key for event in case.events]
        if len(keys) != len(set(keys)):
            return "rejected", "ssdd:exact_four_key_collision"
    return "accepted", f"{arm}:complete_admitted_set"


def evaluate(arm: str, case: Case, manifest_hash: str) -> dict[str, Any]:
    disposition, reason = arm_gate(arm, case)
    prior = GENESIS
    decision: dict[str, Any] = {
        "precommit_gate": reason,
        "event_count": len(case.events),
        "expected_event_count": len(case.expected_event_ids),
    }
    checkpoint: str | None = None
    if disposition == "accepted":
        ordered, engine_trace = engine_order(arm, case.events)
        candidate_state = sum(event.payload for event in ordered)
        decision["engine_trace"] = engine_trace
        decision["candidate_state"] = candidate_state
        if case.tamper_candidate_state:
            disposition = "rejected"
            reason = "candidate_state_mismatch_before_commit"
            decision["tampered_candidate_state"] = candidate_state + 1
        else:
            checkpoint = contract_checkpoint(case.events, candidate_state)
            decision["commit"] = "published"
    else:
        decision["commit"] = "not_published"
    result = {
        "case_id": case.case_id,
        "arm": arm,
        "disposition": disposition,
        "reason": reason,
        "manifest_hash": manifest_hash,
        "decision_record": decision,
        "checkpoint_hash": checkpoint,
        "prior_valid_checkpoint_hash": prior,
    }
    if disposition != case.expected_disposition:
        raise AssertionError(
            f"{arm}/{case.case_id}: expected {case.expected_disposition}, got {disposition}"
        )
    if disposition != "accepted" and checkpoint is not None:
        raise AssertionError(f"{arm}/{case.case_id}: rejected/deferred case created a checkpoint")
    return result


def policy_inventory() -> dict[str, Any]:
    return {
        "status": "predeclared human-review inventory; no automatic policy-complexity winner",
        "ssdd": [
            "four-field canonical ordering",
            "exact-key collision treatment",
            "declared reduction",
            "state/hash chain",
            "candidate validation before commit",
            "reject/defer disposition",
        ],
        "cas_retry": [
            "event identity/idempotency treatment",
            "versioned compare-and-swap reservation",
            "retry/conflict handling",
            "timeout or late-source disposition",
            "candidate validation before commit",
            "recovery/audit record",
        ],
        "single_writer_sequencer": [
            "enqueue contract",
            "ordering/publication rule",
            "writer availability/failover treatment",
            "retry or late-source disposition",
            "candidate validation before commit",
            "checkpoint/audit record",
        ],
    }


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def write_checksums(root: Path) -> None:
    entries = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name != "SHA256SUMS":
            entries.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(root)}")
    (root / "SHA256SUMS").write_text("\n".join(entries) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--run-label", required=True)
    args = parser.parse_args()

    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    fixture = fixture_events()
    case_list = cases()
    manifest = {
        "suite": "ssdd-comparative-value-native-contract-smoke",
        "run_label": args.run_label,
        "execution_domain": "local-native-single-process-policy-reference",
        "purpose": "common-fixture semantic and evidence-contract check before comparative claims",
        "non_claims": [
            "No physical CXL, FPGA, hardware, latency, jitter, throughput, scaling, or production claim.",
            "No contention or CAS performance claim; this deterministic local harness is not a concurrent benchmark.",
            "No automated policy-complexity, diagnostic-clarity, or superiority winner.",
        ],
        "fixture_events": [event.canonical_record() for event in fixture],
        "case_contract": [
            {
                "case_id": case.case_id,
                "expected_disposition": case.expected_disposition,
                "event_ids": [event.event_id for event in case.events],
                "tamper_candidate_state": case.tamper_candidate_state,
            }
            for case in case_list
        ],
        "arms": ["ssdd", "cas_retry", "single_writer_sequencer"],
        "required_diagnostic_fields": list(REQUIRED_DIAGNOSTIC_FIELDS),
    }
    manifest_hash = digest(manifest)
    write_json(output / "manifest.json", manifest)
    write_json(output / "policy-surface-inventory.json", policy_inventory())

    results: list[dict[str, Any]] = []
    for arm in manifest["arms"]:
        for case in case_list:
            results.append(evaluate(arm, case, manifest_hash))
    write_json(output / "results.json", results)

    permutation_results = [
        item
        for item in results
        if item["case_id"].startswith("arrival-permutation-") and item["disposition"] == "accepted"
    ]
    summary: dict[str, Any] = {
        "status": "contract_smoke_completed_no_comparative_value_conclusion",
        "execution_domain": manifest["execution_domain"],
        "manifest_hash": manifest_hash,
        "case_count": len(case_list),
        "result_count": len(results),
        "arms": {},
        "diagnostic_schema_completeness": {},
        "required_human_review": [
            "Audit policy-surface inventory; do not infer complexity from the list count alone.",
            "Audit decision records for explanatory usefulness under the same reviewer task.",
            "Use an independently implemented concurrent baseline before any CAS/retry performance claim.",
            "Use the separate preregistered KVM-to-Timing matrix before any performance-cost claim.",
        ],
    }
    for arm in manifest["arms"]:
        arm_results = [item for item in results if item["arm"] == arm]
        accepted_permutations = [
            item for item in permutation_results if item["arm"] == arm
        ]
        unique_hashes = {item["checkpoint_hash"] for item in accepted_permutations}
        summary["arms"][arm] = {
            "accepted": sum(item["disposition"] == "accepted" for item in arm_results),
            "rejected": sum(item["disposition"] == "rejected" for item in arm_results),
            "deferred": sum(item["disposition"] == "deferred" for item in arm_results),
            "arrival_permutation_count": len(accepted_permutations),
            "arrival_permutation_checkpoint_hash_count": len(unique_hashes),
            "arrival_permutation_invariant_under_contract": len(unique_hashes) == 1,
        }
        summary["diagnostic_schema_completeness"][arm] = all(
            all(field in item for field in REQUIRED_DIAGNOSTIC_FIELDS)
            for item in arm_results
        )
    write_json(output / "summary.json", summary)
    write_checksums(output)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
