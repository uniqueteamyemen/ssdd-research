# SSDD Independent Reviewer Outreach Package — LinkedIn

**Purpose:** Recruit independent reviewers for a bounded, blinded comparison of three shared-state policy records.
**Posting control:** This file is copy-ready material for the owner to post. It does **not** authorize an automated post, promise a result, or disclose the arm-label key.

## 1. Public claim boundary

The current local result is deliberately not a marketing win. Under one bounded 133-case contract, SSDD, a serious CAS/retry reference, and a serious single-writer-sequencer reference each met the tested semantic containment contract after the conventional arms explicitly added canonical candidate/queue-drain policies. No arm has been declared clearer, simpler, faster, lower-overhead, or superior.[1]

The invitation asks reviewers whether the retained decision/evidence path is more inspectable for a fixed engineering task. It does **not** ask them to endorse SSDD, and it does not claim physical CXL, FPGA, hardware, latency, jitter, percentile, throughput, scaling, or production evidence.

## 2. Primary LinkedIn post — recommended

> **Independent systems reviewers requested — a deliberately non-promotional comparison**
>
> We are testing a narrow question about shared-state engineering: when the same event set can arrive in different orders or contain a late, corrupted, or conflicting record, does one policy give an engineer a clearer reason for accepting, rejecting, or deferring the next shared checkpoint?
>
> We compared three bounded local policy references against the same 133-case contract: **SSDD**, **CAS/retry**, and a **single-writer sequencer**.
>
> The current result is not “SSDD wins.” All three satisfied the tested containment and arrival-order contract once the conventional alternatives explicitly included canonical candidate/queue-drain policies. That is the honest result.
>
> The remaining question is human and practical: from a blinded evidence bundle, can an engineer determine the disposition rule, material condition, prior valid checkpoint, and policy surface more clearly in one approach than in the others?
>
> We are looking specifically for **independent systems engineers, distributed-systems engineers, memory-system architects, verification/reliability practitioners, and systems researchers**. This is not general engagement: the review asks whether a real engineer can reconstruct a shared-state decision, identify the material condition, and locate the policy surface to change. You do not need to agree with SSDD. A result that favors CAS/retry or a sequencer is equally useful.
>
> The review is bounded: six short cases, three unlabeled policy records per case, and five fixed questions per record. No confidential infrastructure access, source-code change, benchmark run, or product endorsement is requested.
>
> **No contact or permission is required.** Open the public self-service packet at <https://github.com/uniqueteamyemen/ssdd-research/blob/main/docs/review/ssdd-public-self-service-review.md>, verify its checksums, and submit the blinded response directly through the included GitHub Issue template. The A/B/C label key is withheld until responses are locked. The aggregate outcome—including no difference or a baseline-favoring result—will be published within the stated scope.
>
> #DistributedSystems #SystemsEngineering #ComputerArchitecture #CXL #Verification #OpenResearch

## 3. Short LinkedIn post — alternative

> Looking for independent systems, distributed-systems, verification, and memory-architecture reviewers. We tested SSDD, CAS/retry, and a single-writer sequencer on the same bounded shared-state contract. The honest current result: all three meet the tested semantics when the baselines explicitly add canonicalization; there is no declared winner.
>
> We now need blinded review of decision records: which policy makes acceptance/rejection/defer decisions and prior valid state easiest to inspect? No product endorsement or benchmark required. Participate directly—no message or approval required: <https://github.com/uniqueteamyemen/ssdd-research/blob/main/docs/review/ssdd-public-self-service-review.md>
>
> #SystemsEngineering #DistributedSystems #ComputerArchitecture

## 4. Optional comment reply for interested reviewers

> Thank you. You can participate immediately without waiting for a reply: <https://github.com/uniqueteamyemen/ssdd-research/blob/main/docs/review/ssdd-public-self-service-review.md>. The public packet includes the protocol, six cases × three unlabeled records, checksum verification, and the direct response template. Please do not infer or request the label key until responses are locked. A conclusion of “no meaningful clarity difference” is a valid result.

## 5. Optional direct-message invitation

> Hello [Name],
>
> Thank you for offering to review. You may participate immediately through the public workflow; no approval is needed: <https://github.com/uniqueteamyemen/ssdd-research/blob/main/docs/review/ssdd-public-self-service-review.md>. We are running a small independent review of three unlabeled shared-state policy records. The purpose is not to prove SSDD superior; the current local semantic result is a tie after the conventional references explicitly include canonicalization.
>
> Your task is to inspect six short cases and answer the same five questions for each: publication/disposition, governing rule, material event/condition, prior valid checkpoint, and policy surface to change for a different outcome. Please record elapsed time and any uncertainty.
>
> The packet contains no production credentials, infrastructure access, payment, or customer data. It is integrity checked, and the A/B/C label mapping stays withheld until answers are locked. If you agree, I will send the review packet and response template.

## 6. Reviewer acceptance and response procedure

| Stage | Owner action | Reviewer action | Integrity control |
|---|---|---|---|
| Self-enrolment | Reviewer opens the public protocol. | State relevant systems/distributed-systems experience in the Issue template. | Do not reveal arm labels. |
| Eligibility | Apply the predeclared Issue-template controls after submission. | Confirm no direct implementation role and willingness to report “no difference” or a baseline-favoring outcome. | Retain only a minimal participation log without unnecessary personal data. |
| Packet retrieval | No manual sharing required. | Verify `SHA256SUMS` using `checksum-verification.txt`. | Keep `unblinding-key.json` outside the public repository. |
| Review | Provide one fixed public protocol and response template. | Answer five fixed questions per packet; record elapsed time and uncertainty. | Lock eligible Issue responses before any unblinding. |
| Unblinding | Reveal A/B/C mapping only after responses are locked. | Review aggregate outcome and correction notes. | Preserve raw anonymized responses and result methodology. |

## 7. Reviewer response sheet

Use one row per packet. Do not ask the reviewer to rank products or predict performance.

| Packet ID | Published checkpoint? | Governing rule | Material event/condition | Prior valid checkpoint reference | Policy surface to change | Elapsed minutes | Uncertain? | Notes |
|---|---|---|---|---|---|---:|---|---|
| `[packet-id]` | `yes/no` | `[reason]` | `[event/key/condition]` | `[hash]` | `[named surface]` | `[number]` | `yes/no` | `[free text]` |

## 8. Result-publication rule

Publish only an aggregate, anonymized outcome with the exact fixed task, number of completed reviews, data-quality exclusions, and the result category below.

| Outcome | Permitted public statement |
|---|---|
| No material difference | “For this bounded task, the review did not establish a material clarity or policy-inspectability advantage for SSDD.” |
| SSDD record clearer | “For this bounded implementation and reviewer task, SSDD’s retained record was assessed as clearer. This is not a performance or universal-superiority claim.” |
| Baseline record clearer | “For this bounded task, the CAS/retry or sequencer record was assessed as clearer. SSDD should not be marketed as clearer for this scenario.” |
| Review invalid/incomplete | “The review did not meet the predeclared integrity or completeness rule; no conclusion is reported.” |

## 9. Materials to share privately after acceptance

Share only the blinded reviewer folder produced from the retained concurrent local result:

`/home/ubuntu/ssdd-deliverables/ssdd-comparative-blinded-review-20260823T170000Z/reviewer-packets/`

The owner keeps the adjacent `unblinding-key.json` private until responses are locked. The full non-blinded evidence, implementation references, and claim limits are retained in the research repository at commit `c2ab640`.[1] [2]

## References

[1] [`../validation/ssdd-comparative-local-policy-matrix-evidence-20260823.md`](../validation/ssdd-comparative-local-policy-matrix-evidence-20260823.md)
[2] [`../validation/ssdd-comparative-human-review-protocol-20260823.md`](../validation/ssdd-comparative-human-review-protocol-20260823.md)
