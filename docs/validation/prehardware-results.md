# SSDD Pre-Hardware Deterministic Verification Results

## Result Status

The retained reference suite completed its current acceptance matrix on 17 August 2026. It combines a native deterministic reference harness, a minimal retained Rust reference for the documented ledger rule, and the earlier gem5 simulator evidence. The result supports **reference-model behavior only**. It does not establish hardware timing, distributed fault tolerance, CXL behavior, security certification, or production readiness.

## Core Determinism and Forensics

| Record | Procedure | Observed outcome | Boundary |
|---|---|---:|---|
| SSC ordering | One 48-packet fixture, 128 seeded randomized arrival permutations. | **128 / 128** byte-identical ordered batches; batch hash `8fd17060a85f190a0d977fda225da4528636215e4b25d7038c63d584ec072930`. | The fixture validates the retained reference sort, not concurrent SSC firmware. |
| Four-key collisions | Prefix collisions were sorted by the fourth tuple member; an exact duplicate four-key tuple was submitted separately. | Prefix source ordering **3, 7, 9**; exact duplicate rejected before commit. | Duplicate rejection is an explicit harness safety control because the supplied Python comparator defines no fifth tie-breaker. |
| Full replay | Two independent 100-epoch processes consumed the same generated stream and exposed every chain entry. | **100 / 100** hash-chain entries equal; final hash `34b7958a64082c326ba3a7cab44468ae9564c7ec2072f88533e10426e23f65c2`. | This establishes reproducibility for the retained serialization and generator only. |
| Ledger forensic checks | State hash, previous hash, aggregate, and epoch ID were independently modified at epoch 7. | **4 / 4** modifications detected. | Epoch-ID detection is a continuity check; the documented state-hash formula binds previous hash and serialized state rather than epoch ID directly. |
| Q32.32 boundary set | Saturating addition, multiplication saturation, zero, signed fractional product, and min/max cases. | **9 / 9** cases accepted. | The test follows the manual’s stated semantics using a retained reference because the uploaded engine imports an unavailable `q32_32_core` module. |

## Failure Containment Model

| Fault case | Commit on affected epoch | Last valid state preserved | Result |
|---|---:|---:|---|
| Packet drop | No | Yes | Incomplete batch rejected. |
| Node delay | No | Yes | Late node deferred; no commit created. |
| Aggregator failure | No | Yes | Aggregator unavailable; no commit created. |
| Corrupted state or ledger | No | Yes | Audit validation rejected the altered record. |

The four cases are explicit control-flow models. They establish that the retained reference does not append a new record after the injected condition; they do not measure recovery of an operating distributed cluster.

## Cross-Language and Scaling Record

The supplied source paths contained no Rust source file or Cargo manifest. A small Rust reference was retained solely to implement the same SHA-256 construction, genesis value, Q32.32 aggregate stream, and 100-epoch ledger chain as the Python reference. Python and Rust produced the same 100 hashes and the same final hash `34b7958a64082c326ba3a7cab44468ae9564c7ec2072f88533e10426e23f65c2`. This is not a comparison against a supplied or production Rust runtime.

| Matrix point | Epochs | Packets per epoch | Mean `T_total` | Epoch success | Interpretation boundary |
|---|---:|---:|---:|---:|---|
| 8 logical nodes | 25 | 32 | 22.013 µs | 100% | Native reference wall-clock. |
| 32 logical nodes | 25 | 128 | 83.573 µs | 100% | Native reference wall-clock. |
| 128 logical nodes | 25 | 512 | 277.503 µs | 100% | Native reference wall-clock. |
| 1k events/s-equivalent | 50 | 1 | 2.663 µs | 100% | Input-generation model, not observed network rate. |
| 100k events/s-equivalent | 50 | 100 | 56.426 µs | 100% | Input-generation model, not observed network rate. |

The scaling and load data retain `T_ssc`, `T_agg`, `T_fuse`, `T_total`, packet counts, 28-byte canonical packet serialization, and modeled bytes per epoch. They are not measurements of a NIC, fabric bandwidth, physical convergence, or hardware timing.

### Complete scaling evidence

| Logical nodes | Packets / epoch | Modeled bytes / epoch | `T_ssc` | `T_agg` | `T_fuse` | `T_total` | Reference events / second | Epoch success |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 32 | 896 | 15.962 µs | 4.167 µs | 1.884 µs | 22.013 µs | 478,025.18 | 100% |
| 16 | 64 | 1,792 | 61.918 µs | 8.301 µs | 2.914 µs | 73.133 µs | 372,453.09 | 100% |
| 32 | 128 | 3,584 | 66.185 µs | 14.375 µs | 3.013 µs | 83.573 µs | 432,435.35 | 100% |
| 64 | 256 | 7,168 | 111.590 µs | 22.924 µs | 2.203 µs | 136.716 µs | 547,043.05 | 100% |
| 128 | 512 | 14,336 | 232.230 µs | 41.875 µs | 3.399 µs | 277.503 µs | 514,657.26 | 100% |

### Complete load evidence

| Input model rate | Packets / epoch | Modeled bytes / epoch | `T_ssc` | `T_agg` | `T_fuse` | `T_total` | Observed reference events / second | Epoch success |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1,000 events/s-equivalent | 1 | 28 | 1.086 µs | 0.449 µs | 1.128 µs | 2.663 µs | 131,324.25 | 100% |
| 5,000 events/s-equivalent | 5 | 140 | 2.677 µs | 0.849 µs | 1.012 µs | 4.538 µs | 381,345.20 | 100% |
| 10,000 events/s-equivalent | 10 | 280 | 4.547 µs | 1.338 µs | 1.128 µs | 7.013 µs | 434,260.74 | 100% |
| 25,000 events/s-equivalent | 25 | 700 | 11.291 µs | 2.717 µs | 1.663 µs | 15.671 µs | 511,124.52 | 100% |
| 50,000 events/s-equivalent | 50 | 1,400 | 20.670 µs | 4.513 µs | 1.339 µs | 26.523 µs | 548,823.93 | 100% |
| 100,000 events/s-equivalent | 100 | 2,800 | 45.708 µs | 9.043 µs | 1.675 µs | 56.426 µs | 540,817.09 | 100% |

## Evidence Audit Anchors

The retained result directory contains a machine-readable outcome for each public record: `ordering.json`, `replay-independent.json`, `faults.json`, `ledger-tamper.json`, `q32.json`, `cross-language.json`, and `scaling-load.json`. The full outputs show the following acceptance anchors: **128 / 128** randomized arrivals, rejection of the exact four-key tuple `(4, 2, 99, 9)`, **100 / 100** independent chain entries, **4 / 4** last-valid-state-preserving fault outcomes, **4 / 4** detected ledger changes, **100 / 100** equal Python/Rust reference-chain hashes, and **9 / 9** Q32.32 outcomes. They are retained artifacts, not public downloadable source material.

## Reproducibility Artifacts

The retained harness, independent Rust comparison reference, and generated output records are included in this repository:

```text
reference/python/prehardware_reference.py
reference/rust/prehardware_ledger_reference.rs
scripts/run_prehardware_core.sh
scripts/run_prehardware_extended.sh
evidence/prehardware/
```

The acceptance matrix and source catalog explain how the supplied SSDD documents were translated into test cases:

```text
docs/validation/verification-matrix.md
docs/validation/source-catalog.md
```
