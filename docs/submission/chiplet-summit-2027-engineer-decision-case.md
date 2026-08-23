# The Engineer’s Decision: Use SSDD or Not?

**Question:** What practical capability does an engineer gain by using SSDD, and what remains unresolved without it?

## The short answer

An engineer uses SSDD when the system must make a **shared semantic decision** from events that can arrive through different paths, under different memory placements, or with some declared integrity failures. SSDD gives that engineer an explicit rule for when a candidate result is allowed to become committed:

> **For the same admitted event set under the declared policy, publish one canonical committed result; otherwise reject or defer the candidate before it changes shared state.**

Without SSDD—or an equivalent application/system policy—the engineer may still have coherent CXL memory and correct interconnect operation. What remains absent is a declared, testable answer to a different question: **did a topology, latency, ordering, or integrity variation change the shared application decision, and if so, was that change allowed?**

## Decision table

| Engineer concern | If the engineer uses SSDD | If the engineer does not use SSDD or an equivalent policy | Evidence status |
|---|---|---|---|
| **Different arrival orders for the same admitted events** | The declared four-field key canonicalizes the batch; exact key collisions are rejected. The engineer can test whether an order change changed the committed result. | Coherence alone does not define an application event order or collision disposition. The team must rely on an implicit or separately designed rule, which may be harder to reproduce and audit. | Native reference: 128 shuffled 48-packet permutations yielded one ordered-batch hash; a 256-seed, 100-epoch chain stress test yielded one full hash chain. |
| **Memory/topology experimentation** | The engineer can change a declared memory mode or modeled latency and separately check semantic preservation: same canonical digest, or a defined reject/defer outcome. | The team can still test performance and functional behavior, but lacks this particular semantic invariant unless it builds an equivalent mechanism. A changed result can be harder to classify as expected application behavior, a race, a bad ordering assumption, or an integrity failure. | Controlled gem5: 10/50/100 ns model inputs had different `sim_ticks` with the same accepted digest tuple. Full-system SimCXL: DRAM-control, `cxl-asic`, `cxl-fpga`, and interleave accepted rows retained the same reference digest. |
| **Proof or state corruption before commit** | The validator can reject the selected candidate, and the declared reference fault cases preserve the last valid state rather than create a normal new commit. | The engineer must implement and test a separate integrity/commit policy. CXL memory coherency does not decide whether an application should accept a corrupted proof or publish a candidate state. | Controlled gem5 and full-system SimCXL: selected proof-corruption cases rejected as designed. Native reference: four declared fault cases are modeled as no-commit/deferred and retain the last valid state. |
| **Root-causing a semantic regression** | The engineer receives a canonical batch hash, reference/replay digest, state/hash chain, and explicit accept/reject disposition. This narrows investigation to a declared input, policy, or implementation deviation. | Logs may still exist, but there is no SSDD-specific canonical decision record tying input order, candidate state, and commit disposition together. | Full-system matrix retains digests, summaries, configs, manifests, and checksum inventories; native reference retains state/hash chains. |
| **Architecture decision gate** | The engineer can make a predeclared gate: “This configuration is acceptable only if it retains the declared semantic result, or fails through the declared containment path.” | The engineer may judge a configuration by latency, bandwidth, coherence, or application tests alone, but not by this explicit semantic-commit gate. | The current evidence demonstrates the gate in bounded reference/gem5/SimCXL simulations only. |

## What the engineer gains in one sentence

**SSDD turns an otherwise implicit question—“did this architecture change the decision, or only the path to it?”—into a concrete acceptance test with a canonical result or a contained failure.**

## What the engineer loses by not using it

The loss is **not** CXL coherency, memory sharing, or basic system correctness. CXL still provides its intended interconnect and coherent-memory capabilities. The loss is a ready-made, explicitly tested policy for:

1. canonicalizing a declared set of events before reduction;
2. rejecting exact-key collisions rather than choosing an accidental order;
3. distinguishing an accepted semantic result from a proof/state failure;
4. preserving a last valid state in the declared no-commit/defer cases; and
5. correlating architecture variation with an auditable semantic outcome.

Without such a policy, the engineer must build an equivalent mechanism or accept that these questions remain application-specific and less directly testable.

## Adoption cost and fit

SSDD is not free and is not required for every CXL workload. Adoption requires the engineer to define the event key, collision rule, epoch/commit boundary, aggregate/reduction policy, and rejection/defer handling. It also introduces ordering, hashing, validation, and artifact-retention work. The current corpus does **not** quantify that overhead.

The policy is most appropriate where several components can influence one shared decision or state transition and where a wrong-but-coherent result would be more costly than a contained rejection. It is less compelling for simple local memory expansion, read-mostly sharing, or workloads with no shared event-to-state transition to govern.

## Evidence boundary

This case is supported by native-reference, syscall-emulation gem5, and full-system KVM-to-Timing SimCXL behavioral evidence. It does not claim physical CXL or FPGA deployment, a production runtime, direct KVM-versus-CXL performance, latency/jitter improvement, consensus, universal fault coverage, or measured adoption overhead.

## Evidence references

- [`cherry-controlled-gem5-matrix-evidence-20260822.md`](../validation/cherry-controlled-gem5-matrix-evidence-20260822.md)
- [`cherry-kvm-full-matrix-evidence-20260822.md`](../validation/cherry-kvm-full-matrix-evidence-20260822.md)
- [`cherry-execution-mode-reconciliation-20260823.md`](../validation/cherry-execution-mode-reconciliation-20260823.md)
- [`cherry-measurement-claim-matrix-20260823.md`](../validation/cherry-measurement-claim-matrix-20260823.md)
