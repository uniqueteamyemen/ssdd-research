#!/usr/bin/env python3
"""Concurrent local policy references for the SSDD comparative-value campaign.

Each arm has its own admission/publication path.  Thread scheduling is used to
exercise contention/arrival variation, but this harness records no timing
metric and makes no concurrency-performance claim.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import queue
import threading
from pathlib import Path
from typing import Any

from independent_policy_matrix import ARMS, Case, Event, checkpoint, make_cases, stable_hash


GENESIS = "0" * 64


def packaged_result(
    arm: str,
    case: Case,
    manifest_hash: str,
    disposition: str,
    reason: str,
    trace: dict[str, Any],
    final_events: list[Event] | None = None,
    state: int | None = None,
) -> dict[str, Any]:
    if disposition == "accepted":
        assert final_events is not None and state is not None
        trace["commit"] = "published"
        checkpoint_hash = checkpoint(final_events, state)
    else:
        trace["commit"] = "not_published"
        checkpoint_hash = None
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


def required_set_outcome(
    arm: str, actual_ids: set[str], expected_ids: set[str]
) -> tuple[str, str] | None:
    missing = sorted(expected_ids - actual_ids)
    unexpected = sorted(actual_ids - expected_ids)
    if missing or unexpected:
        return "deferred", f"{arm}:incomplete_or_unexpected_set:missing={missing};unexpected={unexpected}"
    return None


def concurrent_ssdd(case: Case, manifest_hash: str) -> dict[str, Any]:
    lock = threading.Lock()
    barrier = threading.Barrier(len(case.events))
    arrivals: list[Event] = []
    arrival_log: list[dict[str, Any]] = []

    def producer(event: Event) -> None:
        barrier.wait()
        with lock:
            arrival_log.append({"event_id": event.event_id, "arrival_index": len(arrivals)})
            arrivals.append(event)

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(case.events)) as pool:
        list(pool.map(producer, case.events))
    trace: dict[str, Any] = {
        "policy": "concurrent-producer-ssdd-canonical-commit",
        "arrival_log": arrival_log,
        "checks": [],
    }
    seen_ids: dict[str, dict[str, Any]] = {}
    seen_keys: set[tuple[int, int, int, int]] = set()
    for event in arrivals:
        existing = seen_ids.get(event.event_id)
        if existing is not None and existing != event.record():
            return packaged_result("ssdd", case, manifest_hash, "rejected", f"ssdd:conflicting_event_id:{event.event_id}", trace)
        seen_ids[event.event_id] = event.record()
        if not event.proof_valid:
            return packaged_result("ssdd", case, manifest_hash, "rejected", f"ssdd:invalid_proof:{event.event_id}", trace)
        if event.key in seen_keys:
            return packaged_result("ssdd", case, manifest_hash, "rejected", "ssdd:exact_four_key_collision", trace)
        seen_keys.add(event.key)
    set_outcome = required_set_outcome("ssdd", set(seen_ids), set(case.expected_ids))
    if set_outcome:
        return packaged_result("ssdd", case, manifest_hash, *set_outcome, trace)
    ordered = sorted(arrivals, key=lambda event: event.key)
    state = sum(event.payload for event in ordered)
    trace.update({"ordered_keys": [event.key for event in ordered], "ordered_batch_hash": stable_hash([event.record() for event in ordered]), "candidate_state": state})
    if case.candidate_state_tamper:
        trace["tampered_candidate_state"] = state + 1
        return packaged_result("ssdd", case, manifest_hash, "rejected", "ssdd:candidate_state_mismatch_before_commit", trace)
    return packaged_result("ssdd", case, manifest_hash, "accepted", "ssdd:canonical_batch_validated", trace, ordered, state)


def concurrent_cas_retry(case: Case, manifest_hash: str) -> dict[str, Any]:
    lock = threading.Lock()
    barrier = threading.Barrier(len(case.events))
    store: dict[str, dict[str, Any]] = {}
    stored_events: dict[str, Event] = {}
    version = 0
    errors: list[str] = []
    admission_log: list[dict[str, Any]] = []

    def producer(event: Event) -> None:
        nonlocal version
        expected_version = 0
        barrier.wait()
        attempts = 0
        while True:
            attempts += 1
            with lock:
                existing = store.get(event.event_id)
                if existing is not None:
                    if existing != event.record():
                        errors.append(f"cas_retry:conflicting_event_id:{event.event_id}")
                    admission_log.append({"event_id": event.event_id, "attempts": attempts, "outcome": "duplicate_or_conflict"})
                    return
                if not event.proof_valid:
                    errors.append(f"cas_retry:invalid_proof:{event.event_id}")
                    admission_log.append({"event_id": event.event_id, "attempts": attempts, "outcome": "invalid_proof"})
                    return
                if version != expected_version:
                    expected_version = version
                    continue
                store[event.event_id] = event.record()
                stored_events[event.event_id] = event
                version += 1
                admission_log.append({"event_id": event.event_id, "attempts": attempts, "outcome": "published_to_versioned_store", "published_version": version})
                return

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(case.events)) as pool:
        list(pool.map(producer, case.events))
    trace: dict[str, Any] = {
        "policy": "concurrent-versioned-cas-retry-with-canonicalized-candidate",
        "admission_log": admission_log,
        "final_store_version": version,
    }
    if errors:
        return packaged_result("cas_retry", case, manifest_hash, "rejected", sorted(errors)[0], trace)
    set_outcome = required_set_outcome("cas_retry", set(stored_events), set(case.expected_ids))
    if set_outcome:
        return packaged_result("cas_retry", case, manifest_hash, *set_outcome, trace)
    candidate = sorted(stored_events.values(), key=lambda event: event.key)
    state = sum(event.payload for event in candidate)
    trace.update({"candidate_snapshot_order": [event.event_id for event in candidate], "canonicalization_policy_surface": "explicit", "candidate_state": state})
    if case.candidate_state_tamper:
        trace["tampered_candidate_state"] = state + 1
        return packaged_result("cas_retry", case, manifest_hash, "rejected", "cas_retry:candidate_state_mismatch_before_commit", trace)
    return packaged_result("cas_retry", case, manifest_hash, "accepted", "cas_retry:versioned_candidate_validated", trace, candidate, state)


def concurrent_sequencer(case: Case, manifest_hash: str) -> dict[str, Any]:
    barrier = threading.Barrier(len(case.events))
    inbound: queue.Queue[Event] = queue.Queue()

    def producer(event: Event) -> None:
        barrier.wait()
        inbound.put(event)

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(case.events)) as pool:
        list(pool.map(producer, case.events))
    queue_log: list[dict[str, Any]] = []
    seen_ids: dict[str, dict[str, Any]] = {}
    queued: list[Event] = []
    while not inbound.empty():
        event = inbound.get_nowait()
        queue_log.append({"event_id": event.event_id, "queue_position": len(queued)})
        existing = seen_ids.get(event.event_id)
        if existing is not None and existing != event.record():
            return packaged_result("single_writer_sequencer", case, manifest_hash, "rejected", f"single_writer_sequencer:conflicting_event_id:{event.event_id}", {"policy": "concurrent-producer-single-writer-sequencer", "enqueue_log": queue_log})
        if not event.proof_valid:
            return packaged_result("single_writer_sequencer", case, manifest_hash, "rejected", f"single_writer_sequencer:invalid_proof:{event.event_id}", {"policy": "concurrent-producer-single-writer-sequencer", "enqueue_log": queue_log})
        seen_ids[event.event_id] = event.record()
        queued.append(event)
    trace: dict[str, Any] = {"policy": "concurrent-producer-single-writer-sequencer-with-canonical-queue-drain", "enqueue_log": queue_log}
    set_outcome = required_set_outcome("single_writer_sequencer", set(seen_ids), set(case.expected_ids))
    if set_outcome:
        return packaged_result("single_writer_sequencer", case, manifest_hash, *set_outcome, trace)
    drained = sorted(queued, key=lambda event: event.key)
    state = sum(event.payload for event in drained)
    trace.update({"queue_drain_order": [event.event_id for event in drained], "canonical_queue_drain_policy_surface": "explicit", "publish_count": 1, "candidate_state": state})
    if case.candidate_state_tamper:
        trace["tampered_candidate_state"] = state + 1
        return packaged_result("single_writer_sequencer", case, manifest_hash, "rejected", "single_writer_sequencer:candidate_state_mismatch_before_commit", trace)
    return packaged_result("single_writer_sequencer", case, manifest_hash, "accepted", "single_writer_sequencer:queue_drained_and_validated", trace, drained, state)


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def checksums(root: Path) -> None:
    values = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name not in {"SHA256SUMS", "checksum-verification.txt"}:
            values.append(f"{__import__('hashlib').sha256(path.read_bytes()).hexdigest()}  {path.relative_to(root)}")
    (root / "SHA256SUMS").write_text("\n".join(values) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--run-label", required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    cases = make_cases()
    manifest = {
        "suite": "ssdd-comparative-value-local-concurrent-policy-matrix",
        "run_label": args.run_label,
        "execution_domain": "local-native-threaded-policy-references",
        "purpose": "independent concurrent admission/publish-path semantics without timing metrics",
        "non_claims": ["No latency, jitter, p95/p99, throughput, overhead, scaling, hardware, CXL, or production claim.", "Thread scheduling/order traces are not reproducibility or performance metrics.", "No automatic comparative-value winner."],
        "arms": list(ARMS),
        "case_contract": [{"case_id": case.case_id, "expected_disposition": case.expected_disposition, "event_ids": [event.event_id for event in case.events], "candidate_state_tamper": case.candidate_state_tamper} for case in cases],
        "required_diagnostic_fields": ["manifest_hash", "decision_record", "checkpoint_hash", "prior_valid_checkpoint_hash", "disposition", "reason"],
    }
    manifest_hash = stable_hash(manifest)
    write_json(args.output / "manifest.json", manifest)
    evaluators = {"ssdd": concurrent_ssdd, "cas_retry": concurrent_cas_retry, "single_writer_sequencer": concurrent_sequencer}
    rows = [evaluators[arm](case, manifest_hash) for arm in ARMS for case in cases]
    for row in rows:
        expected = next(case.expected_disposition for case in cases if case.case_id == row["case_id"])
        if row["disposition"] != expected:
            raise AssertionError(f"unexpected disposition: {row['arm']}/{row['case_id']}")
        if not set(manifest["required_diagnostic_fields"]).issubset(row):
            raise AssertionError(f"incomplete diagnostic record: {row['arm']}/{row['case_id']}")
    write_json(args.output / "results.json", rows)
    summary: dict[str, Any] = {"status": "concurrent_local_policy_matrix_completed_no_value_winner", "execution_domain": manifest["execution_domain"], "manifest_hash": manifest_hash, "case_count": len(cases), "result_count": len(rows), "arms": {}, "required_human_review": ["Run blinded reviewer tasks against each arm’s record bundle.", "Review policy surfaces and operational tradeoffs; a baseline that canonicalizes is not a failed baseline.", "Do not measure or claim performance until a separate preregistered matrix exists.", "Do not promote to Cherry before the human review gate is complete."]}
    for arm in ARMS:
        arm_rows = [row for row in rows if row["arm"] == arm]
        hashes = {row["checkpoint_hash"] for row in arm_rows if row["case_id"].startswith("arrival-permutation-")}
        summary["arms"][arm] = {"accepted": sum(row["disposition"] == "accepted" for row in arm_rows), "rejected": sum(row["disposition"] == "rejected" for row in arm_rows), "deferred": sum(row["disposition"] == "deferred" for row in arm_rows), "arrival_permutation_checkpoint_hash_count": len(hashes), "arrival_permutation_invariant_under_contract": len(hashes) == 1}
    write_json(args.output / "summary.json", summary)
    checksums(args.output)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
