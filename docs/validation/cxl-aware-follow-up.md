# CXL-Aware Follow-Up Gate After the Limited Matrix

**Status:** Defined; no follow-up SimCXL execution has started.
**Execution domain if run:** `cxl_aware_simulation`.
**Entry evidence:** The retained limited matrix contains one accepted CXL-ASIC normal case and one bounded rejected proof-corruption case.[1]

## Purpose

The completed limited matrix resolves one narrow question: whether the reference workload's stated normal and proof-corruption behavior is observable after a guest exposes the selected simulated two-node Type-3 topology. The next work must answer specific remaining questions without relaunching a large or unfocused campaign. Every result remains simulation-only and may not be relabelled as FPGA or real-CXL hardware evidence.

## Prioritised follow-up set

| Priority | Named case or design task | Unanswered question | Required observables | Stop/acceptance condition |
| --- | --- | --- | --- | --- |
| 0 | Instrumentation design review | Are Snapshot/Epoch measurements defined at a traceable boundary and paired with identical inputs? | `epoch_input_digest`, `ordered_batch_digest`, chain values, named timing intervals, counter definitions. | Do not execute performance-shaped cases until instrumentation is versioned, unit-defined, and tested against a DRAM control. |
| 1 | `dram-control-accepted` and `dram-control-proof-corruption` | Does the unchanged full-system control preserve the known normal/reject oracle outside CXL allocation? | Normal/reject digest and exit markers, topology, raw traces, SHA-256 inventory. | Accept only if the prescribed normal and corruption outcomes hold; otherwise stop and investigate before CXL comparison. |
| 2 | `cxl-fpga-accepted` | Does the alternate **simulated** Type-3 model preserve the normal oracle under the same allocation policy? | The limited-matrix observables plus model configuration hash. | Record acceptance or retain failure. Never call it FPGA hardware validation. |
| 3 | `interleave-accepted` | Does the named interleave policy preserve chain correctness? | Same chain/oracle traces plus documented allocation policy. | Record acceptance or retain failure. No bandwidth conclusion. |
| 4 | Latency-binding feasibility review | Is there a verified, version-specific SimCXL configuration binding that changes a defined latency parameter? | Source/configuration citation, binding diff, a frozen control command. | If no binding is demonstrated, record `blocked` and do not fabricate a latency sweep. |
| 5 | One paired latency or contention pilot | Once the preceding gates pass, can one changed model setting or one named co-runner be paired with a frozen control? | The full Snapshot/Epoch measurement set and matched raw artifacts. | Report only the paired model observation; stop before expansion if the oracle diverges or evidence is incomplete. |

## Snapshot/Epoch measurement contract

An execution is eligible for a follow-up result only if it binds each event set to an `epoch_input_digest`, binds its canonical order to an `ordered_batch_digest`, and preserves `previous_hash`/`snapshot_hash` around the targeted epoch. The trace must define `T_admit`, `T_order`, `T_snapshot`, `T_commit`, and `T_total`, including their clock source and unit. Rejected and disrupted cases must preserve the last valid chain value before the target epoch, rather than merely reporting a failed process.

The criteria make a timing-shaped study falsifiable: a case with incomplete trace data, changed input, unknown unit, lost raw evidence, or an unexplained oracle divergence is not a successful result. It is a retained blocked or failed result.

## Review gates

Before each named run, the reviewer must confirm the source tag, tool revisions, input hashes, disk-image provenance, configuration diff, fault oracle, evidence destination, and expected interpretation category. After each run, the reviewer must verify the raw serial log, guest exit, simulator status, hash manifest, derived summary, and claim label before allowing the next priority.

> The goal is not to maximize simulator runs. It is to reduce the number of unanswerable claims by executing the smallest case that can distinguish a defined model observation from a tooling, input, or evidence defect.

## References

[1]: [SimCXL Type-3 Limited-Matrix Results](simcxl-type3-limited-results.md)
