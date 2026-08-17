# Contributing to SSDD Research Materials

Contributions must improve reproducibility, provenance, or validation coverage. They must not silently alter the historical meaning of an evidence record.

## Required change record

Every experiment change must identify the changed input, seed, ordering rule, serialization, configuration, compiler/runtime, and execution command. Generated outputs should be stored as machine-readable artifacts alongside a concise interpretation note.

## Claim discipline

Results must distinguish reference-model behavior, software-runtime behavior, simulator behavior, and hardware observations. Do not label a simulated or retained-reference result as a hardware, CXL, security, resilience, or production qualification.

## Source preservation

Do not overwrite a supplied source document or original reference file. Add a dated successor, document its provenance, and retain the prior artifact. Avoid duplicate copies of documents; the canonical source lives under `docs/source/`.
