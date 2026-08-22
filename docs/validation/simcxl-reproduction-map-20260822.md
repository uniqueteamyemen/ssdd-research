# SSDD SimCXL Reproduction Map — 22 August 2026

**Purpose.** This record separates local provenance from owner-supplied authenticated Cherry shell evidence. It is a reproduction map, not a performance result, hardware claim, or evidence of a completed KVM run.

## Repository and resource provenance

| Component | Verified location | Immutable identity / SHA-256 | Status |
|---|---|---|---|
| SimCXL source, local | `/home/ubuntu/simcxl-ssdd` | `edddc2054bcdafdc7537b20c99605f2181bda9dc` | Clean checkout of `TianheMICALab/SimCXL` |
| SSDD source, local | `/home/ubuntu/ssdd-research` | `b26525e116de025b823d86c3a5976e6d0e118015` | Local orchestration checkout |
| SSDD source, Cherry | `/opt/ssdd-research` | Remote HEAD not yet captured | The runner and Type-3 adapter were observed in an authenticated shell transcript; a claimed `1717e0…` commit remains unverified until `git rev-parse HEAD` is recorded from that checkout |
| SimCXL source, Cherry | `/opt/simcxl-ssdd` | `edddc2054bcdafdc7537b20c99605f2181bda9dc` | Observed in authenticated shell transcript |
| Simulator binary, local | `/home/ubuntu/simcxl-ssdd/build/X86/gem5.opt` | `009b626a264ec99bc248c332cbcd16b71c35e6908226da6e39141955a738efd8` | Present and executable |
| Simulator binary, Cherry | `/opt/simcxl-ssdd/build/X86/gem5.opt` | N/A | Observed as **MISSING**; must be built on-host |
| CXL-aware kernel, local | `/home/ubuntu/simcxl-resources/vmlinux` | `4829b32d218af2434e2458c97565ad41f5669c8043d498c63cd9adce45c62b00` | Present, 38,057,208 bytes |
| Guest disk image, local | `/home/ubuntu/simcxl-resources/parsec.img` | `74fd8f1383f39a5b5749178ced58b3496718199fa41ea672ae506c558281f904` | Present, 25,769,803,776 bytes |
| Type-3 adapter | `simulation/cxl/simcxl_type3_ssdd.py` | `1c1f6b5022c3d43ebe4efb7bad3314dc2ed3884aa3189f58047b9e6dfe6fb6a4` in the local checkout | Present locally and observed at `/opt/ssdd-research/...` on Cherry |
| Matrix runner | `scripts/run_simcxl_type3_matrix.sh` | `5a3cf30f3d71fdf8df8904449436406870498e96d4ff8faff6028f37f8fa7f64` in the local checkout | Present locally and observed at `/opt/ssdd-research/...` on Cherry |

> The owner supplied the Cherry shell transcript for the two `/opt` source paths and the missing `gem5.opt`. No SSH retry, BMC action, server redeployment, SSH configuration change, or key change is implied or performed by this record.

## Access status

The owner subsequently supplied evidence of an existing `tmux` session named `simcxl-build` and `/tmp/simcxl-build.log`, showing that a SimCXL build had been started and had reached gem5's interactive `pre-commit` continuation prompt. A continuation keystroke was sent to that session. The iKVM connection then disconnected again with WebSocket code `1006`. Therefore the state of that build is **unknown, not failed**. Do not reconnect iKVM or launch a second build; inspect the named `tmux` session and its log only after a separately authenticated shell is available.

## Reproduction contract

The campaign runner requires `SIMCXL_ROOT`, `SIMCXL_KERNEL`, and `SIMCXL_DISK`. It blocks by default if `/dev/kvm` is unavailable. Its exception `SSDD_ALLOW_ATOMIC_BOOT=1` is only a behavioral fallback and is not admissible for latency, percentiles, jitter, throughput, baseline comparison, or scaling claims.

The Type-3 adapter uses an x86 `SimpleSwitchableProcessor`: it boots with KVM, handles the first exit event by switching to `Timing` CPU, emits `SSDD_TIMING_CPU_ROI_BEGIN`, calls `m5 resetstats`, runs the NUMA-bound workload, calls `m5 dumpstats`, emits `SSDD_TIMING_CPU_ROI_END`, and exits. This is the required evidence boundary for any admitted simulation-performance measurement.

## Local retained execution evidence

The retained controlled run at `ssdd-research/.local-results/controlled-campaign/controlled-20260822T034500Z/simcxl-type3` used the local executable and the pinned kernel and disk above. Its saved command lines show `--boot-cpu=atomic` for all five cells, although the configured post-boot switch and ROI markers are present. The five outcomes were: accepted DRAM control, accepted CXL ASIC, rejected CXL ASIC proof corruption, accepted CXL FPGA model, and accepted interleave. These are **functional and behavioral** results only. They do not admit latency, percentile, jitter, throughput, overhead, baseline-comparison, scaling, or recovery-time claims because the host KVM preflight in the same controlled run recorded both `/dev/kvm` and `vmx`/`svm` as absent.

No `run-manifest.txt` or per-run checksum file was retained with that older Type-3 output. The current runner now generates `run-manifest.txt` and `SHA256SUMS`; a future KVM-admitted run must retain both.

## Newly completed local reference smoke

At `2026-08-22T06:54:06Z`, the current `simulation/gem5/ssdd_reference_workload.cpp` was compiled locally with `g++ -O2 -std=c++20` and executed in two deliberately bounded cases. The accepted case (`--fault=none`) returned exit code `0`; the controlled proof-corruption case (`--fault=proof-corruption --fault-record=18`) returned its expected rejection exit code `2`. The complete binary, standard output, standard error, manifest, and SHA-256 file are retained in `ssdd-research/.local-results/reference-smoke-20260822T065406Z`.

This is a **fresh functional reference-workload test**. It is not a SimCXL full-system run, it does not use Cherry, and it supports no timing, throughput, latency, percentage, or hardware claim.

## Required order on Cherry

| Gate | Required operation | Acceptance condition | Stop condition |
|---|---|---|---|
| 1. Host admission | Run the non-destructive KVM probe or its exact predicates: readable/writable `/dev/kvm` and `vmx` or `svm` in CPU flags. | Both predicates are true. | Record blocked result and end the performance branch. |
| 2. Build readiness | Check `python3`, `scons`, compiler, and required development libraries; install only missing documented build dependencies if approved by the active campaign scope. | Dependencies are present. | Do not substitute an unverified binary. |
| 3. SimCXL build | From `/opt/simcxl-ssdd`, run `scons build/X86/gem5.opt -j8`; then SHA-256 the output. | Executable `build/X86/gem5.opt` exists and its hash is retained. | Preserve compiler log and record failure. |
| 4. Resource staging | Transfer the kernel and disk through an approved channel and compare SHA-256 against the values above before use. | Both hashes match exactly. | Do not launch with a mismatched resource. |
| 5. KVM/Timing smoke | Run the limited runner with KVM boot. | Guest boots, explicit Timing-CPU ROI markers appear, stats are produced. | No performance campaign on Atomic CPU. |
| 6. Measurement campaign | Run only admitted matrix cells, with immutable per-cell manifests, raw stats, logs, and checksums. | All planned gates remain satisfied. | Stop at timebox or on an evidence-gate failure. |

## Build command confirmed by SimCXL documentation

```bash
cd /opt/simcxl-ssdd
scons build/X86/gem5.opt -j8
sha256sum build/X86/gem5.opt
```

This is the Type-3 Classic build target documented by the upstream SimCXL project. The concurrency is deliberately capped at eight workers to match the provisioned eight physical cores; it can be reduced if the compiler log or host resource check indicates pressure.

## Deferred facts

The following are **not yet evidenced**: KVM device admission on Cherry, dependency availability, successful SimCXL build, kernel and disk transfer to Cherry, resource checksum match on Cherry, KVM guest boot, Timing-CPU transition, ROI statistics, or any SSDD performance result.

## References

[1]: [SimCXL README — Type-3 build and KVM-to-Timing design](https://github.com/TianheMICALab/SimCXL)
[2]: [SSDD bare-metal execution plan](file:///home/ubuntu/ssdd-research/docs/validation/bare-metal-execution-plan-20260822.md)
