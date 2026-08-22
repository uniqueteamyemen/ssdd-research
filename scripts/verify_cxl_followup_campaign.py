#!/usr/bin/env python3
"""Verify a model-scoped CXL follow-up run without inferring performance evidence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--preflight", required=True, type=Path)
    args = parser.parse_args()

    matrix = args.run_dir / "matrix.csv"
    preflight = args.preflight / "kvm-preflight.json"
    if not matrix.is_file() or not preflight.is_file():
        raise SystemExit("missing matrix.csv or kvm-preflight.json")

    preflight_data = json.loads(preflight.read_text())
    with matrix.open(newline="") as handle:
        raw_rows = list(csv.DictReader(handle))

    cases = []
    overall = "accepted"
    for row in raw_rows:
        validation = row.get("validation", "")
        fault = row.get("fault", "")
        sim_exit = row.get("sim_exit", "")
        guest_exit = row.get("guest_exit", "")
        if validation == "accepted" and sim_exit == "0" and guest_exit == "0":
            disposition = "accepted"
        elif validation == "rejected" and fault == "proof-corruption" and guest_exit == "2":
            disposition = "rejected as designed"
        else:
            disposition = "failed"
            overall = "failed"
        cases.append({**row, "disposition": disposition})

    kvm_preflight_passed = preflight_data["status"] != "blocked_host_kvm_prerequisites_missing"
    report = {
        "campaign_scope": "CXL Type-3 simulation behavioral follow-up",
        "overall_disposition": overall,
        "kvm_preflight_status": preflight_data["status"],
        "measurement_status": (
            "eligible_only_after_retained_gem5_kvm_to_timing_roi_confirmation"
            if kvm_preflight_passed
            else "not_collected_atomic_cpu_behavioral_evidence_only"
        ),
        "unsupported_factors": {
            "contention_or_interference": "NOT_SUPPORTED_BY_CURRENT_SIMCXL_ADAPTER",
            "T_admit": "NOT_INSTRUMENTED_BY_CURRENT_WORKLOAD",
            "T_order": "NOT_INSTRUMENTED_BY_CURRENT_WORKLOAD",
            "T_snapshot": "NOT_INSTRUMENTED_BY_CURRENT_WORKLOAD",
            "T_commit": "NOT_INSTRUMENTED_BY_CURRENT_WORKLOAD",
            "T_total": "NOT_INSTRUMENTED_BY_CURRENT_WORKLOAD",
        },
        "cases": cases,
        "input_files": {
            "matrix.csv": sha256(matrix),
            "kvm-preflight.json": sha256(preflight),
        },
    }
    (args.run_dir / "verification.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
