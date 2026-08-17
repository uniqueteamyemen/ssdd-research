# SSDD Adversarial Validation Plan

## Status

**Status:** planned; no additional adversarial result is reported here
**Purpose:** predefine a minimum falsification-oriented matrix for the SSDD ordering, state, and evidence invariants.

The plan treats a passing result as bounded evidence for a named invariant and a named execution domain. It does not convert a pass in a reference model, `gem5`, CXL-aware simulation, RTL simulation, FPGA hardware, or real CXL hardware into evidence for any other domain.

## Invariants under test

| Identifier | Invariant to challenge | Failure condition |
| --- | --- | --- |
| O-1 | Equal admitted input sets map to one canonical four-key ordered batch independent of arrival permutation. | Any unequal canonical batch, duplicate, omission, or ordering tie resolved outside the defined key. |
| O-2 | Exact four-key collisions receive the predeclared rejection disposition and do not emit a normal ordered batch. | A collision is silently accepted, ambiguously ordered, or changes committed state. |
| E-1 | Epoch boundaries and late-event rules are deterministic and auditable. | An event crosses an epoch boundary without a defined disposition or yields divergent replay state. |
| S-1 | A fault does not replace the last valid committed state with an unverified global state. | The recovered/visible state differs from the last accepted state absent a valid subsequent commit. |
| L-1 | Ledger and proof records detect defined tampering. | A modified recorded field verifies as though untouched. |
| R-1 | Identical deterministic inputs and declared environment produce the same replay evidence where the domain promises determinism. | Batch, hash chain, proof disposition, or trace differs without an explained non-deterministic component. |
| T-1 | Timing claims are supported by complete traces and predeclared envelopes. | A timing conclusion is drawn without raw timestamps, clock source, or predeclared acceptance method. |

## Minimum adversarial matrix

| Family | Injection | Expected recorded disposition | Evidence required |
| --- | --- | --- | --- |
| Epoch boundary | Deliver before-close, close-race, and after-close events with controlled timestamps | Predeclared accept, reject, or defer result for each class | Input manifest, boundary clock/sequence record, output batch, state/hash result |
| Late event | Deliver a valid-key event after its source epoch has finalized | Deterministic late-event disposition without retroactive mutation | Finalized epoch record, late input, replay result, recovery state |
| Ordering perturbation | Randomize, rotate, and concurrently interleave equal event sets | Same canonical batch for each equal admitted set | All permutations, canonical traces, trace hashes |
| Exact collision | Duplicate all four ordering fields while varying payload/source metadata | Rejection with no normal ordered output and no invalid state commit | Rejection trace, output absence/marker, pre/post state hashes |
| Packet drop | Remove an expected packet before assembly | Bounded timeout/failure or explicitly defined incomplete-epoch path | Injection marker, timeout/recovery log, last-valid-state check |
| Node delay | Delay one source beyond the epoch policy threshold | Deterministic defer/reject/recovery behavior | Delay schedule, event disposition, state continuity result |
| Aggregator failure | Terminate or reset aggregation at controlled points | No unverified state publication; restart from recorded valid point | Fault point, process/RTL state evidence, restart and final state |
| State corruption | Alter stored working state or serialized state before verification | Detection and containment before a new valid commit | Original/corrupted bytes, verification output, retained prior state |
| Ledger tamper | Alter state hash, previous hash, aggregate, and epoch identifier in separate cases | Each alteration detected by verification | Tampered artifact, verifier result, full chain result |
| Proof corruption | Alter proof payload, proof hash, or proof linkage independently | Rejection without accepting the corrupted proof as valid | Corrupted input, verifier result, unchanged valid-state evidence |
| Replay divergence | Run independent processes or simulator invocations from the same manifest | Byte-identical or otherwise predeclared equivalent evidence | Environment manifest, trace/hash comparison, divergence report if any |
| Latency/jitter envelope | Apply offered-rate steps and delayed-event injections | Measured only against an envelope declared before collection | Raw timestamps, percentile/dispersion method, load generator version |

## Domain-specific execution rules

Reference and multi-process software experiments may test ordered batches, hash chains, and fault containment. `gem5` and CXL-aware simulation may additionally retain simulator configuration and guest/host logs, but they remain simulation evidence. RTL simulation may test bounded controller behavior, not distributed timing or CXL traffic. FPGA and real-CXL campaigns require the physical topology, bitstream, firmware, measurement, and capture requirements specified in the [real-CXL source register](real-cxl-hardware-source-register.md) before a physical-domain result can be classified.

## Evidence and disposition rules

Each test case must declare its invariant, injection point, deterministic input manifest, expected disposition, timeout, and acceptance rule before execution. The evidence directory must retain all raw logs, configuration, implementation hashes, start/end times, and a summary that distinguishes `accepted`, `rejected as designed`, `failed`, `timed out`, and `invalid/inconclusive`. No failed case may be deleted or overwritten; a remediation attempt uses a new evidence directory and references the prior result.

## Entry and exit criteria

The campaign may begin only after the target execution domain and instrumentation path are identified. A family is complete only when its negative cases have documented dispositions, its positive-control case has been retained, and an independent replay is available where deterministic replay is claimed. A performance result remains descriptive until an integrity companion check passes for the same run.
