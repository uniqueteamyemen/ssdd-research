# Publication allocation inventory

**Purpose.** This inventory records the publication destination for the material reviewed during the SSDD repository curation. It is a scope-control record: no material is copied to a repository unless its destination and evidence status are explicit.

## SSDD repository: `uniqueteamyemen/ssdd-research`

| Material class | Curated location | Publication status | Boundary |
|---|---|---|---|
| SSDD specification, implementation manual, prototype roadmap, and code-core documents | `docs/source/` | Included as the four primary source documents | Source material; not a claim of completed production delivery. |
| Python deterministic reference | `reference/python/` | Included | Research reference and test fixture; not the product runtime. |
| Rust ledger reference | `reference/rust/` | Included | Independent comparison fixture created for the recorded cross-language test; not a supplied SSDD Rust runtime. |
| gem5 workload and configuration | `simulation/gem5/` | Included | Model-scoped simulation fixture; not hardware, CXL, or certification evidence. |
| Reproduction scripts | `scripts/` | Included | Local output is intentionally excluded by `.gitignore`. |
| Machine-readable accepted/rejected results | `evidence/` | Included | Retained evidence only; raw local build products and temporary outputs are excluded. |
| Validation plans, results, catalog, and test matrix | `docs/validation/` | Included | Public claims must follow the limitation language in each record. |

## Existing PayLock repository: `uniqueteamyemen/paylock-core`

PayLock remains in its existing repository. Its commercial protocol, product-specific source material, and any PayLock-only evidence belong there. No PayLock source, market claim, payment workflow, customer data, or deployment configuration has been copied into `ssdd-research`.

## Existing HC-CXL repository: `uniqueteamyemen/HC-CXL-Sovereign`

HC-CXL remains in its existing repository. Its protocol source material, physical and systems-model documentation, certified-link claims, visual material, and experiment records belong there. No HC-CXL source, hardware claim, or physical-performance assertion has been copied into `ssdd-research`.

## Excluded material

The SSDD repository excludes external simulator source and build trees, temporary simulator output, local executables, duplicate upload variants, secrets and local environment files. The repository therefore contains the curated sources, reproducibility harnesses, retained evidence records, and documentation needed to evaluate the declared model-scoped work without presenting unrelated or unsupported material.
