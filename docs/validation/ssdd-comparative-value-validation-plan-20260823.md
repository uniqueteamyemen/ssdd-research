# SSDD Comparative Value Validation Plan

**Status:** Planned. No comparative result is reported in this document.  
**Question:** Does SSDD provide a clearer or simpler semantic-commit containment capability than credible conventional alternatives for the same shared-memory engineering problem?

**Relationship to the completed Cherry corpus:** This plan is a future comparative-value/superiority experiment. It is not a prerequisite for, and does not reopen, the completed positive mechanism evidence that SSDD preserves a declared canonical result or contains a declared invalid candidate across the retained reference, controlled gem5, and KVM-to-Timing SimCXL domains.

## 1. Fixed engineering scenario

The comparison uses one bounded task: several producers contribute declared event records to a shared checkpoint. A consumer/system must decide whether to publish the next shared checkpoint. The same admitted event set may arrive in different orders, one producer may be late, an exact event key may collide, an input/proof may be corrupted, or memory access may use one of the declared simulation modes.

The experiment does **not** ask whether CXL is coherent. It asks whether the system makes a predeclared and auditable decision about the shared checkpoint under those inputs.

## 2. Competitor implementations

| Arm | Fair implementation contract | What it may prove | What it may not claim |
|---|---|---|---|
| **A. Arrival-order CAS/retry baseline** | Shared-memory compare-and-swap/retry loop with idempotency keys; apply accepted records in arrival order; define its own retry/timeout behavior. | What a conventional optimistic shared-memory implementation does under the injected cases. | That all conventional systems behave this way. |
| **B. Single-writer sequencer baseline** | One explicit queue/sequencer chooses event order and publishes checkpoints; define failover/retry and proof handling. | A strong conventional ordering alternative. It may match or exceed SSDD semantic outcomes. | That it is inherently inferior because it is centralized. |
| **C. SSDD policy** | Four-field canonical key; collision rejection; canonical batch; declared reduction; state/hash chain; proof/state validation before commit; predeclared reject/defer handling. | Whether the SSDD policy meets its declared semantic-containment contract under the same cases. | That it is universally simpler, faster, or better without comparison results. |

The baseline code must be written as a serious implementation of its stated policy, not intentionally weakened. A baseline that passes all declared semantic, containment, and diagnostic criteria defeats any claim that SSDD is clearer or simpler for this scenario.

## 3. Same input and environment contract

Every arm receives the same versioned input manifest, event payloads, key definitions, producer schedule, fault schedule, seed, initial state, and expected disposition table. The execution domain is recorded separately for:

1. native multi-process software reference;
2. syscall-emulation gem5 model;
3. full-system KVM-to-Timing SimCXL/gem5 behavioral simulation.

No result is transferred from one domain to another. Physical CXL, FPGA, or production claims remain outside this plan.

## 4. Required injections and predeclared outcomes

| Case family | Injection | Required observation for every arm |
|---|---|---|
| Positive control | Same complete admitted event set | Final shared checkpoint, state digest, and disposition. |
| Arrival permutation | 128 shuffled arrivals plus a separate longer-chain stress set | Whether the final semantic result is equal where the arm’s contract says it should be; otherwise the declared differing disposition. |
| Exact key collision | Same four ordering fields with a changed payload/source field | Reject, resolve, or other predeclared behavior; no implicit ambiguity. |
| Late source | One producer crosses the epoch/commit boundary | Explicit accept, reject, defer, or retry outcome and its state effect. |
| Proof corruption | Alter one selected proof field/record | Whether the candidate is rejected before commit or how the baseline’s documented policy treats it. |
| State corruption | Alter the candidate checkpoint before verification/publication | Whether a bad candidate is contained and whether the prior valid checkpoint remains identifiable. |
| Mode variation | DRAM-control, CXL-aware simulator mode, interleave mode, and declared model-latency points | Semantic outcome separately from performance counters; no cross-domain speed inference. |
| Replay | Independent rerun from the same manifest | Reproducibility evidence appropriate to the arm’s declared policy. |

## 5. What would prove value

The campaign does **not** define success as “SSDD passes and a baseline fails.” A credible sequencer can reasonably pass many semantic tests. SSDD earns a narrower value claim only if the retained evidence shows one or more of the following under the same contract:

| Value question | Predeclared evidence | SSDD may claim only if result supports it |
|---|---|---|
| **Containment** | Candidate corruption or incomplete input cannot produce an undocumented new checkpoint; prior valid checkpoint is identifiable. | Its declared policy contained these tested failure cases. |
| **Semantic invariance** | Same admitted set under declared order/mode changes produces the expected same result, or a named disposition. | The tested policy separated semantic outcome from these declared variations. |
| **Diagnostic clarity** | A reviewer can trace input manifest → ordering/decision record → checkpoint/hash → disposition without reconstructing the event history from unrelated logs. | The SSDD artifact path was clearer for these cases. |
| **Policy compactness** | A predeclared count and description of independent ordering, retry, integrity, and commit rules needed by each arm. | SSDD expressed this scenario with fewer or more unified policy surfaces in this implementation—not in all systems. |
| **Performance cost** | Separate KVM-to-Timing campaign with identical workload, ROI, warm-up, repetitions, raw timestamps/counters, and statistical analysis. | Only the measured overhead or latency result; not a generic performance advantage. |

## 6. Falsification rules

The SSDD value proposition fails or is narrowed if any of the following occurs:

1. The SSDD arm produces divergent final state for a same-admitted-set case where its policy requires invariance.
2. A declared corrupted/incomplete candidate becomes a normal committed state without an explicit predeclared disposition.
3. A conventional baseline produces the same containment and diagnostic artifact with equal or fewer policy surfaces for the defined scenario.
4. The baseline contract is ambiguous, incomplete, or intentionally weak; such a result is invalid rather than favorable to SSDD.
5. The experiment mixes reference-model, syscall-emulation, KVM-to-Timing, and physical-domain claims.

## 7. Evidence inventory per cell

For every arm × case × repeat, retain:

- implementation commit, build hash, configuration, and full input/fault manifest;
- CPU mode, execution domain, simulator/memory mode, and ROI markers where applicable;
- raw stdout/stderr, trace, decision/order record, state/checkpoint digest, and disposition;
- pre/post valid-state evidence for negative cases;
- raw timing and counter files only when a separate predeclared performance matrix applies;
- exit status, SHA-256 inventory, and an immutable summary that records `accepted`, `rejected as designed`, `failed`, `timed out`, or `invalid/inconclusive`.

## 8. Current evidence and gap

Cherry evidence already supports bounded SSDD mechanism demonstrations: canonical ordering in a native reference harness, selected no-commit/defer fault behavior, selected proof rejection, timing-sensitivity cases with unchanged accepted digests, and KVM-to-Timing SimCXL behavioral repeats. It does **not** include a credible conventional baseline under the same contract. Therefore it supports the **hypothesis and mechanism**, not the comparative claim that SSDD is simpler or clearer than alternatives.

## 9. Decision after the campaign

| Campaign outcome | Honest conclusion |
|---|---|
| SSDD uniquely meets containment/diagnostic criteria in the fixed scenario | “For this declared scenario and implementation set, SSDD provided the clearest retained semantic-commit containment path.” |
| SSDD and sequencer both meet the criteria | “SSDD is an alternative policy with different architectural tradeoffs; do not claim superiority.” |
| Baseline meets criteria with simpler retained policy surface | “Do not market SSDD as simpler for this scenario; narrow its target problem or revise the mechanism.” |
| SSDD fails an invariant or containment case | “Treat the failure as a design defect or limitation; do not make the value claim.” |

## Related controls

- [`adversarial-validation-plan.md`](adversarial-validation-plan.md)
- [`controlled-validation-campaign-20260822.md`](controlled-validation-campaign-20260822.md)
- [`cherry-measurement-claim-matrix-20260823.md`](cherry-measurement-claim-matrix-20260823.md)
