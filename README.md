# Custodia

Custodia is a standalone GenLayer Intelligent Contract primitive for
hash-bound milestone escrow. A sponsor locks GEN against an exact deliverable
and evidence bundle. Validators independently fetch the committed raw bytes,
verify SHA-256 digests, and semantically decide whether the evidence supports
release.

The deterministic contract derives `approved`, `blocked`, or `retryable` from
the agreed bounded result. Approval is never based on a summary alone. Payout
logic follows the safe escrow order: read the deposited ledger, zero and save
it, then emit GEN. This makes duplicate settlement structurally impossible.

Terminal paths are deliberately small:

`pending -> approved -> consumed` (beneficiary payout after the review window)

`pending -> blocked|retryable -> settled` (sponsor refund)

`pending -> cancelled` (sponsor refund before review)

Every artifact is HTTPS, size bounded, UTF-8, and SHA-256 verified. External
availability and semantic uncertainty fail closed.

## Release evidence

The current v0.1.1 source is frozen at commit `510c262` and has SHA-256
`b39d55659480c381bc654371abc43188dddf13d7de779d4647f25280d5e0e9d8`.
It is deployed on Studionet at
[`0x1164fB94319dedBB841059E3d20E99f1DfC85C82`](https://explorer-studio.genlayer.com/address/0x1164fB94319dedBB841059E3d20E99f1DfC85C82)
from deployment transaction
[`0x5b465c30fc5a2ee0b09bb3491d12b32711d1fc198d46c4de97f854581648e7a6`](https://explorer-studio.genlayer.com/tx/0x5b465c30fc5a2ee0b09bb3491d12b32711d1fc198d46c4de97f854581648e7a6).
The deployment finalized with `MAJORITY_AGREE` and GenVM `SUCCESS`. The
source returned by `gen_getContractCode` is byte-for-byte identical (13,348
bytes) to `contracts/custodia.py`.

The live proposal
[`0x57fcc744ed1e7cd689a95615bf75879de5330f5cd5baebb7902530a66d182d2a`](https://explorer-studio.genlayer.com/tx/0x57fcc744ed1e7cd689a95615bf75879de5330f5cd5baebb7902530a66d182d2a)
created `CUSTODIA-LIVE-002` and finalized successfully with the exact
hash-bound artifacts stored in `evidence/`. The semantic review
[`0x1d09556957145f9d4206e69bbd7f61a716fe247646d83a125748758ddad31e58`](https://explorer-studio.genlayer.com/tx/0x1d09556957145f9d4206e69bbd7f61a716fe247646d83a125748758ddad31e58)
also finalized with GenVM `SUCCESS`, but the available Studionet model output
was malformed and the contract correctly recorded `retryable` rather than
approving. The sponsor then exercised the fail-closed refund path in
[`0x055c3cd72f22a2af2518f5237dbe97365206225f3466f0b178586b54f33fe955`](https://explorer-studio.genlayer.com/tx/0x055c3cd72f22a2af2518f5237dbe97365206225f3466f0b178586b54f33fe955):
the 1 GEN ledger was zeroed and refunded, leaving the escrow `settled` with
`deposited = 0`. An earlier pre-fix deployment and proposal are retained as
historical runtime evidence only.
