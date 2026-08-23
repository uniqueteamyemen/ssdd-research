# SSDD Comparative Value: Native Contract-Smoke Execution Plan

**Status:** Implemented local harness; execution results must be reviewed separately.
**Purpose:** Establish one auditable problem contract for SSDD, CAS/retry, and a single-writer sequencer before treating any later result as comparative evidence.

## Where it runs first

The first gate runs locally in `/home/ubuntu/ssdd-research`, using the isolated comparison harness at `comparison/ssdd_comparative_harness.py` and runner `scripts/run_ssdd_comparative_native.sh`. It does **not** alter the closed Cherry evidence, use a remote server, require KVM, or imply CXL/FPGA/hardware behavior.

Cherry is a later confirmation environment only. It becomes relevant after all three arms satisfy this shared semantic/evidence contract and a separate concurrent-baseline implementation is ready for a declared gem5 or KVM-to-Timing SimCXL matrix.

## Fixed shared-state problem

Twelve fixed event records contribute integer payloads to one shared checkpoint. Every arm receives the same event manifest and must make one explicit disposition: `accepted`, `rejected`, or `deferred`. A shared referee checkpoint digest covers the final aggregate state and event membership; it is not any arm’s private log or ordering mechanism.

| Case | Contracted condition | Required outcome for every arm |
|---|---|---|
| Positive control | Complete admitted set | `accepted` with one referee checkpoint digest. |
| 128 arrival permutations | Same complete set, shuffled deterministically | `accepted`; one digest across all 128 permutations. |
| Exact event-ID collision | Same event ID with conflicting content | `rejected`; no checkpoint. |
| Late source | One expected event absent at the commit boundary | `deferred`; no checkpoint. |
| Proof corruption | One invalid proof flag | `rejected`; no checkpoint. |
| Candidate-state corruption | Candidate aggregate altered before publication | `rejected`; no checkpoint. |

This is deliberately not a test that tries to make a baseline fail. The common contract requires explicit containment in all three arms.

## Policy arms

| Arm | Local reference implementation | What this first gate can establish | What it cannot establish |
|---|---|---|---|
| SSDD | Canonical four-field ordering, collision rule, declared reduction, and validation before commit. | The current SSDD policy meets the shared contract. | General distributed-system behavior or performance. |
| CAS/retry | Versioned, arrival-order CAS/retry policy reference with explicit idempotency, retry, late-source, validation, and audit rules. | The alternative’s stated policy meets the same semantic contract. | Hardware atomics, contention cost, retry behavior under an OS scheduler, or performance. |
| Single-writer sequencer | Explicit queue and one writer with declared publication, late-source, validation, and audit rules. | A strong conventional ordering alternative meets the same contract. | Availability/failover behavior outside the declared reference policy or performance. |

## Required evidence and scoring boundary

For every arm/case, the harness retains a manifest hash, disposition, reason, decision record, referee checkpoint hash if accepted, and prior-valid checkpoint reference. It also produces a policy-surface inventory. The latter is a **human-review instrument**, not an automatic score: counting rows cannot prove that a policy is simpler.

The automated summary may establish only contract compliance, arrival-permutation invariance under the shared referee digest, and presence of the required diagnostic schema. It must never announce a winner for clarity, compactness, or superiority.

## Gates before a comparative value claim

1. All arms must pass the shared contract without weak or undocumented baseline behavior.
2. A reviewer exercise must assess diagnostic clarity from the retained bundle—manifest → decision record → checkpoint/disposition—using the same questions and time boundary for every arm.
3. A reviewed policy inventory must identify independent ordering, retry, integrity, and commit rules per arm; conclusion wording must remain implementation-specific.
4. A separate concurrent CAS/retry implementation and a preregistered timing matrix are required before any contention, latency, overhead, or performance-cost statement.
5. Only then should the same complete contract be promoted first to controlled gem5 and later, if necessary, to KVM-to-Timing SimCXL. No Cherry use is needed before this gate.

## Execution command

```bash
cd /home/ubuntu/ssdd-research
scripts/run_ssdd_comparative_native.sh
```

The runner writes an evidence directory under `evidence/comparative/`, including `manifest.json`, `results.json`, `summary.json`, policy inventory, provenance, captured stdout/stderr, `SHA256SUMS`, and checksum verification. A completed run remains a local contract-smoke result until the human-review and concurrent-baseline gates above are satisfied.

## References

[1] [SSDD comparative-value validation plan](ssdd-comparative-value-validation-plan-20260823.md)
[2] [Completed cross-domain mechanism proof](cherry-cross-domain-mechanism-proof-20260823.md)
