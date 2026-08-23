# SSDD Comparative Value: Local Policy-Matrix Evidence

**Status:** Completed local semantic/evidence gates; comparative-value conclusion **not yet established**.
**Purpose:** Record the local result honestly before any gem5, SimCXL, or Cherry promotion.

## Execution domains and integrity

| Local execution | Purpose | Result status | Evidence root |
|---|---|---|---|
| Native contract-smoke | Confirm one fixed 133-case contract and required diagnostic fields across the three declared arms. | Completed; interface/evidence-contract gate only. | `evidence/comparative/native-contract-smoke-20260823T161500Z/` |
| Native independent-policy matrix | Run separately coded SSDD, CAS/retry, and single-writer sequencer policy references on the same cases. | Completed; semantic and decision-record result. | `evidence/comparative/native-independent-policy-20260823T163000Z/` |
| Local threaded policy matrix | Exercise concurrent admission/arrival paths, without recording a timing metric. | Completed; semantic and decision-record result. | `evidence/comparative/concurrent-local-policy-20260823T170000Z/` |

Each retained result directory includes its manifest, source/runner provenance, stdout/stderr, results, summary, SHA-256 inventory, and checksum verification. The threaded matrix also produced 18 integrity-checked, arm-blinded reviewer packets for six representative cases; its label key is kept outside the reviewer packet.[1]

## Common case matrix

Every arm received the same 133 cases: one positive control, 128 shuffled arrival permutations, exact conflicting event identity, late source/incomplete set, proof corruption, and candidate-state corruption. The fixed contract required `accepted`, `rejected`, or `deferred` explicitly; rejected/deferred candidates could not publish a referee checkpoint.

| Arm | Accepted | Rejected | Deferred | Arrival permutations | Unique accepted referee-checkpoint hashes |
|---|---:|---:|---:|---:|---:|
| SSDD | 129 | 3 | 1 | 128 | 1 |
| CAS/retry reference | 129 | 3 | 1 | 128 | 1 |
| Single-writer sequencer reference | 129 | 3 | 1 | 128 | 1 |

All three arms retained the required manifest hash, disposition, reason, decision record, checkpoint reference, and prior-valid checkpoint reference for every row.

## What this result establishes

The completed local result establishes that, **for this deliberately bounded reference scenario**, a serious CAS/retry policy and a serious sequencer policy can match SSDD on the declared containment and arrival-permutation semantics. This required each baseline to expose canonicalization as an explicit policy surface:

| Arm | Explicit policy added or exercised in the retained local trace |
|---|---|
| SSDD | Canonical four-field order, exact-key collision treatment, candidate validation, and commit containment. |
| CAS/retry | Versioned admission with retry, then an explicit canonicalized candidate snapshot and validation before publication. |
| Single-writer sequencer | Concurrent enqueue / single writer, then an explicit canonical queue drain and validation before publication. |

This is the correct non-promotional result. It rejects the claim that SSDD is necessary merely because shared state or CXL exists. It also rejects any claim that a serious sequencer cannot achieve the same declared semantic outcome.

## What it does not establish

The local matrices do **not** establish that SSDD is simpler, clearer, faster, lower-overhead, or superior. They are policy references, not a production distributed runtime, a benchmark, physical CXL/FPGA/silicon evidence, a latency/jitter/p95/p99/throughput experiment, or a KVM/SimCXL result. The threaded execution uses scheduling only to exercise admission paths; it records no timing metric.

## Current decision gate

The next valid question is now narrow: can a reviewer determine the material condition, disposition rule, prior valid checkpoint, and policy surface more clearly from one arm’s retained record than from the others under a common task and time budget? The predeclared blinded review protocol answers that question.[2]

Until that review is completed, the only permitted comparative conclusion is:

> **SSDD, CAS/retry with explicit canonicalized candidates, and a single-writer sequencer with explicit canonical queue drain all met the bounded local semantic contract. No comparative-value winner has been established.**

Cherry is not required at this point. It becomes relevant only after a valid reviewer/policy result identifies a narrow claim worth promoting to a separately preregistered gem5 or KVM-to-Timing SimCXL matrix.

## References

[1] [`ssdd-comparative-native-contract-smoke-20260823.md`](ssdd-comparative-native-contract-smoke-20260823.md)
[2] [`ssdd-comparative-human-review-protocol-20260823.md`](ssdd-comparative-human-review-protocol-20260823.md)
[3] [`ssdd-comparative-value-validation-plan-20260823.md`](ssdd-comparative-value-validation-plan-20260823.md)
