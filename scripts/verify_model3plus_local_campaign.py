#!/usr/bin/env python3
"""Verify the evidence shape and dispositions for the SSDD Model 3+ local A–E campaign.

The verifier intentionally checks behavioral and integrity artifacts only. It does
not calculate, summarize, or interpret latency, jitter, throughput, or hardware
performance data.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    if not path.is_file():
        raise AssertionError(f"missing expected JSON artifact: {path}")
    return json.loads(path.read_text())


def text_has(path: Path, expected: str) -> None:
    if not path.is_file():
        raise AssertionError(f"missing expected text artifact: {path}")
    if expected not in path.read_text():
        raise AssertionError(f"expected marker {expected!r} not found in {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args()
    outdir = args.outdir.resolve()
    prehardware = outdir / "prehardware"

    ordering = load_json(prehardware / "ordering.json")
    ordering_stress = load_json(prehardware / "ordering-chain-stress.json")
    replay = load_json(prehardware / "replay-independent.json")
    faults = load_json(prehardware / "faults.json")
    recovery = load_json(prehardware / "fault-recovery.json")
    ledger = load_json(prehardware / "ledger-tamper.json")
    cross_language = load_json(prehardware / "cross-language.json")

    assert ordering["domain"] == "native_reference"
    assert ordering["all_permutations_equal"] is True
    assert ordering["exact_four_key_duplicate_rejected"] is True
    assert ordering_stress["all_full_hash_chains_equal"] is True
    assert replay["domain"] == "native_reference_independent_processes"
    assert replay["full_hash_chain_equal"] is True
    assert replay["run_a_accepted"] is True and replay["run_b_accepted"] is True
    assert len(faults["cases"]) == 4
    assert all(case["result"] == "rejected" for case in faults["cases"])
    assert all(case["last_valid_state_preserved"] is True for case in faults["cases"])
    assert len(recovery["cases"]) == 4
    assert all(case["resumed_chain_accepted"] is True for case in recovery["cases"])
    assert all(case["post_checkpoint_suffix_equal"] is True for case in recovery["cases"])
    assert len(ledger["tamper_cases"]) == 4
    assert all(case["detected"] == "true" for case in ledger["tamper_cases"])
    assert cross_language["full_hash_chain_equal"] is True

    text_has(outdir / "proof-accepted.txt", "validation=accepted")
    text_has(outdir / "proof-corruption.txt", "fault_mode=proof-corruption")
    text_has(outdir / "proof-corruption.txt", "validation=rejected")

    result = {
        "campaign": "SSDD Model 3+ local evidence packages A-E",
        "status": "accepted",
        "execution_domains": [
            "native_reference",
            "native_reference_independent_processes",
            "native_python_reference",
            "native_rust_reference",
            "native_compiled_reference_workload",
        ],
        "packages": {
            "A_adversarial_functional": {
                "status": "accepted",
                "invariants": ["O-1", "O-2", "S-1", "R-1"],
                "evidence": [
                    "ordering.json",
                    "ordering-chain-stress.json",
                    "faults.json",
                    "fault-recovery.json",
                    "replay-independent.json",
                ],
            },
            "B_ledger_and_proof_integrity": {
                "status": "accepted",
                "invariants": ["L-1", "S-1"],
                "evidence": ["ledger-tamper.json", "proof-accepted.txt", "proof-corruption.txt"],
            },
            "C_cross_implementation_replay": {
                "status": "accepted",
                "invariant": "R-1",
                "evidence": ["python-ledger.json", "rust-ledger.json", "cross-language.json"],
            },
            "D_cross_domain_sanity": {
                "status": "documented",
                "evidence": ["docs/validation/model3plus-local-campaign-plan.md"],
            },
            "E_artifact_register": {
                "status": "pending_hash_generation",
                "evidence": ["run-manifest.txt", "source-register.sha256", "SHA256SUMS"],
            },
        },
        "limitations": [
            "No latency, jitter, throughput, overhead, or timing result was collected or interpreted.",
            "No gem5/KVM, Timing CPU, FPGA, physical CXL Type-3, silicon, network, security, or production claim is made.",
            "The Rust comparator is a narrow retained reference implementation, not an external supplied runtime.",
            "The native compiled proof workload validates its declared reference logic only and is not a CXL or gem5 execution result.",
        ],
    }
    (outdir / "verification.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "accepted", "packages": ["A", "B", "C", "D", "E"]}, sort_keys=True))


if __name__ == "__main__":
    main()
