# Commercial Workload Definition: Deterministic Settlement Intake

## Status and purpose

**Status:** benchmark definition; no result is reported
**Execution domain:** none until a run is retained and classified
**Purpose:** define a realistic, privacy-preserving workload for comparing deterministic event ordering with a conventional ingress-order baseline.

This document defines a payment-and-settlement-style workload without using customer records, production counterparties, or fabricated performance results. It is a test definition, not an assertion that SSDD is ready for payment processing. Any execution must keep the workload's execution domain separate from the software reference, `gem5`, `cxl_aware_simulation`, `rtl_simulation`, `fpga_hardware`, and `real_cxl_hardware` records.

## Workload contract

Each synthetic settlement-intake event represents an immutable instruction entering a bounded settlement epoch. The producer emits a canonical event identifier, source identifier, amount represented in Q32.32, an account or ledger partition identifier, and a proof or signature reference. Inputs are generated from a versioned manifest and contain no personally identifying, customer, or live financial data.

The SSC ordering key remains exactly:

```text
(structural_dim, enterprise_type, sequence_id, source_chiplet_id)
```

The experiment configuration, not this document, must define the business mapping for these fields. That mapping must be preserved with the input manifest so that a result does not silently reinterpret an ordering dimension as a business priority.

| Dimension | Baseline contract | SSDD comparison contract | Equality requirement |
| --- | --- | --- | --- |
| Business validation | Apply the same structural, balance, and authorization predicates | Apply the same predicates before SSC admission | Equal validation code/version and input manifest |
| Admission | Preserve recorded ingress order | Canonically order admitted events by the four-key SSC tuple | Identical accepted/rejected event set |
| State transition | Apply the shared settlement transition function | Apply the identical transition function to the canonical batch | Same serialized state format and hash algorithm |
| Evidence | Retain ingress trace, output state, and execution metadata | Retain ordered batch, output state, proof/hash trace, and execution metadata | A comparison is invalid if either evidence chain is incomplete |

## Metrics to collect, not numbers to claim

| Metric | Definition | Required raw inputs |
| --- | --- | --- |
| Commit latency | Monotonic time from accepted ingress to state-commit acknowledgment | Per-event ingress and commit timestamps |
| Jitter | Predeclared latency dispersion statistic, such as p99 minus p50 | Complete latency sample, calculation version, and percentile method |
| Throughput | Accepted, committed events divided by measured active interval | Counts, interval boundaries, and exclusion rules |
| Batch size | Events and bytes per completed epoch | Input and output byte counts |
| Network overhead | Wire or transport bytes attributable to the workload | Capture/export method and counters |
| Integrity disposition | Hash-chain verification, proof verification, duplicate/collision handling, and last-valid-state behavior | Full trace, hashes, rejection reason, and recovery output |

No threshold is implied by this definition. A particular target, percentile, or expected improvement must be predeclared for a future run and must not be retrofitted after observing results.

## Controlled experiment matrix

The minimum execution matrix varies one factor at a time while retaining an immutable manifest, implementation revision, and environment record. Each cell requires at least one baseline run and one SSDD-comparison run, plus independent replay where the execution domain permits it.

| Factor | Initial levels | Primary observation | Integrity companion check |
| --- | --- | --- | --- |
| Epoch population | 8, 16, 32, 64, 128 events | Commit latency, throughput, bytes per epoch | Canonical order and final state/hash agreement |
| Arrival disorder | Already ordered, rotated, random permutation, late arrival | Delay and queue behavior | Identical canonical batch for equal admitted event sets |
| Event-rate pressure | Predeclared low, medium, high offered rates | Backpressure, throughput, jitter | No unaccounted admission or state transition |
| Fault condition | Packet drop, node delay, aggregator failure, corrupted state/ledger | Failure containment and recovery time | Last valid state retained and fault disposition recorded |
| Execution domain | Native reference, `gem5`, CXL-aware simulation, and later physical domains | Domain-specific measured values only | No cross-domain aggregation or hardware inference |

## Falsification conditions

The workload comparison fails its integrity claim for a cell if two valid replays with the same admitted input manifest produce different canonical batches, state hashes, or proof dispositions; if a rejected event changes the committed global state; or if timing data lacks the raw timestamps and clock description required to interpret it. A performance cell is inconclusive, rather than accepted, if the two sides do not share the validation and state-transition contract.

## Evidence package

Every execution directory should retain a machine-readable manifest, input checksum, implementation revision, command line, tool versions, environment topology, raw event trace, output trace, hashes, summary table, and an explicit outcome. Failed, timed-out, or invalidated cells remain part of the evidence package; they are never overwritten by a later successful attempt.
