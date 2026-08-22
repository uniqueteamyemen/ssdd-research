# Cherry Controlled gem5 Matrix Evidence — 22 August 2026

**Status:** completed and checksum-verified model-scoped simulation.

> **Claim boundary.** This is a one-process x86 gem5 syscall-emulation run using `TimingSimpleCPU`, `SimpleMemory`, and a selected model-latency input. It is **not** a KVM full-system measurement, a CXL Type-3 configuration, FPGA evidence, physical-hardware evidence, or a baseline-versus-SSDD performance comparison.

## Execution identity

| Field | Recorded value |
|---|---|
| Remote run root | `/opt/ssdd-results/cherry-controlled-matrix1/gem5-controlled-matrix/` |
| Local raw retention | `/home/ubuntu/ssdd-research/.local-results/cherry-controlled-matrix1-20260822T083500Z/` |
| Curated repository evidence | `evidence/gem5/cherry-controlled-matrix1-20260822/` |
| Runner exit status | `0` |
| SimCXL commit | `edddc2054bcdafdc7537b20c99605f2181bda9dc` |
| SSDD source commit | `b26525e116de025b823d86c3a5976e6d0e118015` |
| gem5 binary SHA-256 | `1611313b15f741cc70cdabab1aedcef4d1c7163a5436f1bcb087ccaf21b5615f` |
| Runner SHA-256 | `ee32d98c1fd1b45a6f00cc8e71f77a4cc0db33c30b5addbe5d95d59c516c1406` |
| Workload source SHA-256 | `2ec429c1bf77fbadb5b1fabcba8c1aec06b10931b73d32df597b572de128f372` |
| Configuration SHA-256 | `ebdda4fa45da12d2fb6375c9d40d450ca589d872ba20dacb35c212889eacb956` |

The launcher fixed all run inputs and explicitly recorded `execution_domain=syscall-emulation-gem5` and `scope=model-specific-functional-and-timing-sensitivity-only` in the retained manifest. The configuration constrains the execution to one reference process and one reference CPU; it rejects non-`SimpleMemory` configurations and explicitly states that it is not a CXL or hardware-validation configuration.[^config]

## Audited results

The matrix completed **21 runs**, each with `gem5_exit=0`. Both remote `sha256sum -c SHA256SUMS` and the post-copy local verification passed for the retained `simout`, summaries, ticks, stats, configuration, matrix, and manifest artifacts.

| Test family | Runs | Observed disposition | Reproducibility evidence |
|---|---:|---|---|
| Latency sensitivity at 10 ns | 2 | accepted | Same replay digest `ff05ec2371488ba1`, reference digest, memory-probe digest, and `sim_ticks=1067650932` |
| Latency sensitivity at 50 ns | 2 | accepted | Same accepted semantics and `sim_ticks=1361453364` |
| Latency sensitivity at 100 ns | 2 | accepted | Same accepted semantics and `sim_ticks=1728706404` |
| Fixed 50 ns replay | 5 | accepted | All five runs carry the identical replay/reference/probe digest trio and `sim_ticks=1361453364` |
| Fault disabled at 50 ns | 2 | accepted | Both controls reproduce the canonical digest tuple |
| Generic proof corruption at record 18 | 2 | rejected as designed | Both retain replay digest `c169add06c40191c` while the reference digest remains `ff05ec2371488ba1` |
| Proof corruption at records 1, 18, 35 | 6 | rejected as designed | Each position repeats its rejection deterministically; replay digests are respectively `3fe63d3143fdc98c`, `c169add06c40191c`, and `ec824874337849a5` |

The selected 10 ns, 50 ns, and 100 ns model inputs yield different simulated tick totals while preserving accepted state semantics. Those totals describe only this fixed model and workload; they are not wall-clock latency, throughput, jitter, p95/p99, CPU overhead, memory overhead, physical memory latency, or CXL behavior.

The proof-corruption cases establish only that the reference validator deterministically rejects the selected one-bit proof mutation at the three tested record positions. They do not establish coverage of other adversarial families, ordering failures, races, network faults, cryptographic attacks, or another implementation.

## Retained artifacts

The curated evidence includes the [matrix CSV](../../evidence/gem5/cherry-controlled-matrix1-20260822/matrix.csv), [run manifest](../../evidence/gem5/cherry-controlled-matrix1-20260822/run-manifest.txt), [SHA-256 inventory](../../evidence/gem5/cherry-controlled-matrix1-20260822/SHA256SUMS), [remote checksum result](../../evidence/gem5/cherry-controlled-matrix1-20260822/remote-sha256sum-check.txt), [local collection audit](../../evidence/gem5/cherry-controlled-matrix1-20260822/local-collection-audit.txt), and each retained per-run `simout`, `summary`, `sim_ticks`, `stats.txt`, and `config.ini` listed in [ARTIFACTS.txt](../../evidence/gem5/cherry-controlled-matrix1-20260822/ARTIFACTS.txt).

[^config]: [Controlled syscall-emulation configuration](../../simulation/gem5/controlled_se.py). The governing campaign contract is [controlled-validation-campaign-20260822.md](controlled-validation-campaign-20260822.md).
