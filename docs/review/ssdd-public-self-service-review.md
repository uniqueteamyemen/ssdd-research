# SSDD Public Self-Service Comparative Review

**Status:** Open public reviewer workflow.
**What this is:** A bounded blinded review of decision records from SSDD, a CAS/retry policy reference, and a single-writer-sequencer policy reference. It is not a benchmark, product trial, funding request, or vote.

## Why this review exists

The local comparative result has an important limit: under one fixed 133-case shared-state contract, all three policy references met the declared containment and arrival-order semantics once the conventional alternatives explicitly included canonical candidate or queue-drain rules. No winner is claimed.

The remaining engineering question cannot be answered by another automatic hash check:

> When a state is accepted, rejected, or deferred, which retained policy record lets an engineer determine the governing rule, material condition, prior valid checkpoint, and required policy change with the least ambiguity?

Your response may favor SSDD, CAS/retry, a sequencer, or **no meaningful difference**. Each outcome is useful.

## Why this is for a specific technical audience

| Your background | Why it matters in this review |
|---|---|
| Distributed systems / concurrency | You can recognize the real cost of retry, idempotency, late-source, and publication rules rather than treating them as labels. |
| Shared-memory, memory systems, chiplet, or CXL architecture | You can judge whether the record exposes a useful system-level decision boundary without confusing it with a coherence or hardware-performance claim. |
| Systems verification, reliability, or incident analysis | You can assess whether the retained manifest → decision → checkpoint/disposition path would support a post-incident explanation. |
| Systems software / runtime engineering | You can distinguish an explicit operational policy from a simplified toy baseline and identify policy surfaces that must exist in a real implementation. |

This is **not aimed at general engagement**. Familiarity with one or more areas above is requested because the question is about engineering diagnosis and policy design, not brand preference.

## Participate without contacting the owner

1. Download or clone the public repository: <https://github.com/uniqueteamyemen/ssdd-research>.
2. Open `evidence/comparative-review/public-blinded-packet-20260823T170000Z/reviewer-packets/README.md`.
3. Verify the packet locally:

   ```bash
   cd evidence/comparative-review/public-blinded-packet-20260823T170000Z/reviewer-packets
   sha256sum -c SHA256SUMS
   ```

4. Review the eighteen unlabeled records: six cases, each with labels `A`, `B`, and `C`. Do not try to infer the label mapping.
5. Use the public [response template](../../.github/ISSUE_TEMPLATE/blinded-review-response.md) to create an issue directly in GitHub. You do not need to contact the owner or request permission.
6. Submit the issue only after you have answered the same five questions for every packet. The unblinding key remains unpublished until review responses are locked.

## Fixed reviewer task

For every packet, state:

1. Whether a new checkpoint was published.
2. The precise rule that led to the disposition.
3. The material event, key, or condition.
4. The prior valid checkpoint reference.
5. The policy surface that would have to change to produce another outcome.

Also record your elapsed review time and any uncertainty. Do not submit rankings, performance speculation, personal data, confidential work information, or code changes.

## Integrity and fairness controls

The public packet includes per-file SHA-256 values. The label key is intentionally absent. The exact response format, packet set, and decision rule are fixed before unblinding. A response is excluded if it is incomplete, reveals an attempt to unblind labels, or fails the checksum/control procedure.

Any public result will be aggregate and anonymized. It will report the number of completed reviews, exclusions, the bounded task, and one of four outcomes: no material difference, SSDD clearer in scope, a baseline clearer in scope, or invalid/incomplete review. It will not become a generic performance, CXL, hardware, or product claim.

## Evidence scope

The source matrix is a local native policy-reference exercise. It makes no claim about physical CXL, FPGA, silicon, latency, jitter, percentiles, throughput, scaling, production systems, or universal superiority. See [`ssdd-comparative-local-policy-matrix-evidence-20260823.md`](../validation/ssdd-comparative-local-policy-matrix-evidence-20260823.md) for the completed bounded result and [`ssdd-comparative-human-review-protocol-20260823.md`](../validation/ssdd-comparative-human-review-protocol-20260823.md) for the predeclared review rule.
