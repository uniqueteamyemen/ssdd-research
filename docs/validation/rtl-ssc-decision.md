# RTL Decision: Bounded Snapshot / Epoch SSC

## Decision status

**Selected first RTL target:** a bounded `Snapshot / Epoch` Sequencing and Sorting Controller (SSC) that receives packet descriptors, rejects an exact four-component key collision, and releases the accepted batch in canonical key order only after an explicit snapshot-close event.

The target is deliberately small and has one purpose: move a high-value SSDD invariant from the Python reference into an independently executable RTL simulation. It is **not** an SSDD runtime, CXL endpoint, aggregate engine, hash engine, FPGA implementation, timing closure result, or hardware validation.

## Why this target precedes arithmetic or hashing

The current reference defines the SSC key as:

`structural_dim || enterprise_type || sequence_id || source_chiplet_id`

and rejects exact duplication of that entire four-component key before canonical sorting. This is the first irreversible ordering boundary before aggregation and audit commitment. The existing reference already has deterministic randomized-arrival and collision test intent, making it suitable for a bounded RTL/reference comparison.

## Bounded interface contract

The initial simulation-only module has a compile-time batch capacity of **8 descriptors**. Each descriptor contains the four 32-bit key fields, a signed 64-bit Q32.32 payload field, and a 32-bit node identifier. Its control transitions are:

| State / event | Required behavior |
| --- | --- |
| `snapshot_begin` | Clear the bounded ingress set and start one uncommitted batch. |
| `packet_valid` | Accept a descriptor only while the snapshot is open and capacity remains. |
| exact four-key collision | Raise a reject condition, release no ordered batch, and leave the prior completed snapshot unchanged. |
| `snapshot_close` | Canonically sort accepted descriptors and make them available sequentially. |
| ordered output | Emit exactly the accepted descriptors in ascending lexicographic four-key order. |
| final output acknowledgement | End the snapshot without creating an aggregate, audit record, or global state commitment. |

## Initial reference vectors and acceptance criteria

The RTL test bench will derive or mirror deterministic vectors from `reference/python/prehardware_reference.py`.

| Case | Acceptance condition |
| --- | --- |
| Eight-descriptor shuffled snapshot | Output keys match the reference canonical ordering exactly. |
| Repeated shuffled arrivals | Every trial produces the same ordered output sequence. |
| Shared three-key prefix | `source_chiplet_id` breaks the tie in the expected direction. |
| Same four-key, changed payload or node | The snapshot is rejected; no batch is emitted. |
| New snapshot after rejection | The next valid snapshot is independent of the rejected one. |

The retained test output must distinguish `rtl_simulation` from `native_reference` and must record the module/test-bench source hashes. A successful run validates this bounded behavioral contract only.

## Explicit exclusions

The following are later or separate work items: variable-scale hardware sorting, CXL traffic, Q32.32 RTL arithmetic, SHA-256 acceleration, ledger storage, multi-node network behavior, timing closure, synthesis, place-and-route, board loading, CXL protocol compliance, and real-hardware performance.

## Transition gates

1. **RTL simulation gate:** source-controlled vectors pass in at least two independent invocations and collision rejection is retained.
2. **Synthesis gate:** a named target device, clock constraint, synthesis reports, and post-synthesis checks exist. This does not constitute FPGA execution.
3. **FPGA hardware gate:** bitstream, board identity, clocking, physical I/O observations, and retained output evidence exist.
4. **Real-CXL gate:** the FPGA/ASIC device is attached to an identified CXL-capable host and the evidence includes a real link/device observation and applicable independent protocol validation. See [the real-CXL source register](real-cxl-hardware-source-register.md).
