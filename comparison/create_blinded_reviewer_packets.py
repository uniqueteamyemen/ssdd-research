#!/usr/bin/env python3
"""Create an arm-blinded reviewer packet from one comparative result bundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SELECTED_CASES = (
    "positive-control",
    "arrival-permutation-064",
    "exact-event-id-collision",
    "late-source",
    "proof-corruption",
    "candidate-state-corruption",
)
BLIND_LABELS = {
    "ssdd": "A",
    "cas_retry": "B",
    "single_writer_sequencer": "C",
}


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows: list[dict[str, Any]] = json.loads((args.source / "results.json").read_text())
    args.output.mkdir(parents=True, exist_ok=True)
    packets = []
    for case_id in SELECTED_CASES:
        for row in rows:
            if row["case_id"] != case_id:
                continue
            blind = BLIND_LABELS[row["arm"]]
            packet = {
                "packet_id": f"{case_id}__{blind}",
                "case_id": case_id,
                "arm_label": blind,
                "manifest_hash": row["manifest_hash"],
                "disposition": row["disposition"],
                "reason": row["reason"],
                "decision_record": row["decision_record"],
                "checkpoint_hash": row["checkpoint_hash"],
                "prior_valid_checkpoint_hash": row["prior_valid_checkpoint_hash"],
            }
            write_json(args.output / f"{packet['packet_id']}.json", packet)
            packets.append({"packet_id": packet["packet_id"], "case_id": case_id, "arm_label": blind})
    review_sheet = """# SSDD Comparative Review Sheet (Blinded)

**Use:** Review every JSON packet in this directory without trying to infer the implementation behind labels A, B, or C.  Do not modify the packets.

For each packet, answer the same five questions within the same time budget:

1. Was a new checkpoint published?
2. What exact rule produced the disposition?
3. Which event, key, or condition was material?
4. What is the prior valid checkpoint reference?
5. Which named policy surface would need to change for another outcome?

Record an answer, elapsed review time, and an uncertainty flag per packet in a separate file. A label key is intentionally not included here.
"""
    (args.output / "README.md").write_text(review_sheet)
    write_json(args.output / "packet-index.json", packets)
    write_json(
        args.output.parent / "unblinding-key.json",
        {
            "status": "keep outside reviewer packet until all answers are locked",
            "arm_to_label": BLIND_LABELS,
            "source_bundle": str(args.source),
            "selected_cases": list(SELECTED_CASES),
        },
    )


if __name__ == "__main__":
    main()
