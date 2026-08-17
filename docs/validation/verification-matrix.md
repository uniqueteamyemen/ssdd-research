# SSDD Pre-Hardware Verification Matrix

## Status and Interpretation

This matrix operationalizes the supplied SSDD specification, implementation manual, and prototype roadmap in a **software-reference and gem5-assisted validation pathway**. It does not certify hardware timing, physical HC-CXL behavior, security, or production readiness. Every test retains its seed, implementation revision, full result manifest, and failure output.

## Acceptance Matrix

| ID | Property and source intent | Controlled procedure | Acceptance criterion | Interpretation boundary |
|---|---|---|---|---|
| ORD-01 | SSC canonical ordering under the four-key tuple | Generate one fixed 48-packet set, apply 128 deterministic arrival permutations, and emit an aged batch. | Every unique-key permutation has byte-identical ordered output and the same batch hash. | Validates the reference sidecar sort only; not concurrent firmware behavior. |
| ORD-02 | Prefix and full-key collision handling | Exercise collisions in one, two, and three key positions, plus an exact four-key duplicate. | Prefix collisions sort canonically; an exact four-key duplicate is rejected before commit. | The supplied reference `Packet.__lt__` has no fifth tie-breaker. Exact duplicate rejection is an explicit harness safety rule, not a claim about the supplied source. |
| RPL-01 | Full replay theorem intent | Run 100 epochs against the same generated input stream in two independent processes. | All 100 chain entries, per-epoch state values, and binary audit records are equal. | Validates the retained reference serialization; it does not prove a full canonical-CBOR implementation. |
| FLT-01 | Failure containment | Inject packet drop, node delay, aggregator failure, and corrupt state/ledger at a named epoch. | The affected epoch is not committed, verification fails where applicable, and the state/hash remain equal to the last valid commit. | Models explicit controls in a single-process reference; no distributed fault-tolerance claim. |
| LED-01 | Forensic non-divergence | Independently modify state hash, previous hash, aggregate, and epoch ID in retained audit data. | Each alteration is detected by full audit validation. | Hash recomputation alone cannot bind `epoch_id` when the documented formula excludes it; the validator separately enforces monotonically contiguous epoch IDs. |
| XLG-01 | Cross-language hash matching | Feed a shared line-oriented epoch fixture to Python and a retained Rust reference. | Same serialized records and all 100 SHA-256 chain entries match. | This is a reference-to-reference test because no supplied Rust source was available. |
| SCL-01 | Scaling behavior | Execute fixed, seeded workloads at 8, 16, 32, 64, and 128 logical nodes. | Retain component timings, epoch success, event rate, packet count, and modeled byte volume for every point; do not infer a target threshold. | Host microbenchmark and modeled network counters; not a fabric benchmark. |
| LOD-01 | Load behavior | Step fixed input rates through 1k, 5k, 10k, 25k, 50k, and 100k events/s-equivalent generation windows. | Retain `T_ssc`, `T_agg`, `T_fuse`, `T_total`, events/s, packets/epoch, and modeled bytes. | The rate is an input-generation rate in the reference model, not observed NIC bandwidth. |
| Q32-01 | Numeric safety | Test raw Q32.32 min/max boundaries, addition and multiplication overflow, zero, and signed fractional products. | Saturation matches `INT64_MIN`/`INT64_MAX`; negative products truncate toward zero. | Tests a fresh reference implementation of the manual’s rules; the uploaded engine lacks its imported `q32_32_core` module. |

## Required Failure Semantics

The reference validator must distinguish **rejection** from **state corruption**. A rejected batch, delayed node, dropped packet, or unavailable aggregator may prevent an epoch from committing; it must not append a new ledger record or mutate the previously committed state. Ledger validation must recompute every record and confirm that the previous-hash chain and epoch sequence are continuous.

## Artifact Layout

The harness writes each fresh run below `SSDD_RESULTS_DIR` (default: `.local-results/prehardware/`). Curated, immutable result records are copied into [`evidence/prehardware/`](../../evidence/prehardware/) in a new named directory rather than overwriting previous output:

```text
prehardware/
  manifest.json
  ordering.json
  replay-run-a.json
  replay-run-b.json
  faults.json
  ledger-tamper.json
  q32.json
  scaling-load.json
  cross-language.json
  gem5-replay/                 # only for the compiled replay integration case
```

The artifacts will name their execution domain: `native_reference`, `rust_reference`, or `gem5_se_timing_simple_cpu`.

## Preconditions and Open Gaps

The uploaded Python engine imports `q32_32_core`, but that module was not supplied. The suite therefore records direct conformance against the documented arithmetic and serialization rules rather than executing the whole uploaded package. The source bundle also has no Rust manifest or Rust source; the cross-language comparison is limited to a retained, minimal Rust reference implementation and is not evidence about an external Rust runtime.
