# Cherry Execution-Mode Reconciliation — SSDD

**Status:** Internal evidence-reconciliation record for submission preparation.  
**Repository state reviewed:** `396f51bc2ef890121383903a6d7dd491193b9dc7`  
**Purpose:** Distinguish the retained Cherry execution domains before any submission uses CPU-mode, KVM, CXL, latency, or jitter language.

## Corrected finding

Cherry was used for more than one SSDD execution domain. The retained material establishes three separate bodies of evidence. They must not be merged into one performance claim.

| Evidence body | Execution path established by retained material | What it establishes | What it does not establish |
|---|---|---|---|
| Nine-ID Cherry index, including SCL-01 and LOD-01 | Reference-model / native-reference evidence | The declared behavioral and integrity outcomes for the nine indexed IDs | Physical CXL, FPGA, KVM full-system performance, network throughput, or baseline-versus-SSDD overhead |
| `cherry-controlled-matrix1-20260822` | gem5 syscall-emulation controlled matrix; each retained `config.ini` declares `type=BaseTimingSimpleCPU` | TimingSimpleCPU was used in this model-specific controlled matrix; modeled latency/fault sensitivity and retained functional outcomes can be inspected | KVM boot, full-system guest execution, physical CXL, or a statistical latency/jitter comparison campaign |
| Cherry KVM full SimCXL Type-3 matrix | `boot_cpu=kvm`, then gem5 switches to a Timing CPU before the guest-delimited ROI | An admitted full-system KVM-to-Timing SimCXL behavioral path, five declared memory/fault cells, and three independently retained ROI-closed behavioral executions | A benchmark, latency/p95/p99/jitter/throughput result, physical CXL Type-3, or FPGA behavior |

## Direct artifact basis

The controlled matrix run manifest records `cpu_type=TimingSimpleCPU`, `execution_domain=syscall-emulation-gem5`, and `scope=model-specific-functional-and-timing-sensitivity-only`. The per-run `config.ini` files retain `BaseTimingSimpleCPU`. This is direct configuration evidence for a Timing CPU in the controlled matrix; it is not KVM evidence.

The full-system record states that the five-cell SimCXL matrix used `boot_cpu=kvm`, switched to a Timing CPU on the first exit event, and placed the guest-delimited region of interest after the switch. It retains the markers `SSDD_TIMING_CPU_ROI_BEGIN` and `SSDD_TIMING_CPU_ROI_END`, a `switching cpus` gem5 marker, and nonzero final Timing-CPU `numCycles` counters for every retained case. Runs 1, 2, and 4 are the three ROI-closed behavioral executions. Run 3 remains a semantic behavioral repeat with one documented incomplete ROI-close marker in its rejection cell.[^kvm]

The nine-ID evidence index deliberately keeps this KVM-backed full-system matrix separate from the indexed reference-model results. Its SCL-01 and LOD-01 records are explicitly native-reference/model observations and do not convert the input targets, component timings, or counters into measured CXL/fabric throughput.[^nine]

## Submission-safe language

The following statement is supported:

> SSDD retained a Cherry-hosted, full-system SimCXL/gem5 behavioral matrix that booted under KVM and switched to a Timing CPU before a guest-delimited region of interest. Across three independently retained ROI-closed executions, the five declared behavioral cells reproduced their expected acceptance or rejection semantics. Separately, a syscall-emulation controlled matrix retained TimingSimpleCPU configurations for model-specific timing-sensitivity and fault experiments.

The following statements are **not** supported by the retained records and must not be used:

| Do not claim | Reason |
|---|---|
| Measured latency difference, p95/p99 latency, jitter, or throughput improvement | The KVM-to-Timing matrix was retained as behavioral evidence, not a preregistered quantitative comparison; its documented counters are proof of Timing-CPU execution, not normalized performance metrics. |
| Baseline-versus-SSDD performance or overhead | No retained baseline/control comparison contract is closed for this matrix. |
| Physical CXL Type-3, FPGA, silicon, or production behavior | `cxl-asic` and `cxl-fpga` are simulator modes; the record explicitly rejects physical-device and FPGA claims. |
| A single uniform CPU mode across every Cherry artifact | The corpus contains distinct native-reference, syscall-emulation TimingSimpleCPU, and full-system KVM-to-Timing domains. |

## Readiness consequence for Chiplet Summit

The submission may present the Cherry work as **pre-silicon, full-system SimCXL behavioral validation with a KVM-to-Timing ROI path**, together with separately bounded model-specific TimingSimpleCPU sensitivity evidence. It must label the work as simulation and preserve the separation from the nine indexed reference-model IDs.

A quantitative latency/jitter section requires a new, explicitly declared campaign with a baseline/control definition, repeated runs, ROI accounting, metric units, statistical summary method, and retained raw artifacts. Such a campaign is not created by reinterpreting the current `numCycles`, `sim_ticks`, input targets, or reference counters.

## Evidence references

[^kvm]: [`cherry-kvm-full-matrix-evidence-20260822.md`](cherry-kvm-full-matrix-evidence-20260822.md), especially the execution path, scope boundary, ROI evidence, and repeatability sections.

[^nine]: [`cherry-nine-test-campaign-evidence-index-20260822.md`](cherry-nine-test-campaign-evidence-index-20260822.md), especially the scope boundary, SCL-01/LOD-01 entries, and explicit separation of the KVM-backed full-system matrix from the nine IDs.
