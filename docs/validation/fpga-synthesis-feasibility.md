# SSC FPGA Synthesis Feasibility Record

## Classification

**Status:** `synthesis_feasibility`
**Execution domain:** none; this is not `fpga_hardware`
**Tool:** Yosys 0.33, generic technology-unmapped synthesis
**Evidence:** [`evidence/fpga-feasibility/yosys-generic-2026-08-17/`](../../evidence/fpga-feasibility/yosys-generic-2026-08-17/)

This record establishes only that the bounded `snapshot_epoch_ssc` module was parsed and transformed by a generic open-source synthesis flow. It is deliberately not a resource estimate for a named FPGA, a timing result, a place-and-route result, a bitstream, or a hardware execution result.

## Reproducible command

```sh
yosys -p 'read_verilog -sv rtl/ssc/snapshot_epoch_ssc.sv; synth -top snapshot_epoch_ssc; stat'
```

The retained `source.sha256` identifies the RTL source submitted to the tool. The raw `synthesis.log` preserves the exact Yosys output and reported warnings, while `yosys-version.txt` identifies the installed tool version.

## Generic netlist result

| Observable | Reported value | Interpretation boundary |
| --- | ---: | --- |
| Total generic cells | 41,894 | Technology-independent Boolean and sequential cells after Yosys generic mapping. It is not an LUT, ALM, DSP, BRAM, or area count. |
| Sequential-cell family | 1,859 | Sum of reported generic DFF/DFFE cells; it is not a target-device register utilization figure. |
| Inferred memories | 0 | The result reflects the submitted bounded RTL and this generic pass; it does not determine whether a target tool will infer RAM resources. |
| Tool consistency check | 0 obvious problems reported | A structural consistency check, not functional equivalence, timing closure, or board validation. |

The generic synthesis log preserves the complete cell breakdown. These values must not be compared directly with vendor-device utilization reports because mapping rules and primitive libraries differ.

## Required next gate

The first target-specific feasibility gate should choose one named device, pin and clock constraints, tool version, and flow. A small open flow may use a Lattice ECP5 target for early mapping experiments; a CXL endpoint route requires a platform with relevant vendor IP and a compatible host, such as the Agilex path described in the separate [real-CXL source register](real-cxl-hardware-source-register.md). Neither route is present in the current environment.

| Missing artifact | Why it is required before an FPGA claim |
| --- | --- |
| Target-specific synthesis and mapping report | Connects generic cells to actual LUT/FF/BRAM/DSP or equivalent resources. |
| Timing constraints and timing report | Establishes whether the selected clock and I/O constraints close. |
| Place-and-route output and bitstream | Establishes that the chosen board design can be implemented. |
| Board identity, programmed bitstream, inputs, outputs, and measurements | Establishes `fpga_hardware` execution. |
| CXL-capable host/device topology and protocol observation | Establishes the additional prerequisites for a `real_cxl_hardware` claim. |

## Limitations

No FPGA board, vendor CXL IP, target technology library, timing constraint, place-and-route run, bitstream, CXL host, or link trace was used. This evidence remains separate from `rtl_simulation` and `cxl_aware_simulation`.
