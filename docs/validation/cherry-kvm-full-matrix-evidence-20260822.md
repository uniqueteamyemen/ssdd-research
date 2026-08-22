# Cherry KVM Full SimCXL Type-3 Matrix Evidence — 22 August 2026

**Status:** Completed and audited as a five-cell full-system **SimCXL/gem5 behavioral matrix**. This record is intentionally evidence-bounded. It records an admitted KVM-to-Timing execution path and expected functional outcomes; it does **not** report a benchmark or physical-device result.

## Scope and claim boundary

The run exercised the pinned SSDD Type-3 configuration with copied guest images in five declared memory/fault cells on the active Cherry bare-metal host. It used `boot_cpu=kvm`, then the configuration switched the processor to a Timing CPU on the first exit event before the guest-delimited region of interest. The runner retained raw `simout`, `summary`, `m5out/config.ini`, and `m5out/stats.txt` artifacts per cell.[^runner] [^config]

> This is **not** evidence of physical CXL Type-3 hardware, an FPGA implementation, FPGA timing closure, silicon behavior, production deployment, or real CXL latency. The `cxl-fpga` row denotes only the declared **simulator mode**. This one-pass matrix also does not support latency, p95/p99, jitter, throughput, scaling, baseline-comparison, or overhead claims.

## Preserved execution evidence

The remote artifact root remains `/opt/ssdd-results/cherry-kvm-matrix1/simcxl-type3/` on Cherry. A light, checksum-preserved local evidence copy was collected at `/home/ubuntu/ssdd-research/.local-results/cherry-kvm-matrix1-20260822T073954Z/`; it deliberately excludes the generated `guest.img` files. The retained copy includes the launcher log, runner/config source snapshots, `matrix.csv`, `run-manifest.txt`, `SHA256SUMS`, every per-case summary and `simout`, plus each case's `m5out/config.ini` and `m5out/stats.txt`.

| Provenance item | Verified value |
|---|---|
| Cherry host / kernel | `enjoyed-scorpion` / `6.17.0-23-generic` |
| SimCXL commit | `edddc2054bcdafdc7537b20c99605f2181bda9dc` |
| SSDD commit on Cherry | `b26525e116de025b823d86c3a5976e6d0e118015` |
| SimCXL worktree status | `0 modified-paths` at collection |
| SSDD worktree status | `0 modified-paths` at collection |
| gem5 binary SHA-256 | `1611313b15f741cc70cdabab1aedcef4d1c7163a5436f1bcb087ccaf21b5615f` |
| Kernel SHA-256 | `4829b32d218af2434e2458c97565ad41f5669c8043d498c63cd9adce45c62b00` |
| Source disk SHA-256, before / after | `74fd8f1383f39a5b5749178ced58b3496718199fa41ea672ae506c558281f904` / identical |
| Type-3 configuration SHA-256 | `1c1f6b5022c3d43ebe4efb7bad3314dc2ed3884aa3189f58047b9e6dfe6fb6a4` |
| Guest workload SHA-256 | `4c676266d6cfe60ecba8bfb81669f4da511ae2c8333630d76165813f42a1307b` |
| CPU / disk staging in manifest | `boot_cpu=kvm`; `disk_staging=copied` |

The remote verification command `sha256sum -c SHA256SUMS` reported `OK` for all five summaries, `matrix.csv`, and `run-manifest.txt`. The source disk's before/after SHA-256 equality and `disk_staging=copied` establish that the pinned source disk was not staged in place.

## Matrix outcomes

| Case | Memory mode | Injected condition | Guest exit | Validation | Replay / reference digest | gem5 exit |
|---|---|---|---:|---|---|---:|
| `dram-control` | `dram-control` | none | 0 | accepted | `ff05ec2371488ba1` / same | 0 |
| `cxl-asic-accepted` | `cxl-asic` | none | 0 | accepted | `ff05ec2371488ba1` / same | 0 |
| `cxl-asic-proof-corruption` | `cxl-asic` | `proof-corruption`, record 18 | 2 | rejected | `c169add06c40191c` / `ff05ec2371488ba1` | 0 |
| `cxl-fpga-accepted` | `cxl-fpga` | none | 0 | accepted | `ff05ec2371488ba1` / same | 0 |
| `interleave-accepted` | `interleave` | none | 0 | accepted | `ff05ec2371488ba1` / same | 0 |

The proof-corruption rejection is the expected integrity outcome, not a simulator failure. The launcher log ends with `SimCXL Type-3 matrix completed`, the matrix contains all five expected rows, the remote tmux session had exited at collection, and every per-cell `sim_exit` recorded in `matrix.csv` is `0`.

## KVM-to-Timing and ROI evidence

Every case's `simout` records `boot_cpu=kvm`, `roi_cpu=timing-after-first-exit-event`, and the gem5 marker `switching cpus`. Each filtered guest summary contains `SSDD_CXL_NUMA_BEGIN`, `SSDD_CXL_NUMA_END`, `SSDD_TIMING_CPU_ROI_BEGIN`, and `SSDD_TIMING_CPU_ROI_END`. The final Timing CPU `numCycles` counter in the retained `stats.txt` was nonzero in all five cases.

| Case | Final `board.processor.switch.core.numCycles` |
|---|---:|
| `dram-control` | 213,784,591 |
| `cxl-asic-accepted` | 383,046,943 |
| `cxl-asic-proof-corruption` | 384,905,557 |
| `cxl-fpga-accepted` | 104,908,716 |
| `interleave-accepted` | 164,795,548 |

These counters are retained only as proof that the Timing CPU executed after the switch. They are not compared, normalized, or presented as performance measurements. The raw logs also retain gem5's unsupported-MSR warnings; those warnings did not block boot, CPU switching, ROI markers, case completion, or the observed functional result.

## Exit-status caveat and audit decision

The launcher wrapper's `/opt/ssdd-results/cherry-kvm-matrix1/exit-status` file contains the literal text `\0`, not a numeric process status. The cause is an escaping defect in the wrapper's status-write expression. It is therefore **not** used as independent proof of a shell exit code, and it has not been edited after the run. Completion is supported instead by the intact five-row matrix, all per-cell `sim_exit=0` values, the terminal completion line in the launcher log, the fully written manifest/checksum inventory, and the absence of the matrix tmux session at collection.

The matrix is **accepted as controlled full-system SimCXL behavioral evidence with retained KVM-to-Timing execution proof**. It is not accepted as a quantitative performance campaign. A future baseline, scaling, adversarial timing, or overhead result must declare the comparison/control, repetitions, ROI accounting, and claimed metrics in advance and retain the raw artifacts required by the controlled validation contract.[^campaign]

[^runner]: [`scripts/run_simcxl_type3_matrix.sh`](../../scripts/run_simcxl_type3_matrix.sh)
[^config]: [`simulation/cxl/simcxl_type3_ssdd.py`](../../simulation/cxl/simcxl_type3_ssdd.py)
[^campaign]: [`controlled-validation-campaign-20260822.md`](controlled-validation-campaign-20260822.md)
