# SSDD Engineering Capability Case for Chiplet Summit

**Purpose:** Explain the concrete engineering capability SSDD adds above an interconnect/memory fabric. This is a positioning record, not an abstract revision and not a hardware-performance claim.

## Judgment on the proposed positioning

The proposed direction is **substantively right but needs sharper wording**. CXL 3.0 provides coherent memory and shared-memory capabilities across participating hosts; its official white paper describes a memory region that can be simultaneously accessible by multiple hosts while keeping each host’s view of that location up to date through hardware coherency.[^cxl3]

That capability does not by itself define an application-specific rule for: which events are admitted into a shared decision, how equal accepted event sets are canonicalized, when a candidate state may become committed, or what must happen when proof or state integrity fails. Those are not missing CXL features; they are a different engineering responsibility above the memory fabric.

The strongest SSDD claim is therefore **not** “SSDD adds determinism” or “SSDD adds verifiability.” It is this:

> **SSDD supplies a semantic-commit containment boundary: under declared variation in arrival order, modeled memory latency, and tested memory-placement mode, the system must either emit the same canonical committed result or reject the affected candidate before it changes the committed state.**

This is a proposed systems-design capability evaluated in bounded simulations. It is not a claim that CXL cannot support an application that implements a similar policy, nor that SSDD has been validated on physical CXL hardware.

## Six-part engineering case

| Required element | Evidence-bounded case |
|---|---|
| **1. Engineering problem** | A heterogeneous memory system can preserve a coherent byte-level view while the surrounding system still has to decide whether different arrival orders, placement choices, delayed inputs, or corrupted proof/state records are allowed to produce a new shared application decision. Without an explicit semantic commit boundary, engineers can change topology or timing and be unable to distinguish a legitimate timing change from an unintended change in the committed result. |
| **2. Conventional CXL/chiplet behavior** | CXL provides the fabric-level building blocks for coherent memory semantics, memory sharing/pooling, and multi-node topologies.[^cxl3] Its purpose is not to prescribe an application’s event-admission key, canonical batch representation, state-reduction rule, or commit/rejection policy. An architect still needs software/system rules for those choices. |
| **3. SSDD addition** | SSDD’s reference mechanism uses a declared four-field event key, rejects exact-key collisions, canonical-sorts admitted events, reduces the declared batch, constructs a state/hash chain, and validates a candidate record before commitment. In the reference model, packet drop, node delay, aggregator failure, and corrupted-state cases are represented as no-commit or deferred cases that retain the last valid state. |
| **4. Observable benefit** | The useful architectural question becomes testable: **does a declared change in memory mode, modeled latency, or arrival order preserve the same accepted semantic result, or is it contained as an explicit rejection/deferment before state publication?** This lets a hardware/system architect explore memory placement and fabric choices while checking a semantic invariant instead of inferring correctness from coherence alone. |
| **5. Experimental proof** | The retained evidence is bounded but concrete. The native reference tests report 128 shuffled arrival permutations of a 48-packet set with one ordered-batch hash; a separate 256-seed, 100-epoch chain stress test reports one full hash chain; and two independent 100-epoch replays report equal full chains. The controlled gem5 matrix shows the same accepted digest tuple at modeled 10 ns, 50 ns, and 100 ns inputs, while `sim_ticks` differ; selected proof corruptions are rejected. The full-system Cherry SimCXL matrix shows the same accepted reference digest in DRAM-control, `cxl-asic`, `cxl-fpga`, and interleave simulator modes, while proof corruption is rejected. Those CXL labels are simulator modes, not physical devices. |
| **6. Chiplet Summit value proposition** | **SSDD gives a chiplet or CXL system architect a semantic-commit containment rule: vary the memory fabric as needed, but require tested execution paths to produce the same canonical decision or to reject the affected candidate before it mutates the shared state.** |

## What this lets an engineer do

The practical use is not to replace CXL coherence. It is to add a testable contract above it. An architect can run a declared workload through DRAM control, a CXL-aware simulator mode, an interleave mode, or a modeled-latency point and ask two separate questions:

1. What is the resource or timing effect of this configuration?  
2. Did the configuration change the accepted semantic commit, or did the system preserve the same canonical result—or refuse the invalid candidate—under the declared policy?

CXL addresses the first category through its interconnect and memory semantics. SSDD supplies a bounded method for evaluating the second category in the tested system model. The value is the ability to **contain semantic drift while architecture variables are explored**, not a claim that the fabric has no role in correctness.

## Corrections to the supplied ChatGPT text

| Supplied statement | Judgment | Evidence-bounded correction |
|---|---|---|
| “CXL makes distributed memory coherent; SSDD makes the resulting execution state coherent and deterministic.” | Directionally useful but too absolute. | “CXL provides coherent-memory capabilities; SSDD proposes an explicit application/system policy for canonicalization, validation, and commit containment in the tested model.” |
| “128/128 permutations” | Supported only as a native-reference 48-packet ordering test. | State the domain and mechanism: 128 shuffled arrival permutations produced the same canonical batch hash in the reference harness. |
| “100/100 replay hashes” | Not supported as written. | The retained evidence has **two independent replays of 100 epochs** with equal full chains; it is not 100 independent replay runs. |
| “Faults prevent commit of the affected state.” | Supported only in bounded reference/fault cases and selected proof-corruption tests. | State that the tested model represents specified faults as no-commit/deferred cases, preserving the last valid state; selected proof corruption is rejected in gem5/SimCXL evidence. |
| “Layer above CXL fabric.” | Useful architecture shorthand, not a protocol-layer claim. | Say “a system/application-level semantic-commit policy that can be evaluated over CXL-aware configurations,” not a new CXL protocol layer. |

## Claim boundaries that must remain

This narrative does **not** claim that SSDD improves CXL performance, decreases latency/jitter, implements physical CXL or FPGA hardware, replaces coherence, provides distributed consensus, protects against every fault or adversary, or has production deployment evidence. The full-system matrix is a KVM-to-Timing SimCXL/gem5 behavioral record; the native timing series is a reference-model record.[^kvm] [^controlled] [^reference]

## Evidence references

[^cxl3]: [CXL 3.0 white paper, Compute Express Link Consortium](https://computeexpresslink.org/wp-content/uploads/2023/12/CXL_3.0_white-paper_FINAL.pdf)
[^kvm]: [`../validation/cherry-kvm-full-matrix-evidence-20260822.md`](../validation/cherry-kvm-full-matrix-evidence-20260822.md)
[^controlled]: [`../validation/cherry-controlled-gem5-matrix-evidence-20260822.md`](../validation/cherry-controlled-gem5-matrix-evidence-20260822.md)
[^reference]: [`../validation/cherry-scl-lod-derived-timing-differences-20260823.md`](../validation/cherry-scl-lod-derived-timing-differences-20260823.md)
