# RTL SSC Validation Plan

## Objective

Independently simulate the bounded Snapshot/Epoch SSC contract selected in [the RTL decision](rtl-ssc-decision.md) and retain the simulator log plus source hashes. The plan compares ordering and rejection behavior only; it does not validate the remainder of SSDD.

## Invocation

```bash
./scripts/run_rtl_ssc.sh
```

The default retained evidence location is `evidence/rtl-ssc/`. The runner requires the open-source Icarus Verilog simulator (`iverilog` and `vvp`).

## Required accepted cases

| Case | Oracle | Acceptance condition |
| --- | --- | --- |
| Rotated arrival order | Canonical four-key ordering contract in the Python reference | Sixteen rotations emit the same eight descriptors in canonical order. |
| Shared prefix | Four-key lexicographic comparison | `source_chiplet_id` orders records when the preceding three key fields are equal. |
| Exact collision | Python reference `canonical_sort` collision policy | A repeated full key, even with a changed payload or node, sets rejection and emits no batch. |
| Recovery | Snapshot isolation contract | A valid later snapshot emits normally after an earlier rejected snapshot. |

## Evidence boundary

The accepted result is classified solely as `rtl_simulation`. A passing simulator log does not establish a synthesized design, a clock target, timing closure, physical I/O, a CXL device, or execution on hardware. The next gates remain defined in [the RTL decision](rtl-ssc-decision.md).
