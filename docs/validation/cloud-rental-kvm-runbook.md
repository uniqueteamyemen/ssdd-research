# SSDD Cloud-Rental KVM Runbook

**Status:** Prepared — no paid resource created
**Scope:** A short-lived, single-tenant x86_64 host for the SSDD KVM and Timing-CPU measurement gate.
**Owner and PI:** Abobakr Ahmed Awadh, Deterministic Solutions and Design LLC.
**Campaign title:** *SSDD: Pre-Silicon Quantitative Behavioral Characterization of Distributed Memory-System Execution.*

## Decision Rule

The preferred class is an **hourly bare-metal host**, not a generic VPS and not nested KVM, because the benchmark must expose host `/dev/kvm` directly to gem5. A cloud offering may not be admitted merely because it uses the word “KVM” in its product name. The resulting host must demonstrate both a readable/writable `/dev/kvm` and `vmx` or `svm` in its CPU flags before it is allowed to receive the performance branch of SSDD.[1] [2]

| Criterion | Required for admission | Not sufficient by itself |
|---|---|---|
| Compute model | x86_64 single-tenant bare metal, hourly or otherwise immediately terminable | VPS, cloud VM, shared instance, or advertised “KVM VPS” |
| Virtualization | `/dev/kvm` readable and writable, plus `vmx` or `svm` | Provider marketing statement alone |
| Measurement transition | Executed gem5 KVM boot, explicit Timing-CPU switch before ROI, retained `resetstats` and `dumpstats` boundaries | Successful OS boot or a host preflight alone |
| Evidence | Raw `stats.txt`, serial logs, manifests, configuration hashes, and SHA-256 inventory | Screenshots, summaries, or elapsed wall-clock time alone |
| Teardown | Provider resource terminated after every rejected smoke or accepted campaign | Closing the browser window or leaving a machine idle |

## Published Cost Boundary

Cherry Servers publishes a bare-metal entry range of US$0.06–0.20/hour and a mid-tier range of US$0.20–0.60/hour for 8–16 cores with 64–128 GB ECC RAM.[3] An 85-hour run at the latter published range is **US$17.00–US$51.00 before VAT and extras**. This is not an offer and not an authorization to spend: final cost depends on the exact in-stock configuration, location, storage, operating-system options, tax treatment, and duration.

The acceptance sequence deliberately limits risk. First create only a short smoke allocation, run the host preflight, and terminate immediately if it fails. Extend the reservation only after KVM boot and the Timing-CPU hand-off succeed. The owner must explicitly approve the exact provider, selected configuration, maximum spend, and resource creation before any payment, terms acceptance, or instance creation.

## Provisioning Sequence

1. The owner creates or accesses the provider account and enters personal/payment information directly. Do not place credentials or payment data in this repository, a chat message, a script, or a shell history.
2. Select an x86_64 **bare-metal** host with enough capacity for the pinned gem5 artifact, guest disk, simulator output, and retained evidence. The actual CPU, RAM, storage, location, price, and hourly termination rule become part of the campaign manifest.
3. Before creating the resource, confirm the exact maximum cost and terminate-after-smoke policy with the owner. Creation and payment are owner-confirmed browser actions.
4. On the already-created host, clone the pinned SSDD commit and run `scripts/run_remote_kvm_host_preflight.sh` from a trusted workstation. The preflight only observes the remote host; it does not install, configure, or benchmark it.
5. If the preflight passes, build or verify the exact gem5 version and execute the KVM-to-Timing-CPU smoke. The smoke must write a new evidence directory and include the processor transition plus ROI statistics boundaries.
6. Only then run the matched baseline-versus-SSDD and time-based adversarial matrices. Each attempt receives a separate directory and one of the standard dispositions: **accepted**, **rejected as designed**, **failed**, **timed out**, **blocked**, or **invalid/inconclusive**.
7. Verify all SHA-256 inventories, curate only accepted evidence into `evidence/`, commit documentation and verified artifacts, push to the SSDD repository, then terminate the host and retain its termination record.

## Remote Host Preflight

From a local checkout at the exact campaign commit, run:

```bash
export SSDD_REMOTE_HOST="<provider-hostname-or-ip>"
export SSDD_REMOTE_USER="<ssh-user>"
export SSDD_SSH_KEY="$HOME/.ssh/<private-key>"
scripts/run_remote_kvm_host_preflight.sh \
  .local-results/cloud-kvm-preflight/<run-id>
```

Exit code `0` means only that the host predicates passed. Exit code `20` means that the host is **blocked** and must not receive a performance claim. The result record is not the gem5 smoke; it is merely the prerequisite record that decides whether the smoke may start.

## Claim Boundary

> A passing rental-host probe does not establish latency, jitter, throughput, overhead, physical CXL Type-3 behavior, FPGA behavior, or silicon performance. Those claims require the subsequent admitted measurement path and remain scoped to the retained gem5 and simulated-CXL configuration.[1] [2]

## References

[1]: [gem5: Using KVM CPUs](https://www.gem5.org/documentation/general_docs/using_kvm/)
[2]: [SSDD controlled-validation campaign](controlled-validation-campaign-20260822.md)
[3]: [Cherry Servers: Bare-metal server cost](https://www.cherryservers.com/blog/bare-metal-server-cost)
