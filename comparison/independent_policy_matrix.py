#!/usr/bin/env python3
"""Independent local policy references for the SSDD comparative-value campaign.

The three arms intentionally do not invoke a shared validator.  They share
only a fixed fixture format and a referee checkpoint digest.  This is a local
semantic/diagnostic matrix, not a performance or hardware experiment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


GENESIS = "0" * 64
ARMS = ("ssdd", "cas_retry", "single_writer_sequencer")


def stable_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
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
    def key(self) -> tuple[int, int, int, int]:
        return (self.structural_dim, self.enterprise_type, self.sequence_id, self.source_chiplet_id)

    def record(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Case:
    case_id: str
    events: tuple[Event, ...]
    expected_ids: tuple[str, ...]
    expected_disposition: str
    candidate_state_tamper: bool = False


def base_events() -> tuple[Event, ...]:
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


def make_cases() -> list[Case]:
    baseline = base_events()
    expected_ids = tuple(event.event_id for event in baseline)
    output = [Case("positive-control", baseline, expected_ids, "accepted")]
    for seed in range(128):
        shuffled = list(baseline)
        random.Random(0x5A5D000 + seed).shuffle(shuffled)
        output.append(Case(f"arrival-permutation-{seed:03d}", tuple(shuffled), expected_ids, "accepted"))
    output.extend(
        [
            Case(
                "exact-event-id-collision",
                baseline
                + (
                    Event(
                        event_id=baseline[2].event_id,
                        structural_dim=baseline[2].structural_dim,
                        enterprise_type=baseline[2].enterprise_type,
                        sequence_id=baseline[2].sequence_id,
                        source_chiplet_id=baseline[2].source_chiplet_id,
                        payload=baseline[2].payload + 1,
                    ),
                ),
                expected_ids,
                "rejected",
            ),
            Case("late-source", baseline[:-1], expected_ids, "deferred"),
            Case(
                "proof-corruption",
                baseline[:5]
                + (Event(**{**asdict(baseline[5]), "proof_valid": False}),)
                + baseline[6:],
                expected_ids,
                "rejected",
            ),
            Case("candidate-state-corruption", baseline, expected_ids, "rejected", True),
        ]
    )
    return output


def checkpoint(events: list[Event], state: int) -> str:
    return stable_hash(
        {
            "contract": "shared-checkpoint-v1",
            "event_ids": sorted(event.event_id for event in events),
            "state": state,
        }
    )


def result(
    arm: str,
    case: Case,
    manifest_hash: str,
    disposition: str,
    reason: str,
    trace: dict[str, Any],
    accepted_events: list[Event] | None = None,
    candidate_state: int | None = None,
) -> dict[str, Any]:
    committed = disposition == "accepted"
    if committed:
        assert accepted_events is not None and candidate_state is not None
        checkpoint_hash = checkpoint(accepted_events, candidate_state)
        trace["commit"] = "published"
    else:
        checkpoint_hash = None
        trace["commit"] = "not_published"
    return {
        "arm": arm,
        "case_id": case.case_id,
        "disposition": disposition,
        "reason": reason,
        "manifest_hash": manifest_hash,
        "decision_record": trace,
        "checkpoint_hash": checkpoint_hash,
        "prior_valid_checkpoint_hash": GENESIS,
    }


def ssdd_arm(case: Case, manifest_hash: str) -> dict[str, Any]:
    seen_ids: dict[str, dict[str, Any]] = {}
    seen_keys: set[tuple[int, int, int, int]] = set()
    trace: dict[str, Any] = {"policy": "canonical-four-field-commit-policy", "checks": []}
    for event in case.events:
        existing = seen_ids.get(event.event_id)
        if existing is not None and existing != event.record():
            return result("ssdd", case, manifest_hash, "rejected", f"ssdd:conflicting_event_id:{event.event_id}", trace)
        seen_ids[event.event_id] = event.record()
        if not event.proof_valid:
            return result("ssdd", case, manifest_hash, "rejected", f"ssdd:invalid_proof:{event.event_id}", trace)
        if event.key in seen_keys:
            return result("ssdd", case, manifest_hash, "rejected", "ssdd:exact_four_key_collision", trace)
        seen_keys.add(event.key)
    missing = sorted(set(case.expected_ids) - set(seen_ids))
    unexpected = sorted(set(seen_ids) - set(case.expected_ids))
    if missing or unexpected:
        return result("ssdd", case, manifest_hash, "deferred", f"ssdd:incomplete_or_unexpected_set:missing={missing};unexpected={unexpected}", trace)
    ordered = sorted(case.events, key=lambda event: event.key)
    state = sum(event.payload for event in ordered)
    trace.update({"ordered_keys": [event.key for event in ordered], "ordered_batch_hash": stable_hash([event.record() for event in ordered]), "candidate_state": state})
    if case.candidate_state_tamper:
        trace["tampered_candidate_state"] = state + 1
        return result("ssdd", case, manifest_hash, "rejected", "ssdd:candidate_state_mismatch_before_commit", trace)
    return result("ssdd", case, manifest_hash, "accepted", "ssdd:canonical_batch_validated", trace, ordered, state)


def cas_retry_arm(case: Case, manifest_hash: str) -> dict[str, Any]:
    """Versioned event-set admission with a predeclared stale-snapshot retry.

    Pairwise arrivals deliberately share an initial snapshot: the first write
    advances the version, the second detects it and retries. This is a semantic
    CAS/retry reference, not a scheduler or throughput measurement.
    """
    store: dict[str, dict[str, Any]] = {}
    version = 0
    trace: dict[str, Any] = {"policy": "versioned-cas-retry-with-canonicalized-candidate", "admissions": []}
    for start in range(0, len(case.events), 2):
        pair = case.events[start : start + 2]
        snapshot_version = version
        for position, event in enumerate(pair):
            attempts = 1
            expected_version = snapshot_version
            if position == 1 and version != expected_version:
                attempts += 1
                expected_version = version
            existing = store.get(event.event_id)
            if existing is not None and existing != event.record():
                return result("cas_retry", case, manifest_hash, "rejected", f"cas_retry:conflicting_event_id:{event.event_id}", trace)
            if not event.proof_valid:
                return result("cas_retry", case, manifest_hash, "rejected", f"cas_retry:invalid_proof:{event.event_id}", trace)
            if version != expected_version:
                raise AssertionError("cas reference exhausted retry before expected publication")
            store[event.event_id] = event.record()
            version += 1
            trace["admissions"].append({"event_id": event.event_id, "attempts": attempts, "published_version": version})
    missing = sorted(set(case.expected_ids) - set(store))
    unexpected = sorted(set(store) - set(case.expected_ids))
    if missing or unexpected:
        return result("cas_retry", case, manifest_hash, "deferred", f"cas_retry:incomplete_or_unexpected_set:missing={missing};unexpected={unexpected}", trace)
    candidate = sorted(case.events, key=lambda event: event.key)
    state = sum(event.payload for event in candidate)
    trace.update({"final_store_version": version, "candidate_snapshot_order": [event.event_id for event in candidate], "canonicalization_policy_surface": "explicit"})
    if case.candidate_state_tamper:
        trace["tampered_candidate_state"] = state + 1
        return result("cas_retry", case, manifest_hash, "rejected", "cas_retry:candidate_state_mismatch_before_commit", trace)
    return result("cas_retry", case, manifest_hash, "accepted", "cas_retry:versioned_candidate_validated", trace, candidate, state)


def sequencer_arm(case: Case, manifest_hash: str) -> dict[str, Any]:
    queue: list[Event] = []
    seen_ids: dict[str, dict[str, Any]] = {}
    trace: dict[str, Any] = {"policy": "single-writer-sequencer-with-canonical-queue-drain", "enqueue_log": []}
    for event in case.events:
        existing = seen_ids.get(event.event_id)
        if existing is not None and existing != event.record():
            return result("single_writer_sequencer", case, manifest_hash, "rejected", f"single_writer_sequencer:conflicting_event_id:{event.event_id}", trace)
        if not event.proof_valid:
            return result("single_writer_sequencer", case, manifest_hash, "rejected", f"single_writer_sequencer:invalid_proof:{event.event_id}", trace)
        seen_ids[event.event_id] = event.record()
        queue.append(event)
        trace["enqueue_log"].append({"event_id": event.event_id, "arrival_position": len(queue) - 1})
    missing = sorted(set(case.expected_ids) - set(seen_ids))
    unexpected = sorted(set(seen_ids) - set(case.expected_ids))
    if missing or unexpected:
        return result("single_writer_sequencer", case, manifest_hash, "deferred", f"single_writer_sequencer:incomplete_or_unexpected_set:missing={missing};unexpected={unexpected}", trace)
    drained = sorted(queue, key=lambda event: event.key)
    state = sum(event.payload for event in drained)
    trace.update({"queue_drain_order": [event.event_id for event in drained], "canonical_queue_drain_policy_surface": "explicit", "publish_count": 1})
    if case.candidate_state_tamper:
        trace["tampered_candidate_state"] = state + 1
        return result("single_writer_sequencer", case, manifest_hash, "rejected", "single_writer_sequencer:candidate_state_mismatch_before_commit", trace)
    return result("single_writer_sequencer", case, manifest_hash, "accepted", "single_writer_sequencer:queue_drained_and_validated", trace, drained, state)


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def checksums(root: Path) -> None:
    values = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name not in {"SHA256SUMS", "checksum-verification.txt"}:
            values.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(root)}")
    (root / "SHA256SUMS").write_text("\n".join(values) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--run-label", required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    case_list = make_cases()
    manifest = {
        "suite": "ssdd-comparative-value-native-independent-policy-matrix",
        "run_label": args.run_label,
        "execution_domain": "local-native-policy-references",
        "purpose": "independent semantic and diagnostic policy implementations under one fixture contract",
        "non_claims": [
            "No physical CXL, FPGA, hardware, latency, jitter, throughput, scaling, or production claim.",
            "No scheduler, contention, or throughput result from the deterministic CAS/retry reference.",
            "No automatic winner for policy compactness, clarity, or superiority.",
        ],
        "fixture_events": [event.record() for event in base_events()],
        "case_contract": [{"case_id": case.case_id, "expected_disposition": case.expected_disposition, "event_ids": [event.event_id for event in case.events], "candidate_state_tamper": case.candidate_state_tamper} for case in case_list],
        "arms": list(ARMS),
        "required_diagnostic_fields": ["manifest_hash", "decision_record", "checkpoint_hash", "prior_valid_checkpoint_hash", "disposition", "reason"],
    }
    manifest_hash = stable_hash(manifest)
    write_json(args.output / "manifest.json", manifest)
    evaluators = {"ssdd": ssdd_arm, "cas_retry": cas_retry_arm, "single_writer_sequencer": sequencer_arm}
    rows = [evaluators[arm](case, manifest_hash) for arm in ARMS for case in case_list]
    for row in rows:
        required = set(manifest["required_diagnostic_fields"])
        if not required.issubset(row):
            raise AssertionError(f"missing diagnostic fields: {row['arm']}/{row['case_id']}")
        expected = next(case.expected_disposition for case in case_list if case.case_id == row["case_id"])
        if row["disposition"] != expected:
            raise AssertionError(f"unexpected disposition: {row['arm']}/{row['case_id']}")
    write_json(args.output / "results.json", rows)
    summary: dict[str, Any] = {"status": "native_independent_policy_matrix_completed_no_value_winner", "execution_domain": manifest["execution_domain"], "manifest_hash": manifest_hash, "case_count": len(case_list), "result_count": len(rows), "arms": {}, "required_human_review": ["Compare a reviewer’s ability to answer the same acceptance/rejection question from each arm’s evidence bundle.", "Review independent policy surfaces; canonicalization added to CAS/retry and sequencer is a legitimate baseline cost, not an SSDD win by default.", "Implement a concurrent CAS/retry workload before claiming contention or performance cost.", "Promote only an approved common matrix to gem5 or SimCXL."]}
    for arm in ARMS:
        arm_rows = [row for row in rows if row["arm"] == arm]
        permutation_hashes = {row["checkpoint_hash"] for row in arm_rows if row["case_id"].startswith("arrival-permutation-")}
        summary["arms"][arm] = {"accepted": sum(row["disposition"] == "accepted" for row in arm_rows), "rejected": sum(row["disposition"] == "rejected" for row in arm_rows), "deferred": sum(row["disposition"] == "deferred" for row in arm_rows), "arrival_permutation_checkpoint_hash_count": len(permutation_hashes), "arrival_permutation_invariant_under_contract": len(permutation_hashes) == 1}
    write_json(args.output / "summary.json", summary)
    checksums(args.output)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
