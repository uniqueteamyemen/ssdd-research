# Cherry KVM Smoke Evidence — 22 August 2026

## Scope and evidence boundary

This record captures a **two-case KVM smoke** executed on the active Cherry bare-metal host. Its purpose was to admit the KVM boot path, verify the configured transition from KVM to the Timing CPU, and confirm the expected SSDD functional outcomes before any performance matrix was considered.

It is **not** a latency, p95/p99, jitter, throughput, scaling, or baseline-comparison result. No performance claim is supported by this smoke.

## Preserved evidence

The compact extraction is retained locally under `/home/ubuntu/ssdd-cherry-kvm-smoke*evidence*`. Remote results are retained beneath `/opt/ssdd-results/cherry-kvm-smoke/simcxl-type3/` on the Cherry host, with one directory per case and the corresponding `m5out`, `config.ini`, `stats.txt`, `simout`, summary, and manifest artifacts.

| Artifact | SHA-256 |
|---|---|
| SimCXL `build/X86/gem5.opt` | `1611313b15f741cc70cdabab1aedcef4d1c7163a5436f1bcb087ccaf21b5615f` |
| Guest kernel `vmlinux` | `4829b32d218af2434e2458c97565ad41f5669c8043d498c63cd9adce45c62b00` |
| Type-3 source configuration | `2ec429c1bf77fbadb5b1fabcba8c1aec06b10931b73d32df597b572de128f372` |
| Generated configuration | `1d7872c9497055ca467525aa7a55b3f31fef893d4bb2bd7372d55e671b40ef86` |
| Guest reference binary | `4c676266d6cfe60ecba8bfb81669f4da511ae2c8333630d76165813f42a1307b` |

## Functional outcomes

| Case | Guest fault mode | Observed functional result | Guest exit |
|---|---|---|---:|
| `cxl-asic-accepted` | none | `validation=accepted` | `0` |
| `cxl-asic-proof-corruption` | `proof-corruption`, record `18` | `validation=rejected` | `2` |

The rejection in the second row is the expected integrity response to a deliberately corrupted proof, not a simulator failure.

## KVM-to-Timing evidence

Both case logs contain `boot_cpu=kvm` and the gem5 transition marker `switching cpus`. The post-transition timing-core statistics record active work in both cases:

| Case | Timing-core busy cycles | Timing-core store accesses | Timing-core integer ALU accesses |
|---|---:|---:|---:|
| `cxl-asic-accepted` | 358,331,179 | 31,900,000 | 163,721,149 |
| `cxl-asic-proof-corruption` | 428,520,864 | 41,148,736 | 191,056,948 |

The KVM logs include documented unsupported-MSR warnings from gem5. They did not prevent the controlled boot, CPU switch, completion, or the expected case outcomes. They must remain in the raw log for reproducibility.

## Admission decision

The KVM boot and Timing-CPU transition gate is **admitted** for the two-case smoke configuration. A subsequent performance campaign must still use independent manifests, repeated runs, and raw `stats.txt`/log retention. It must not generalize the smoke counters as benchmark results.
