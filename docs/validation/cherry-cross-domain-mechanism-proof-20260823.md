# Cherry Cross-Domain Mechanism Proof: SSDD Semantic-Commit Containment

**Status:** Completed evidence reconciliation.  
**Purpose:** State the positive mechanism proof already present in the retained Cherry corpus without claiming a comparative advantage over conventional alternatives.

## Core proposition tested across the retained corpus

> Under a declared input and policy, changing a tested execution-path condition must not silently change the accepted semantic result. The system either preserves the canonical accepted result or records a declared contained disposition before an invalid candidate becomes a normal committed state.

This is a systems/application policy evaluation. It is not a claim that CXL coherence is insufficient, nor a latency, jitter, throughput, physical-CXL, FPGA, or production result.

## Completed positive evidence

| Path condition changed or challenged | Execution domain | Retained result | What the result proves | What it does not prove |
|---|---|---|---|---|
| Arrival order of the same 48-packet admitted set | Native reference | 128 shuffled permutations produced one canonical ordered-batch hash. A separate 256-seed, 100-epoch stress run produced one full chain. | The declared canonical key and sort rule made the tested batch/chain independent of those arrival permutations. | General distributed-runtime ordering behavior, network race coverage, or performance. |
| Independent execution/replay | Native reference | Two independently retained 100-epoch replays produced equal full chains. | The declared reference process reproduced the tested chain. | 100 independent replay runs, hardware repeatability, or cross-node consensus. |
| Declared fault conditions | Native reference | Packet drop, node delay, aggregator failure, and corrupted-state-ledger cases were represented as no-commit/deferred cases that preserved the last valid state. | The reference policy’s tested fault model contains those candidate outcomes before a normal new commit. | Real process/network/storage fault injection coverage. |
| Selected model latency input | Controlled syscall-emulation gem5 | 10 ns, 50 ns, and 100 ns inputs produced different `sim_ticks` but the same accepted replay/reference/probe digest tuple. | In the fixed model/workload, the tested semantic result was preserved despite the declared latency input variation. | Physical latency, jitter, p95/p99, throughput, CXL behavior, or timing advantage. |
| Selected proof corruption | Controlled gem5 and full-system SimCXL | Selected proof mutations were rejected as designed; the accepted reference digest remained identifiable. | The tested validator path did not accept those corrupted candidates as normal valid results. | Universal corruption/adversarial coverage or security certification. |
| Declared memory/simulator mode | Full-system Cherry KVM-to-Timing SimCXL/gem5 | Accepted DRAM-control, `cxl-asic`, `cxl-fpga`, and interleave rows retained the same accepted reference digest; the proof-corruption row rejected. Runs 1, 2, and 4 were ROI-closed behavioral executions. | The full-system policy preserved/rejected the tested semantic result across these declared simulator modes after KVM boot and Timing-CPU ROI transition. | Physical CXL/FPGA behavior, a CXL-versus-DRAM speed comparison, or a generic memory-mode invariant. |

## Correct conclusion

The positive evidence already supports this claim:

> **SSDD’s declared semantic-commit containment mechanism was exercised across native reference execution, a controlled TimingSimpleCPU model, and full-system KVM-to-Timing SimCXL behavioral simulation. Under the tested path variations, it preserved the declared accepted canonical result or rejected/contained the declared invalid candidate.**

This is sufficient to state what the mechanism does in its tested domains. It is not sufficient to say that SSDD is better, simpler, lower-overhead, or more diagnostically useful than a strong conventional alternative. That is a separate **comparative-value** question.

## Why the baseline comparison is separate

The completed evidence answers: **“Does SSDD’s mechanism work under the declared changes and failures?”**  
The future comparison answers: **“Does this mechanism provide a clearer, simpler, or otherwise preferable engineering tradeoff than a credible CAS/retry or sequencer alternative for the same task?”**

The first question is answered positively and boundedly by the retained Cherry corpus. The second should not be inferred from it; it requires the planned shared-contract comparison in [`ssdd-comparative-value-validation-plan-20260823.md`](ssdd-comparative-value-validation-plan-20260823.md).

## Evidence references

- [`cherry-controlled-gem5-matrix-evidence-20260822.md`](cherry-controlled-gem5-matrix-evidence-20260822.md)
- [`cherry-kvm-full-matrix-evidence-20260822.md`](cherry-kvm-full-matrix-evidence-20260822.md)
- [`cherry-execution-mode-reconciliation-20260823.md`](cherry-execution-mode-reconciliation-20260823.md)
- [`cherry-measurement-claim-matrix-20260823.md`](cherry-measurement-claim-matrix-20260823.md)
- [`ssdd-comparative-value-validation-plan-20260823.md`](ssdd-comparative-value-validation-plan-20260823.md)
