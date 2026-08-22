# Cherry native-reference scale-load evidence — 22 August 2026

## Decision and scope

**Status:** Completed, checksum-verified, and retained as a **native-reference wall-clock model check only**. The run establishes that the pinned Python reference accepts its declared scaling and offered-load schedules on the retained Cherry host. It does **not** establish KVM, gem5, CXL Type-3, FPGA, silicon, NIC, distributed-convergence, production, baseline-versus-SSDD, p95/p99, jitter, or hardware-performance results.

> The source result explicitly states: “Wall-clock values and modeled byte counts are reference-model measurements, not NIC bandwidth, distributed convergence, or hardware timing.”

## Reproducibility identity

| Field | Retained value |
|---|---|
| Run label | `cherry-scale-load1` |
| SSH target / host | `84.32.32.40` / `enjoyed-scorpion` |
| Host OS and kernel | Ubuntu 24.04.4 LTS; Linux `6.17.0-23-generic` x86_64 |
| Started | `2026-08-22T09:06:19Z` |
| Exact command | `SSDD_RESULTS_DIR=/opt/ssdd-research/.local-results/cherry-scale-load1 python3 /opt/ssdd-research/reference/python/prehardware_reference.py --mode scale-load` |
| SSDD repository / commit | `/opt/ssdd-research` at `b26525e116de025b823d86c3a5976e6d0e118015` |
| Reference source / SHA-256 | `reference/python/prehardware_reference.py`; `ba1235fc1e8bb6c358dccf480201a2c22e7307d50b1f36374db008adf812ad19` |
| Interpreter / SHA-256 | `/usr/bin/python3.12`, Python 3.12.3; `1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118` |
| Actual outer exit status | `0` |
| Remote and local integrity checks | Passed; source inventories and check logs are retained |

The complete curated evidence package is [`evidence/native-reference/cherry-scale-load1-20260822/`](../../evidence/native-reference/cherry-scale-load1-20260822/). The uncurated local capture is `/home/ubuntu/ssdd-research/.local-results/cherry-scale-load1-20260822T090729Z/`. Both contain manifests, exact stdout/stderr, the original JSON, exit status, provenance, and SHA-256 inventories.

## Accepted source outputs

The original [`scaling-load.json`](../../evidence/native-reference/cherry-scale-load1-20260822/inner/scaling-load.json) contains 11 accepted points, each with `epoch_success_rate: 1.0`. The five scaling points use 25 epochs; the six offered-load points use 50 epochs.

| Category | Declared schedule | Accepted result retained |
|---|---|---|
| Logical-node scaling | 8, 16, 32, 64, 128 logical nodes | all five points accepted; modeled packets/epoch rise from 32 to 512 |
| Offered-load schedule | 1,000, 5,000, 10,000, 25,000, 50,000, 100,000 target input events/s | all six points accepted; each is a bounded native-reference measurement |
| Source JSON status | 11 points | `accepted` |

For audit rather than inference, the JSON reports native-reference timing means for the scaling points from `12.152` μs at 8 logical nodes to `177.625` μs at 128 logical nodes, and for the offered-load points from `1.274` μs at target 1,000 input events/s to `33.085` μs at target 100,000 input events/s. These values are preserved **only** in their declared reference-model domain. They must not be relabeled as device latency, network throughput, CXL latency, production capacity, tail latency, or a comparison against SSDD.

## Evidence inventory and visual companions

| Item | Retained path | Purpose |
|---|---|---|
| Outer manifest and logs | `outer/run-manifest.txt`, `outer/stdout.log`, `outer/stderr.log`, `outer/exit-status` | exact command, environment, outputs, and actual exit |
| Original result | `inner/scaling-load.json` | 11 declared source points and acceptance states |
| Remote and local collection evidence | `provenance/remote-integrity-and-exit.txt`, `provenance/final-remote-provenance.txt`, `provenance/local-collection-audit.txt`, `SHA256SUMS` | source identity, remote/local integrity verification, and file inventory |
| Execution capture | `provenance/execution-live.png` and `provenance/remote-provenance.txt` | launch-time provenance context; not proof of an in-flight process because the short run had already finished when inspected |
| Completion capture | `screenshots/completed-result.png` plus `screenshots/visual-review.md` | readable visual companion showing completed state, exit `0`, manifests, hashes, and JSON acceptance |

The two PNGs are deterministic terminal renderings of preserved text. They supplement, but never replace, the raw logs and inventories. The visual-review record explicitly prevents the launch-time capture from being overstated as live-process proof.

## Claim boundary

This is a completed component of the native-reference testing branch. It closes the missing `scale-load` mode from `model3plus2`, but it does not close the separate KVM full-system baseline, performance, CXL Type-3 performance, governance-ablation, or hardware gates. Those tests require their own declared controls, instrumentation, and evidence before execution or interpretation.
