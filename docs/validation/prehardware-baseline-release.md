# SSDD Pre-Hardware Verification Baseline v0.1.1

**Release label:** `prehardware-baseline-v0.1.1`
**Status:** frozen, reproducible research baseline
**Publication scope:** reproducible reference-model and gem5 simulation evidence only

## Purpose

This release freezes the curated SSDD verification baseline in a form suitable for audit. It binds the source record, test definitions, retained machine-readable evidence, written reports, and acceptance outcomes to one annotated Git tag. Subsequent work must use this tag as its comparison point and record every changed input, implementation, configuration, environment, or acceptance rule.

## Publication correction

The historical tag `prehardware-baseline-v0.1.0` is retained unchanged as the first freeze point. Its controlled gem5 configuration used a repository-relative configuration path that was not valid when the runner was executed from a separate gem5 checkout. The active `prehardware-baseline-v0.1.1` tag includes the `GEM5_ROOT` configuration-path correction, the successful rerun record, and the post-tag reference extensions. It is the reproducible baseline for public audit; the earlier tag remains provenance, not the recommended reproduction target.

## Included record

| Record | Repository location | Boundary |
|---|---|---|
| Primary v1.2 source documents | [`docs/source/`](../source/) | Design and implementation source material; not a production-delivery claim. |
| Pre-hardware test definitions | [`docs/validation/verification-matrix.md`](verification-matrix.md) | Defines the named reference checks and acceptance criteria. |
| Reference implementations | [`reference/python/`](../../reference/python/) and [`reference/rust/`](../../reference/rust/) | Python reference plus a narrow independent Rust ledger comparator; not an official Rust runtime. |
| Raw retained pre-hardware evidence | [`evidence/prehardware/`](../../evidence/prehardware/) | Machine-readable output from the stated reference execution scope. |
| gem5 workload and configuration | [`simulation/gem5/`](../../simulation/gem5/) | Syscall-emulation model fixtures; not hardware, CXL, or production evidence. |
| gem5 result records | [`evidence/gem5/rerun-2026-08-17/`](../../evidence/gem5/rerun-2026-08-17/) | Model-scoped retained output from the named simulations, including per-run summaries and a SHA-256 inventory. |
| Supplementary reference evidence | [`evidence/prehardware/postbaseline-extensions-v0.1.0/`](../../evidence/prehardware/postbaseline-extensions-v0.1.0/) | Separate post-tag reference stress and differential records; not an expansion of the claimed system scope. |
| Written outcome reports | [`prehardware-results.md`](prehardware-results.md), [`postbaseline-extension-results.md`](postbaseline-extension-results.md), [`gem5-baseline-results.md`](gem5-baseline-results.md), and [`gem5-controlled-matrix-results.md`](gem5-controlled-matrix-results.md) | Interpretation is limited to the named model, scripts, compiler, and simulator configuration. |

## Acceptance boundary

The baseline records canonical ordering, full replay, bounded reference fault handling, forensic ledger recomputation, independent Python-to-Rust reference comparison, Q32.32 edge behavior, reference scaling/load measurements, and the retained gem5 workload results. It does **not** certify a distributed runtime, official Rust implementation, hardware timing, CXL behavior, physical stress, security resilience, or production readiness.

## Reproduction rule

The committed evidence is retained for audit. New executions must write to `.local-results/` through the scripts under [`scripts/`](../../scripts/), retain their raw output separately, and be committed as a new result record rather than overwriting this baseline.
