#!/usr/bin/env python3
"""Independent reference comparator for the bounded SSC RTL trace.

This utility verifies only the fixed eight-packet ordering vector used by the
RTL testbench. It is not a proof of the Python reference model, a CXL test, or
an RTL equivalence proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

INPUTS = [
    (2, 1, 3, 7, 0, 0), (0, 3, 2, 1, 1, 1),
    (1, 0, 9, 9, 2, 2), (0, 3, 1, 10, 3, 3),
    (2, 0, 1, 2, 4, 4), (1, 0, 8, 9, 5, 5),
    (0, 3, 1, 3, 6, 6), (2, 0, 1, 1, 7, 7),
]
EXPECTED = sorted(INPUTS, key=lambda packet: packet[:4])
TRACE = re.compile(
    r"^RTL_SSC_TRACE case=affine trial=(\d+) index=(\d+) "
    r"key=(\d+),(\d+),(\d+),(\d+) node=(\d+) payload=(-?\d+)$"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--expected-json", type=Path, required=True)
    args = parser.parse_args()

    expected_serialized = [
        {
            "structural_dim": packet[0], "enterprise_type": packet[1],
            "sequence_id": packet[2], "source_chiplet_id": packet[3],
            "node_id": packet[5], "payload_q32": packet[4] << 32,
        }
        for packet in EXPECTED
    ]
    args.expected_json.write_text(
        json.dumps({"vector": expected_serialized}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    batches: dict[int, list[tuple[int, int, int, int, int, int]]] = {}
    for line in args.log.read_text(encoding="utf-8").splitlines():
        match = TRACE.match(line)
        if match:
            trial, index, *fields = map(int, match.groups())
            batch = batches.setdefault(trial, [])
            if index != len(batch):
                raise SystemExit(f"non-contiguous trace index in trial {trial}: {index}")
            batch.append(tuple(fields))

    expected_trace = [
        (packet[0], packet[1], packet[2], packet[3], packet[5], packet[4] << 32)
        for packet in EXPECTED
    ]
    if sorted(batches) != list(range(128)):
        raise SystemExit(f"expected traces for trials 0..127, received {sorted(batches)}")
    for trial, trace in batches.items():
        if trace != expected_trace:
            raise SystemExit(f"reference mismatch in affine trial {trial}")

    trace_bytes = "\n".join(
        "|".join(map(str, packet)) for packet in expected_trace
    ).encode("utf-8")
    print(
        "RTL_SSC_REFERENCE_COMPARE status=PASS "
        f"batches=128 canonical_trace_sha256={hashlib.sha256(trace_bytes).hexdigest()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
