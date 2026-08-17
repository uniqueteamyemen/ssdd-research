# Scalable Sovereign Deterministic Design (SSDD)

This repository is the curated **research and validation record** for Scalable Sovereign Deterministic Design (SSDD). It preserves the supplied v1.2 design materials, reference implementations, and reproducible evidence that has been generated to date.

> **Research status.** SSDD is a prototype-stage systems architecture. The records in this repository support only the behavior of their named reference models, scripts, compiler settings, and simulator configurations. They do **not** establish hardware timing, CXL behavior, distributed-cluster fault tolerance, security certification, product readiness, or production performance.

## Repository map

| Path | Contents | Intended use |
|---|---|---|
| `docs/source/` | Canonical supplied v1.2 specification, code design, implementation manual, and prototype roadmap | Primary design record |
| `docs/validation/` | Source catalog, acceptance matrix, gem5 plans, and written result records | Scope, method, and interpretation |
| `reference/python/` | Supplied Python engine reference and retained pre-hardware harness | Readable reference behavior |
| `reference/rust/` | Minimal retained Rust implementation of the documented ledger rule | Independent reference comparison only |
| `simulation/gem5/` | gem5 workload and controlled syscall-emulation configuration | Model-scoped simulator experiments |
| `scripts/` | Reproducible experiment entry points | Re-run named validation paths |
| `evidence/` | Machine-readable generated result records and summarized gem5 output | Evidence audit, not performance certification |

## Current evidence, with boundaries

The retained pre-hardware reference suite records canonical ordering checks, 100-epoch replay comparison, fault-containment control-flow cases, ledger-tamper detection, a Python-to-Rust reference-chain comparison, Q32.32 edge cases, and native reference scaling/load measurements. The precise inputs, observed outcomes, and interpretation boundaries are documented in [`docs/validation/prehardware-results.md`](docs/validation/prehardware-results.md).

The gem5 materials model a selected x86 syscall-emulation workload and a controlled memory-latency configuration. They are **simulation-only artifacts**. See [`docs/validation/gem5-validation-plan.md`](docs/validation/gem5-validation-plan.md) and [`docs/validation/gem5-controlled-matrix-results.md`](docs/validation/gem5-controlled-matrix-results.md).

## Reproduce the retained reference suite

The native reference harness requires Python 3. The extended path additionally requires a Rust compiler. Run the scripts directly from this repository root; generated output is written to `.local-results/` by default, leaving the committed result records under `evidence/` unchanged.

```bash
./scripts/run_prehardware_core.sh
./scripts/run_prehardware_extended.sh
```

The gem5 scripts intentionally require a separate compatible gem5 checkout and do not bundle gem5 itself:

```bash
export GEM5_ROOT=/path/to/gem5
./scripts/run_gem5_baseline.sh
./scripts/run_gem5_controlled_matrix.sh
```

Committed JSON and CSV files under `evidence/` are retained result records from the stated experiment scope; they are not synthetic benchmark data or hardware benchmarks.

## Cross-language note

No Rust implementation or Cargo manifest was present in the supplied SSDD source set. `reference/rust/prehardware_ledger_reference.rs` is therefore a **small independent reference**, created solely to exercise the documented SHA-256 ledger construction against the retained Python reference. It is not a substitute for, nor evidence about, a future SSDD Rust runtime.

## Contribution and claim policy

Contributors should preserve source provenance, record every input/configuration change, and attach machine-readable output for every new public result. Any result must name its execution context and must not be generalized beyond the scope of the test. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`SECURITY.md`](SECURITY.md) before opening an issue or submitting a change.

## License and access

All rights are reserved unless an explicit written license is added by the repository owner. This repository is released as a **private** research record. Do not redistribute source documents, artifacts, or derived claims without authorization.
