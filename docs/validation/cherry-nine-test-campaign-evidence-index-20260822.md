# Cherry nine-test campaign evidence index — 22 August 2026

## Scope and evidence rule

This index maps the **nine acceptance IDs** in the controlled verification matrix to the retained Cherry executions that produced their source artifacts. It is an audit navigation record, not a new experiment or a performance claim. The native-reference package and the separate native-reference scale/load package both completed with recorded numeric exit status `0`, remote and local checksum verification, run manifests, command records, and terminal-derived execution and completion captures.[^matrix] [^native] [^scale]

> All nine IDs below are **reference-model evidence**. They do not certify physical CXL, FPGA behavior, KVM full-system performance, NIC bandwidth, distributed fault tolerance, production security, or baseline-versus-SSDD overhead.

## Test-to-evidence map

| ID | Retained Cherry run and primary source artifact | Observed retained outcome | Boundary |
|---|---|---|---|
| ORD-01 | `cherry-model3plus2`; `inner/prehardware/ordering.json` and `ordering-chain-stress.json` | 128 ordering permutations agreed; 256 permutation / 100-epoch stress chains agreed. | Single-process deterministic reference ordering only. |
| ORD-02 | `cherry-model3plus2`; `ordering.json` and `ordering-chain-stress.json` | Prefix collisions sorted; exact four-key duplicates were rejected before commit. | Harness safety rule; not a firmware claim. |
| RPL-01 | `cherry-model3plus2`; `replay-run-a.json`, `replay-run-b.json`, and `replay-independent*.json` | The retained verifier reports equal 100-epoch record sequences and final hashes across independent processes. | Reference serialization, not a complete canonical-CBOR proof. |
| FLT-01 | `cherry-model3plus2`; `faults.json` and `fault-recovery.json` | Packet drop, node delay, aggregator failure, and corrupted state/ledger each produced no commit at epoch 12 and preserved the prior valid state; recovery suffixes were accepted. | Explicit single-process no-commit/deferred model; no live network, process, or storage injector. |
| LED-01 | `cherry-model3plus2`; `ledger-tamper.json` | State hash, previous hash, aggregate, and epoch ID modifications were detected. | Reference audit validator only. |
| XLG-01 | `cherry-model3plus2`; `python-ledger.json`, `rust-ledger.json`, and `cross-language.json` | Python/Rust reference records and chain entries were accepted by the retained cross-language verifier. | Retained minimal Rust reference; no external Rust runtime claim. |
| SCL-01 | `cherry-scale-load1`; `inner/scaling-load.json` points for 8, 16, 32, 64, and 128 logical nodes | Every retained scaling point reported success rate `1.0`, component timings, packet counts, and modeled bytes. | Native-reference wall-clock/model counters, not CXL or fabric performance. |
| LOD-01 | `cherry-scale-load1`; `inner/scaling-load.json` target input points 1k, 5k, 10k, 25k, 50k, and 100k events/s equivalent | Every retained load point reported success rate `1.0`, component timings, event counters, packet counts, and modeled bytes. | Input-generation targets and native-reference observations; not measured network throughput. |
| Q32-01 | `cherry-model3plus2`; `q32.json` and `q32-differential.json` | Nine boundary/overflow/rounding checks and 10,000 differential vectors passed in the retained reference. | Fresh reference implementation because the supplied engine’s `q32_32_core` dependency was unavailable. |

## Provenance and artifact locations

The model/reference run is preserved in [`evidence/native-reference/cherry-model3plus2-20260822/`](../../evidence/native-reference/cherry-model3plus2-20260822/). It includes the command record, host identity and IP record, repository revision, source hashes, compiler and interpreter facts, stdout/stderr, run manifest, exit record, remote and local SHA-256 checks, original JSON artifacts, and execution/completion terminal captures. The scale/load run is preserved separately in [`evidence/native-reference/cherry-scale-load1-20260822/`](../../evidence/native-reference/cherry-scale-load1-20260822/) with the equivalent run-specific provenance and captures.[^native] [^scale]

The supporting evidence notes contain the fuller artifact inventories and checksum scopes. The exact source contract and interpretation boundaries for the IDs are retained in the controlled verification matrix.[^matrix]

## Relationship to the other Cherry evidence

The campaign also retains a KVM-backed full-system SimCXL Type-3 behavioral matrix and a separate syscall-emulation gem5 controlled matrix. Those are distinct experiments with their own manifests and limits; neither is used to inflate or reinterpret the nine reference-model IDs in this index.[^type3] [^controlled]

## References

[^matrix]: [Controlled verification matrix](verification-matrix.md)
[^native]: [Cherry native-reference package evidence](cherry-model3plus-native-reference-evidence-20260822.md)
[^scale]: [Cherry native-reference scale/load evidence](cherry-scale-load-native-reference-evidence-20260822.md)
[^type3]: [Cherry KVM Type-3 evidence](cherry-kvm-full-matrix-evidence-20260822.md)
[^controlled]: [Cherry controlled gem5 evidence](cherry-controlled-gem5-matrix-evidence-20260822.md)
