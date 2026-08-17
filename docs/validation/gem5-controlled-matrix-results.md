# SSDD Controlled gem5 Matrix — Research Record

**Status:** completed model-scoped simulation artifact.
**Interpretation:** this record reports outcomes from a fixed SSDD reference workload in gem5. It is not a statement about physical hardware, CXL traffic, security certification, fault rates, or production readiness.

## Scope and configuration

The experiment uses the portable SSDD reference workload: five logical stages, seven engines per stage, canonical ordering, a per-record proof, a replay digest, and a memory probe. It runs through gem5 25.1.0.1 in X86 syscall-emulation mode with `TimingSimpleCPU`, 32 kB L1 instruction and data caches, 256 MB memory, and a controlled `SimpleMemory` latency. The workload, compiler, simulator revision, and configuration are held fixed unless a listed variable says otherwise.

| Family | Cases | Observed result |
|---|---:|---|
| Fixed latency | 10 ns, 50 ns, 100 ns; two runs each | All six runs accepted with replay digest `ff05ec2371488ba1` |
| Repeated replay | 50 ns; five runs | All five runs accepted with the same replay digest and memory-probe digest |
| Proof corruption | 50 ns; records 1, 18, 35; two runs per record | All six controlled mutations rejected deterministically |

## Recorded simulated-tick outcomes

| Fixed latency | Simulated ticks per run | Change from 10 ns |
|---|---:|---:|
| 10 ns | 1,346,752,000 | baseline |
| 50 ns | 1,637,792,000 | +291,040,000 (+21.6105%) |
| 100 ns | 2,001,592,000 | +654,840,000 (+48.6236%) |

The simulated-tick figures describe the selected gem5 model and workload. They are **not** a conversion to wall-clock performance, physical memory latency, CXL link behavior, or a performance prediction for a deployed implementation.

## Controlled mutation outcomes

| Mutated trace record | Repeated runs | Validation | Replay digest |
|---|---:|---|---|
| 1 | 2 | rejected | `3fe63d3143fdc98c` |
| 18 | 2 | rejected | `c169add06c40191c` |
| 35 | 2 | rejected | `ec824874337849a5` |

The mutation flips one bit in a generated proof after the canonical trace has been assembled. It demonstrates bounded rejection by the reference validator at the tested positions. It does not establish coverage for untested mutation classes, ordering faults, race conditions, malicious adversaries, cryptographic attacks, or failures in a separate implementation.

## Public-claim boundary

The SSDD specification and implementation materials justify testing deterministic ordering, canonical replay, ledgered evidence, and controlled validation scenarios. The prototype roadmap identifies broader capabilities—including convergence, bounded decision windows, cross-language hash matching, and 1,000-node simulation—as objectives. Therefore, the appropriate public statement is:

> Under the stated gem5 configuration, the SSDD reference workload reproduced an accepted canonical replay across the tested fixed-latency cases and rejected the specified one-bit proof corruptions at three tested trace positions.

No stronger hardware, security, production, HC-CXL, or CXL-compliance statement follows from this record.

## Artifact locations

The retained rerun record is [`evidence/gem5/rerun-2026-08-17/controlled-matrix.csv`](../../evidence/gem5/rerun-2026-08-17/controlled-matrix.csv), with a per-case summary for every run and an inventory in [`SHA256SUMS`](../../evidence/gem5/rerun-2026-08-17/SHA256SUMS). The runner is [`scripts/run_gem5_controlled_matrix.sh`](../../scripts/run_gem5_controlled_matrix.sh); the workload source is [`simulation/gem5/ssdd_reference_workload.cpp`](../../simulation/gem5/ssdd_reference_workload.cpp); and the gem5 configuration is [`simulation/gem5/controlled_se.py`](../../simulation/gem5/controlled_se.py).
