# SSDD Comparative Value: Blinded Diagnostic and Policy Review Protocol

**Status:** Planned human-review gate. It is not an executed score or a comparative conclusion.
**Purpose:** Test the engineering question that automated acceptance/rejection rows cannot answer: which policy record lets an engineer understand and audit the committed, rejected, or deferred outcome with the least ambiguity for this fixed scenario?

## Why this review is required

The local contract matrices may show that SSDD, a canonicalized CAS/retry implementation, and a canonical-drain sequencer can all preserve the required state semantics. That is evidence against assuming SSDD is automatically necessary. It does not decide diagnostic clarity or policy compactness: those claims require a common reviewer task and an explicit inventory of policy decisions.

## Blinding and materials

Prepare one evidence bundle for each arm/case pair. Replace the arm label with `A`, `B`, or `C`; retain the mapping outside the reviewer packet. Every bundle must contain only its manifest excerpt, decision record, disposition/reason, checkpoint or prior-valid checkpoint reference, and policy inventory excerpt. Do not hide a required record to make an arm look worse.

Use the same bundle set for every reviewer and randomize the order. A reviewer must not be told which label is SSDD, CAS/retry, or sequencer until responses are locked.

## Fixed reviewer task

For each assigned bundle, the reviewer has the same maximum time budget and answers:

| Question | Objective scoring key |
|---|---|
| Was a new checkpoint published? | `accepted` versus `rejected/deferred`. |
| What precise rule caused the disposition? | Normalized `reason` field. |
| Which event or condition was material? | The affected event/key/missing-set field in the decision record. |
| What is the last valid checkpoint reference? | `prior_valid_checkpoint_hash`. |
| What rule would need to change to obtain another disposition? | Named policy surface in the inventory. |

Record answer correctness, elapsed review time, and any uncertainty flag. A score is valid only if the same reviewer task, evidence granularity, terminology, and time budget were applied to all arms.

## Policy-surface review

For each arm, reviewers independently enumerate the minimum explicit policy surfaces needed in the implementation for this scenario. The inventory must distinguish at least: membership completeness, identity/collision handling, ordering, concurrent admission or queueing, late-source treatment, proof/state validation, publication, and recovery/audit reference.

The outcome is qualitative and implementation-specific. Do not declare one arm “simpler” merely because its list has fewer lines. A defensible narrow claim requires agreement that the retained policy description and evidence path are materially easier to inspect for the declared task, with the evidence bundle available for audit.

## Decision rules

| Result | Allowed conclusion |
|---|---|
| All arms meet semantics; reviewers cannot distinguish clarity/compactness materially | SSDD is an alternative policy; do not claim superiority. |
| SSDD improves review accuracy/time or reduces ambiguity while preserving full evidence | For this fixed implementation and task, SSDD provided a clearer retained containment path. |
| CAS/retry or sequencer matches/improves the review result with equal/fewer independent policies | Do not market SSDD as clearer or simpler for this scenario. |
| Any arm lacks an essential record or the blind is broken | Mark the review invalid; repair the evidence protocol and repeat. |

No performance conclusion follows from this review. A separate preregistered concurrent/KVM-to-Timing campaign is needed for performance cost or overhead.
