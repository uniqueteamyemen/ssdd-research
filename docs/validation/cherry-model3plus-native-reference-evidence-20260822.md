# Cherry Native-Reference Adversarial Package Evidence — 22 August 2026

**Status:** completed, provenance-retained, and checksum-verified native-reference behavioral/integrity execution.

> **Claim boundary.** This package exercised the SSDD native Python, Rust, and compiled reference implementations on a Cherry bare-metal host. It is **not** gem5, KVM, Timing CPU, CXL Type-3, FPGA, physical-CXL, silicon, network, security, production, latency, jitter, throughput, scaling, baseline-versus-SSDD, or overhead evidence.

## Execution identity and provenance

| Field | Recorded value |
|---|---|
| Host | `enjoyed-scorpion` (`84.32.32.40`; retained private address: `10.187.89.34`) |
| Host kernel | `Linux 6.17.0-23-generic x86_64` |
| Remote outer evidence root | `/opt/ssdd-results/cherry-model3plus2/` |
| Remote runner output root | `/opt/ssdd-research/.local-results/cherry-model3plus2/` |
| Local raw retention | `/home/ubuntu/ssdd-research/.local-results/cherry-model3plus2-20260822T085917Z/` |
| Curated repository evidence | `evidence/native-reference/cherry-model3plus2-20260822/` |
| Actual runner exit status | `0` |
| SSDD commit | `b26525e116de025b823d86c3a5976e6d0e118015` |
| Runner SHA-256 | `57a6f5b2727326fda0f037e7c8c62c4d4b2ff5047aa341d6164a85b9270fc1e4` |
| Python reference SHA-256 | `ba1235fc1e8bb6c358dccf480201a2c22e7307d50b1f36374db008adf812ad19` |
| C++ reference workload SHA-256 | `2ec429c1bf77fbadb5b1fabcba8c1aec06b10931b73d32df597b572de128f372` |
| Rust reference SHA-256 | `68cc173ac254008a82658e0a4cac97ca30ecc4b6cf2daf1b91420530dde0fb53` |
| Runtime toolchain | Python `3.12.3`; Rust `1.75.0`; G++ `13.3.0` |

The exact remotely executed command, preserved in the [final provenance record](../../evidence/native-reference/cherry-model3plus2-20260822/final-remote-provenance.txt), was:

```bash
SSDD_RESULTS_DIR=/opt/ssdd-research/.local-results/cherry-model3plus2 \
SSDD_MODEL3_RUN_LABEL=cherry-model3plus2 \
bash /opt/ssdd-research/scripts/run_model3plus_local_campaign.sh
```

`rustc` was absent at initial admission, so the minimal required compiler package was installed before the independent `model3plus2` run. No source checkout, SSH configuration, kernel, reboot, or SimCXL resource was modified. The preserved `model3plus1` launcher failure exited `64` before test execution because its results root lacked the required run-label subdirectory; it remains a separate setup artifact and is not used as test evidence.

## Audited dispositions

The run-level verifier reports an overall `accepted` state. The original `prehardware/*.json` artifacts were then recovered from the remote runner root, copied to the curated evidence directory, and included in the regenerated checksum inventory. The table below uses those retained artifacts directly. Every listed fault remains a **reference-model no-commit/deferred disposition**, not a live process, network, or storage fault injection.

| Package / family | Evidence | Disposition |
|---|---|---|
| Ordering and exact-key collision | `inner/prehardware/ordering.json`, `ordering-chain-stress.json` | 128 arrival permutations and 100×256 full-chain stress preserve deterministic hashes; duplicate and distinct-payload exact four-key collisions are rejected |
| Packet drop | `inner/prehardware/faults.json`, `fault-recovery.json` | rejected with no commit and preserved valid state; checkpoint resumption accepted with equal suffix |
| Node delay | `inner/prehardware/faults.json`, `fault-recovery.json` | rejected/deferred with no commit and preserved valid state; checkpoint resumption accepted with equal suffix |
| Aggregator failure | `inner/prehardware/faults.json`, `fault-recovery.json` | rejected with no commit and preserved valid state; checkpoint resumption accepted with equal suffix |
| Corrupted state ledger | `inner/prehardware/faults.json`, `fault-recovery.json` | rejected with no commit and preserved valid state; checkpoint resumption accepted with equal suffix |
| Ledger tamper | `inner/prehardware/ledger-tamper.json` | all retained tamper fields (`state_hash`, `previous_hash`, `aggregate`, `epoch_id`) detected |
| Deterministic replay | `inner/prehardware/replay-independent.json`, `replay-run-a.json`, `replay-run-b.json` | two 100-epoch runs accepted with equal complete record sequences and final hashes |
| Python/Rust cross-language replay | `inner/prehardware/cross-language.json`, `python-ledger.json`, `rust-ledger.json` | 100 epochs with identical full hash chain and final hash for the retained narrow references |
| Q32 boundary and differential checks | `inner/prehardware/q32.json`, `q32-differential.json` | nine retained boundary/overflow cases pass; 10,000 vectors match the Python integer oracle |
| Compiled proof controls | `inner/proof-accepted.txt`, `inner/proof-corruption.txt` | accepted control passes; record-18 corruption rejects as designed |
| Bounded scale/load | No `scale-load` artifact; `run_model3plus_local_campaign.sh` does not invoke `--mode scale-load` | **not executed** in `model3plus2`; no load/scaling claim is made |
| Cross-domain documentation | campaign plan reference | documented only; not an execution-domain equivalence result |

The included Model 3+ verification output lists its artifact-register subpackage as `pending_hash_generation`; that field is retained verbatim and is **not relabelled as a runner-level acceptance**. Independently, the run emitted `source-register.sha256`, inner and outer `SHA256SUMS`, and `SHA256SUMS.sha256`; remote inner, remote outer, local post-copy, and curated-evidence SHA-256 checks all passed. These distinct facts support artifact integrity of the retained copy but do not rewrite the original verifier’s subpackage field.

## Retained evidence and review captures

The curated directory preserves the exact command, host facts, paths, commits, hashes, launcher stdout/stderr, runner logs, JSON results, compiled proof artifacts, manifests, source register, actual exit status, remote inventories, and local checksum checks.

| Review artifact | Purpose |
|---|---|
| [Live execution provenance PNG](../../evidence/native-reference/cherry-model3plus2-20260822/execution-capture/execution-live.png) | Terminal-derived capture showing host identity, command, process, repository paths, hashes, toolchain, and accumulating artifacts during execution |
| [Completed-result PNG](../../evidence/native-reference/cherry-model3plus2-20260822/completed-result.png) | Terminal-derived capture from the completed launcher log, including accepted package state and proof-corruption rejection |
| [Final remote provenance](../../evidence/native-reference/cherry-model3plus2-20260822/final-remote-provenance.txt) | Exact invocation, host/toolchain facts, numeric exit, remote checksum checks, and inventories |
| [Curated SHA-256 inventory](../../evidence/native-reference/cherry-model3plus2-20260822/SHA256SUMS) | Inventory covering curated files other than the self-referential inventory and its check output |
| [Curated local SHA-256 check](../../evidence/native-reference/cherry-model3plus2-20260822/local-sha256sum-check.txt) | Successful verification of the curated inventory |

The screenshots are deterministic renderings of retained terminal text, not synthetic operational evidence. They assist review but do not replace the text artifacts, manifests, logs, or checksum inventories.

The governing scope and limitation language is retained in [the controlled validation contract](controlled-validation-campaign-20260822.md).
