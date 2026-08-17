# SSDD gem5 validation plan

## Purpose

This workstream establishes a **simulation-only** validation surface for selected SSDD properties. It does not model a production SSDD implementation, a CXL physical link, a memory device, silicon timing, security certification, or market readiness. PayLock remains the only commercial offering presented by the website.

## What gem5 can support

The first experiment uses gem5 syscall-emulation mode with an x86 workload and the timing CPU model. It checks that a controlled, fixed-seed sequence of five stages and seven logical engines produces a stable output digest across repeated runs under the same simulator configuration. gem5's memory-model framework can then support sensitivity experiments with configurable hierarchy and latency assumptions. Ruby/SLICC is a future extension path for state-machine and coherence experiments, not a proxy for physical CXL compliance.

## Observable questions

| Experiment | Claim boundary | Success criterion |
| --- | --- | --- |
| Baseline replay | A deterministic reference trace replays consistently in one fixed gem5 configuration. | Two independent simulator runs emit the same operation count and digest. |
| Timing sensitivity | Simulator assumptions can be varied while preserving functional output. | Output digest remains equal; performance statistics are recorded as model-specific observations. |
| Fault-injection scaffolding | Rejected or interrupted logical records are detected by the reference workload. | A deliberately altered record changes the validation outcome and is reported as rejected. |

## Non-claims

The resulting artifacts must not be interpreted as proof of SSDD production readiness, a hardware timing budget, CXL protocol conformance, confidentiality guarantees, or real-world performance. Any website language must identify the results as **gem5 simulation artifacts** and link to the run manifest when published.

## Reproducibility controls

The published record names the gem5 revision, compiler, workload source, command line, workload digest, and output digest. Every experiment is repeatable through [`scripts/run_gem5_baseline.sh`](../../scripts/run_gem5_baseline.sh) or [`scripts/run_gem5_controlled_matrix.sh`](../../scripts/run_gem5_controlled_matrix.sh) after setting `GEM5_ROOT` to a compatible gem5 checkout. New runs write to `.local-results/`; curated output is retained below [`evidence/gem5/`](../../evidence/gem5/).

## Sources

1. gem5, [Building gem5](https://www.gem5.org/documentation/general_docs/building/), accessed 17 August 2026.
2. gem5, [Ruby memory system](https://www.gem5.org/documentation/general_docs/ruby/), accessed 17 August 2026.
3. Supplied SSDD specification, implementation, prototype, and code-design source materials, reviewed in this project workspace.
