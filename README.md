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

The current v0.2.0 source is frozen at commit
`a3696e40b8bb1d3f8ce3505806e273ba93fb25e0` and has SHA-256
`402e67122ad88fdb2d315cfb50cedf010624f04ac99eee75b6eb9eff022ff7c9`.
The v0.1.1 deployment is historical and must not be treated as the current
release. A fresh v0.2.0 deployment is required after the source is frozen.

The previous v0.1.1 live proposal and malformed-model retryable settlement
remain historical runtime evidence only. v0.2.0 adds storage snapshots for
nondeterministic review, bounded retry attempts, explicit expiry recovery,
consumer-abandonment recovery, and stronger settlement authorization.
