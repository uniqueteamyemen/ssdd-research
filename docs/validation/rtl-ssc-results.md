# RTL SSC Simulation Results

## Classification

**Domain:** `rtl_simulation`
**Status:** accepted for the bounded SSC behavioral contract only
**Evidence:** [`evidence/rtl-ssc/extended-128/manifest.json`](../../evidence/rtl-ssc/extended-128/manifest.json)

This record is intentionally narrower than the software-reference and CXL-aware simulation records. It demonstrates reproducible behavioral simulation of one bounded, snapshot-scoped ordering controller. It does not establish timing closure, FPGA operation, CXL operation, or an SSDD runtime. A separate generic synthesis-feasibility record is available, but it does not change this result's execution domain.

## Accepted results

| Check | Result | Retained evidence |
| --- | --- | --- |
| Deterministic arrival handling | 128 affine arrival trials covering 32 complete unique permutations, with each permutation repeated four times | `extended-128/run-1/simulation.log`, `extended-128/run-2/simulation.log` |
| Full-key ordering | Accepted | Canonical four-key outputs asserted by test bench |
| Three-key-prefix tie break | Accepted | `source_chiplet_id` ordering asserted by test bench |
| Exact four-key collision | Rejected with no ordered output | Collision case in both replay logs |
| Snapshot recovery | Accepted | Valid post-rejection snapshot in both replay logs |
| Independent replay stability | Two independent simulator invocations yielded byte-identical logs | SHA-256 `626b2b530ff79c57771d919e3b380d87955f28c4ce498f7a7891fb32b6a6eae1` |
| Independent vector comparison | Accepted for all 128 affine batches | `RTL_SSC_REFERENCE_COMPARE status=PASS`; canonical trace SHA-256 `418dfa7f30567230babe007d786c044ba5eb3ae07fbf64f5eeba52c6d792fd76` |

The module and test-bench hashes are retained in the manifest. The RTL implementation and test bench are defined by [the bounded SSC decision](rtl-ssc-decision.md) and [its validation plan](rtl-ssc-validation-plan.md). The extended testbench also labels the post-rejection recovery trace separately, preventing that additional sanity check from being miscounted as part of the 128-batch independent reference comparison.

## Technical caveat

Icarus Verilog produced a design time-unit advisory and a synthesis-oriented advisory for a loop bounded by the runtime packet count. These advisories do not invalidate the completed behavioral simulation, but they reinforce its current classification: **no FPGA claim is made**. The separately retained [generic Yosys feasibility record](fpga-synthesis-feasibility.md) reports a technology-unmapped logic transformation only; a target-specific synthesis, timing, place-and-route, bitstream, and board-execution gate remains required.
