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

The deployed v0.2.0 source is preserved at commit
`a3696e40b8bb1d3f8ce3505806e273ba93fb25e0` with SHA-256
`402e67122ad88fdb2d315cfb50cedf010624f04ac99eee75b6eb9eff022ff7c9`.
The v0.2.0 Studionet deployment is historical. The hardened v0.2.1 source
is at commit `8d3073798c9583fcc9edae229fa44399cf18ca33` with SHA-256
`bf54d33f3d1756920714d3d8ede4d8883b7a51760eb3cfd51a52374a5cab508b` and
is deployed at `0x591f06AD9a5Ea228047B4b23209e2116df9Fd353` via transaction
`0xe928f72a5cdfbe1c00fe519c069b50ccec3745a9b855f8b6a93c16ae857a9269`.
Explorer: https://explorer-studio.genlayer.com/address/0x591f06AD9a5Ea228047B4b23209e2116df9Fd353

The historical v0.2.0 Studionet deployment is
`0xeb971A2d98B20f3908F116136A3A8A4A68a6efaf` (deployment transaction
`0xedaf83645cd92d2572b3bb5459c25eb7c91f614389200c40b848e315272d30c5`).
Explorer: https://explorer-studio.genlayer.com/address/0xeb971A2d98B20f3908F116136A3A8A4A68a6efaf
The v0.1.1 deployment remains historical and superseded.

Deployment finalized as `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`, and
`gen_getContractCode` returned 16,891 bytes with byte-for-byte parity and the
SHA-256 above. The v0.2.0 live proposal
`0x1fed850b1337b73a07b3638454ee1b9615e90debbaab2e2a1080f6f062968ba4`
created `CUSTODIA-V2-LIVE-1790155752547` and finalized successfully; the
pending read matched the committed fields exactly. Its semantic review
`0x970ef99425ed5f3bebd5b228970f074af9d50ed76fb515d3ccb7cdd888e71cc6`
also finalized with GenVM `SUCCESS`, but the validators consistently returned
the safe `malformed_model_output` observation, so the escrow became
`retryable` rather than authorizing payout. Sponsor settlement
`0x153f388c4e2b8dc585e9bf5f4d594caca90d3462d5b60b4d6d6c056a305a828d`
finalized with GenVM `SUCCESS`; the full `0.001 GEN` deposit was refunded,
leaving `status=settled`, `deposited=0`, and `settled_amount=1000000000000000`.

This live result demonstrates fail-closed behavior; it does not claim an
approved payout. v0.2.1 adds deterministic normalization for fenced JSON and
safe non-semantic metadata while preserving strict approval predicates. The
underlying v0.2.0 design adds storage snapshots for
nondeterministic review, bounded retry attempts, explicit expiry recovery,
consumer-abandonment recovery, and stronger settlement authorization.

The v0.2.1 live proposal
`0x555d812b3b0c55427cfb8ec91dc0ea2597445fee49d41696bd6ae49d8f86fcc7`
finalized successfully and created `CUSTODIA-V21-LIVE-1790156954326` in
`pending`. Review
`0x211ce41957d8c8531f5da37b5938f5a6c7e37071dde4cd23a440cff9da711bab`
finalized with GenVM success but returned `retryable / malformed_model_output`.
Refund settlement
`0xe97e263bb86fc74a0576df0d8c049fb9704d192668aa15622ba427769b356a9e`
finalized successfully and returned the full deposit, leaving `settled` with
`deposited=0`.
