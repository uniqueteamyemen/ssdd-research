# SSDD Model 3+ Local Evidence Campaign: Packages A–E

**Status:** planned for local execution; no result is asserted by this plan.  
**Execution boundary:** deterministic software-reference and native compiled-reference behavior only.  
**Excluded by design:** latency, jitter, throughput, overhead, gem5/KVM timing, FPGA, physical CXL Type-3, silicon, network, security, and production claims.

## Purpose

This campaign strengthens the currently supportable SSDD research position through independently retained behavioral and integrity evidence. It deliberately does not attempt to manufacture a quantitative characterization in an environment that has not passed the KVM admission and Timing-CPU measurement gate. Each package maps to the declared invariants in the [adversarial validation plan](adversarial-validation-plan.md) and retains its inputs, tools, outputs, and hashes.

| Package | Objective | Executable local evidence | Acceptance boundary |
|---|---|---|---|
| A — adversarial functional matrix | Challenge canonical ordering, exact collision disposition, modeled fault containment, and deterministic replay. | `ordering.json`, `ordering-chain-stress.json`, `faults.json`, `fault-recovery.json`, and independent replay comparison. | Native reference model only; no distributed-fault or timing claim. |
| B — ledger and proof integrity | Challenge recorded-ledger fields and a separately compiled reference proof workload. | `ledger-tamper.json`, an accepted proof control, and a controlled proof-corruption rejection. | Reference validator/workload only; neither result is CXL evidence. |
| C — cross-implementation replay | Compare independently executed Python and retained Rust reference chains. | Python/Rust full-chain outputs and `cross-language.json`. | Reference-to-reference comparison only; the Rust source is not an external supplied runtime. |
| D — cross-domain sanity | Preserve the non-transfer rule across reference, simulator, RTL, FPGA, and physical CXL domains. | This table plus the campaign manifest. | A pass in any one domain establishes nothing in another domain. |
| E — artifact register | Make the run auditable and non-overwriting. | Run manifest, source register, all-output SHA-256 inventory, and self-hash. | The register establishes provenance of the retained files, not correctness beyond the declared checks. |

## Cross-domain claim boundary

| Domain | Current status after this local campaign | Claim allowed from this campaign | Claim prohibited from this campaign |
|---|---|---|---|
| Native reference | Executed only when the retained run is accepted. | Declared ordering, ledger, replay, and modeled fault dispositions. | Hardware, distributed runtime, CXL, security, or performance behavior. |
| Native compiled workload | Executed only as a reference proof-control harness. | The defined proof mutation is rejected by that compiled workload. | gem5, memory-system, CXL, or physical-device behavior. |
| gem5 syscall emulation | Not executed by this campaign. | None newly added. | KVM acceleration, Timing-CPU performance, latency, jitter, throughput, or overhead. |
| SimCXL Type-3 | Not executed by this campaign. | None newly added. | Any new emulator calibration, physical CXL, or timing conclusion. |
| RTL simulation | Not executed by this campaign. | None newly added. | FPGA synthesis, timing closure, board, or CXL conclusions. |
| FPGA | Not executed. | None. | Any FPGA implementation or hardware-validation claim. |
| Physical CXL Type-3 | Not executed. | None. | Any physical CXL performance or compatibility claim. |

## Required execution and retention procedure

The runner creates a fresh directory beneath `.local-results/` and refuses to overwrite an existing directory. Before it runs, it records the repository commit, dirty-state marker, tool versions, host identity, `/dev/kvm` availability, and affirmative exclusions for performance, hardware, and external access. It then executes the reference core suite, two independently created replay files, the retained Rust comparator, and native proof-control cases. A separate verifier enforces named dispositions before the hash inventory is generated.

> A local run is **accepted** only when its positive controls pass, its defined negative cases reject as designed, its independent replay compares equal, and its artifact register is retained. A result is never reclassified as performance evidence because it was fast, nor as CXL or hardware evidence because a related source file is present.

## References

[1]: [Adversarial validation plan](adversarial-validation-plan.md) — declared invariants and minimum negative-case matrix.  
[2]: [Verification matrix](verification-matrix.md) — acceptance rules and existing reference-suite boundaries.  
[3]: [Pre-hardware baseline release](prehardware-baseline-release.md) — frozen baseline and non-overwrite rule.  
