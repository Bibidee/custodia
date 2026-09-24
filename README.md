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

Current Studionet release: v0.2.5 at
[`0xbbE551d0197279E17dC0Ed82b876371856EF03cd`](https://explorer-studio.genlayer.com/address/0xbbE551d0197279E17dC0Ed82b876371856EF03cd).
Its live review reached `approved` (confidence 88, `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`), then the designated consumer settled after the release window. The settlement finalized `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`; canonical state is `consumed`, `deposited=0`, `settlement=paid_beneficiary`, and `settled_amount=1000000000000000` wei (0.001 GEN). The transaction is [`0x8fbc20bfa36316231afe30dd0a70de8c58954f0fc1d55230cb23fcf3f856e22c`](https://explorer-studio.genlayer.com/tx/0x8fbc20bfa36316231afe30dd0a70de8c58954f0fc1d55230cb23fcf3f856e22c). This fixture used one test account as sponsor, beneficiary, and consumer, so the recorded payout went to that same beneficiary/consumer address. Earlier versions in this section are historical evidence.

The historical v0.2.0 source is preserved at commit
`a3696e40b8bb1d3f8ce3505806e273ba93fb25e0` with SHA-256
`402e67122ad88fdb2d315cfb50cedf010624f04ac99eee75b6eb9eff022ff7c9`.
The v0.2.0 Studionet deployment is historical. The v0.2.1 deployment is also
historical/superseded; its source is at commit `8d3073798c9583fcc9edae229fa44399cf18ca33` with SHA-256
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

## Security model

Custodia verifies exact raw artifact bytes against committed SHA-256 digests
before semantic review. HTTPS admission rejects local, private, loopback,
link-local, reserved, multicast, and credential-bearing URLs; it cannot prove
DNS or redirect safety. Artifact text is untrusted and is explicitly fenced
against prompt injection. Malformed model output, unavailable sources, hash
mismatches, and validator disagreement fail closed and remain refundable.
Validators must now agree on the final verdict, all three semantic fields, and
stay within a 20-point confidence band. Consumer abandonment is bounded by a
recovery deadline that refunds the sponsor.

## Historical v0.2.2 deployment

The v0.2.2 source adds bounded semantic equivalence and adversarial tests. Its
source commit is `17a3fbe4fc2309aec14f27b81e3988ac0bd2d967`. Its
source SHA-256 is `2f62f4d2e6ff62a4f8c83fe96a1f8973b83c9026ea715f750866483401e44ab3`.
It is deployed at `0xe27919aEd70acBE7773D125B1efD70a948d2285c` via
`0x6cfe58d6f3def5220b45a02e9827013db0d5e7f1e2883f2e0d6dfd1767421952`.
The deployment finalized as `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`;
`gen_getContractCode` returned 17,875 bytes with byte-for-byte parity.

- `get_info()`: `Custodia`, version `0.2.2`, min confidence `75`, max confidence delta `20`, max artifact bytes `16000`, max review attempts `3`, min deposit `1000000000000000`
- Explorer: https://explorer-studio.genlayer.com/address/0xe27919aEd70acBE7773D125B1efD70a948d2285c

That release passed 12 Direct Mode tests, including approved consumer
settlement, ledger-zeroing before payout, and settlement replay rejection. The
current v0.2.5 gate passes 15 tests.

The first v0.2.2 live proposal
`0x6e5739fc937c214f88f768a25abea5ae46a833c953669b8d66875eff524c2c9f`
created `CUSTODIA-V22-LIVE-1790166530699` and finalized with an exact pending
state read. Review
`0x229a7501615ee458d0cf17ef2fa97a9102ca35577c38108f978b54485ad5f7a3`
finalized `MAJORITY_AGREE / GenVM SUCCESS` but safely recorded
`retryable / malformed_model_output`; no approval or payout was created.
After the timeout, settlement
`0x6a4365727186afd5a96847b191751f68c2b5d091c37621d9fc0b7591b5a27f8e`
finalized `MAJORITY_AGREE / GenVM SUCCESS`, refunded the sponsor, and left
`status=settled`, `deposited=0`, `settled_amount=1000000000000000`.
This records the fail-closed result for that historical attempt; later
v0.2.5 evidence below demonstrates an approved semantic review.

## Historical v0.2.3 hardening and deployment

The v0.2.3 source treated `malformed_model_output` as validator
disagreement rather than an agreed semantic result. This forces leader
rotation and prevents identical provider-shape failures from being committed
as consensus. Approval predicates and artifact checks remain unchanged.

The hardened source is deployed at
`0xa2F83008C4a1d3c4e39A59502765648d6902dfD9` with deployment transaction
`0xaf2571a018f65a781924976bd46643e9a42bbebc3004040444139a6b374105a9`.
It finalized with `MAJORITY_AGREE / GenVM SUCCESS`. Source retrieval through
`gen_getContractCode` matched the repository byte-for-byte: 18,400 bytes and
SHA-256 `1e8377c3fc49a4f8f49eeeea59e0ca8e2fb49b3de7650985024c207cfe306b37`.
`get_info()` reports version `0.2.3`.

The controlled v0.2.3 review probe created
`CUSTODIA-V23-REVIEW-1790193048775` in proposal transaction
`0xa63b5b23b8c370ef4adfc2e3ba188ba114b86fe3283e84be64e4fbcae723e42a`.
Its review transaction
`0xf59ef0743e4c5d52a8629f7862a4f4602fdacaa9f05e6459fd78920ee3df7ec0`
finalized `UNDETERMINED / MAJORITY_DISAGREE / GenVM SUCCESS`; the canonical
state remained `pending` with the deposit held. This demonstrates that
malformed provider output no longer finalizes as agreed retryable consensus.
The probe was then cancelled in
`0x1446d6d89d230e25996ca40f3b979482b98e1a01ef759de18f84e806d8e41383`,
which finalized successfully and left `status=cancelled`, `deposited=0`, and
`settlement=cancelled_refunded`.

## v0.2.4 live diagnostic deployment

The diagnostic source is deployed at
`0x062e737ea928999e233C134da2557bC5F757785e` with deployment transaction
`0x075250f718178b2493fd65dc9bd9108998d8490fea481ca8078d3f2441640c1b`.
It finalized `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`. `get_info()` reports
version `0.2.4`; deployed code retrieved with `gen_getContractCode` matched the
local source byte-for-byte (21,167 bytes, SHA-256
`342d790c1362bd2dff6252e18622673e94d01feb651158e0730355d1e6c789b0`).

The controlled diagnostic escrow `CUSTODIA-V24-DIAG-1790206889939` was
proposed in `0x221faac1141e7597c962a38ecaed3c12783fb3bef6483788e654fcb748113ffd`.
The review transaction
`0x2534f65f5384435cb09c2dc703f5c6d7b45fe8a4c1db62566b93c3a6b1c957aa`
finalized `UNDETERMINED / MAJORITY_DISAGREE / GenVM SUCCESS`. Its bounded
diagnostic was `malformed_model_output:invalid_enum_deliverable_match`: the
`deliverable_match` field did not normalize to one of the contract's allowed
enum values. The Explorer does not expose the raw provider value, so its exact
text is unknown. The escrow was then cancelled and refunded in
`0x2060efbc58d5e7061faf5e88b3f8f9fc5e80f93a7c936467448b64f7475b7b2f`,
finalizing `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS` with
`status=cancelled`, `deposited=0`, and `settlement=cancelled_refunded`.

## v0.2.5 deployment and live approval

The v0.2.5 prompt now states the exact lowercase enum vocabulary and field
meanings, along with JSON type and length constraints. The parser remains
strict: no synonyms are accepted and the approval tuple is unchanged. This
addresses the specific invalid-enum field diagnosed on v0.2.4, although the
provider's exact rejected token remains unavailable.

- Contract: `0xbbE551d0197279E17dC0Ed82b876371856EF03cd`
- Deployment transaction: `0x1c275cb424cbf7e5bde25851f3cba149d7869be32fbb5ce704f18444f2176707`
- Source commit: `6a137bbf172ff2b69e463e1f54ec1b19da9b1c98`
- Deployment result: `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`
- Explorer: [contract](https://explorer-studio.genlayer.com/address/0xbbE551d0197279E17dC0Ed82b876371856EF03cd) · [deployment](https://explorer-studio.genlayer.com/tx/0x1c275cb424cbf7e5bde25851f3cba149d7869be32fbb5ce704f18444f2176707)
- Source parity: byte-for-byte verified through `gen_getContractCode`, 22,489 bytes, SHA-256 `e9429e76a205f1fd506f9c3a75002bffa4c346d2723ac13db6eef7690ad6a000`
- `get_info()`: Custodia v0.2.5, minimum confidence 75, maximum confidence delta 20, maximum artifact size 16,000 bytes, maximum review attempts 3, minimum deposit 0.001 GEN
- Release checks: 15 tests passed; preflight, GenVM lint and ABI/schema passed; GitHub CI run [35935645228](https://github.com/Bibidee/custodia/actions/runs/35935645228) passed.

The live escrow `CUSTODIA-V25-PROMPT-1790207905899` proposed in
[`0x9ceb4f1653388580a8a13fbe029c7659b7ea606aaf4fc6bdeaf9620333891fae`](https://explorer-studio.genlayer.com/tx/0x9ceb4f1653388580a8a13fbe029c7659b7ea606aaf4fc6bdeaf9620333891fae)
finalized `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS` and stored the exact
committed artifact URLs and hashes. Its semantic review
[`0x11a5ec2779ae6abec1c93226bc0bed551d4665b080e7a0c25133fee7f13b22f5`](https://explorer-studio.genlayer.com/tx/0x11a5ec2779ae6abec1c93226bc0bed551d4665b080e7a0c25133fee7f13b22f5)
also finalized `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`; canonical state is
`approved`, confidence `88`, with rationale: “Deliverable CUSTODIA-LIVE-001 is
confirmed complete by independent evidence, matches the committed description,
and is ready for beneficiary release with no contradictions or safety
concerns.” The release window ended at `timeout_at=1790211507`
(`2026-09-24 00:58:27 UTC`). The designated consumer then submitted settlement
transaction
[`0x8fbc20bfa36316231afe30dd0a70de8c58954f0fc1d55230cb23fcf3f856e22c`](https://explorer-studio.genlayer.com/tx/0x8fbc20bfa36316231afe30dd0a70de8c58954f0fc1d55230cb23fcf3f856e22c),
which finalized `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS` with all five
validators agreeing. The canonical escrow state is `consumed`,
`deposited=0`, `settlement=paid_beneficiary`, and
`settled_amount=1000000000000000` wei. The designated account balance read
increased from `448.9999 GEN` to `449.0009 GEN`. This fixture used the same
test account as sponsor, beneficiary, and consumer, so it demonstrates recorded
beneficiary payout and one-time consumption, not a transfer between distinct
users.

The immutable artifacts were independently fetched and hash-verified:

- Deliverable: `https://raw.githubusercontent.com/Bibidee/custodia/2b8e414a8f1000a4679d6a7f1a9926009b4e36cd/evidence/live-deliverable.txt` — SHA-256 `0xb7071f431f30123d20f407f5819e7626792e9e6a8c26e3d7bb51f8cdc5ebeed8`
- Evidence: `https://cdn.jsdelivr.net/gh/Bibidee/custodia@2b8e414a8f1000a4679d6a7f1a9926009b4e36cd/evidence/live-evidence.txt` — SHA-256 `0x090299995751c5a4e8c06fa36259b1e9ded8a0f544cbf4bda2af1ae8d7e035cd`
