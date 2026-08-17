# SSDD gem5 reference validation — baseline replay result

**Status:** Completed, simulation-scoped baseline
**Recorded:** 17 August 2026
**Simulator:** gem5 25.1.0.1, X86 optimized build
**gem5 checkout revision:** `3b60ac6`

## Question

Does the portable SSDD reference workload emit the same logical replay result when executed twice under the same gem5 syscall-emulation configuration?

## Configuration

| Parameter | Value |
|---|---|
| CPU model | `TimingSimpleCPU` |
| Memory size | `256MB` (gem5 reports the binary-equivalent `256MiB`) |
| Instruction cache | `32kB` (`32KiB` after gem5 normalization) |
| Data cache | `32kB` (`32KiB` after gem5 normalization) |
| Workload structure | Five logical stages, seven engines, 35 operations |
| Execution mode | X86 syscall emulation, using gem5's retained legacy `se.py` example configuration |
| Repetitions | Two independent simulator invocations with the same inputs |

## Result

Both runs emitted an identical summary:

```text
stages=5 engines=7 operations=35
replay_digest=ff05ec2371488ba1
validation=accepted
```

The two summaries matched exactly. Each run exited at simulated tick `308777000`.

## Interpretation

This baseline demonstrates **repeatability of the selected reference workload** for the fixed compiler, gem5 revision, configuration, and inputs used here. It establishes a reproducible logical-trace fixture for later experiments involving memory timing, controlled delays, or fault injection.

> This is not hardware validation, CXL traffic validation, a physical-performance measurement, a security certification, or a production-readiness result. The workload is a research fixture, not the SSDD product implementation.

## Reproduction artifacts

| Artifact | Location |
|---|---|
| Reference workload | [`simulation/gem5/ssdd_reference_workload.cpp`](../../simulation/gem5/ssdd_reference_workload.cpp) |
| Runner | [`scripts/run_gem5_baseline.sh`](../../scripts/run_gem5_baseline.sh) |
| Run-one summary | [`evidence/gem5/rerun-2026-08-17/baseline-run-one.summary`](../../evidence/gem5/rerun-2026-08-17/baseline-run-one.summary) |
| Run-two summary | [`evidence/gem5/rerun-2026-08-17/baseline-run-two.summary`](../../evidence/gem5/rerun-2026-08-17/baseline-run-two.summary) |
| Result inventory | [`evidence/gem5/rerun-2026-08-17/SHA256SUMS`](../../evidence/gem5/rerun-2026-08-17/SHA256SUMS) |

## Next experiments

The next validation step is to vary a defined model parameter—such as memory latency or a deliberately injected ordering fault—while retaining the same canonical trace and reporting both the configuration difference and the resulting logical evidence. No model-scoped result should be generalized to a physical HC-CXL implementation without separate empirical work.
