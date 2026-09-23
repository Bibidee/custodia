# Custodia deployment

## Historical v0.1.1 deployment

- Network: Studionet
- Contract: `0x1164fB94319dedBB841059E3d20E99f1DfC85C82`
- Deployment transaction: `0x5b465c30fc5a2ee0b09bb3491d12b32711d1fc198d46c4de97f854581648e7a6`
- Finalization: `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`
- Source commit: `510c262fb808b80bee94d4be33cae0a386103354`
- Local SHA-256: `b39d55659480c381bc654371abc43188dddf13d7de779d4647f25280d5e0e9d8`
- Source parity: `VERIFIED` via `gen_getContractCode`; 13,348 bytes matched exactly
- `get_info()`: `Custodia`, version `0.1.1`, min confidence `75`, max artifact bytes `16000`

The first deployment (`0xa2297650162FA6eA2DAb37c96A52116F04Cf27f4`, tx
`0x73da61ee846b9cde516966e04290cdf797beabc79e06c346319c42148504798a`) is
historical and superseded. Its first live proposal exposed a Studionet
event-emission runtime incompatibility. It is superseded by the v0.2.0 source.

## Historical v0.2.0 deployment

- Frozen source commit: `a3696e40b8bb1d3f8ce3505806e273ba93fb25e0`
- Local SHA-256: `402e67122ad88fdb2d315cfb50cedf010624f04ac99eee75b6eb9eff022ff7c9`
- Contract: `0xeb971A2d98B20f3908F116136A3A8A4A68a6efaf`
- Deployment transaction: `0xedaf83645cd92d2572b3bb5459c25eb7c91f614389200c40b848e315272d30c5`
- Explorer: https://explorer-studio.genlayer.com/address/0xeb971A2d98B20f3908F116136A3A8A4A68a6efaf
- Finalization: `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`
- Deployed source: 16,891 bytes, SHA-256 `402e67122ad88fdb2d315cfb50cedf010624f04ac99eee75b6eb9eff022ff7c9`
- Source parity: `VERIFIED` via `gen_getContractCode`, byte-for-byte
- `get_info()`: `Custodia`, version `0.2.0`, min confidence `75`, max artifact bytes `16000`, max review attempts `3`, min deposit `1000000000000000`

### Historical v0.2.0 live verification

- Proposal: `0x1fed850b1337b73a07b3638454ee1b9615e90debbaab2e2a1080f6f062968ba4`
  - `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`
  - ID: `CUSTODIA-V2-LIVE-1790155752547`
  - Pending read matched sponsor, beneficiary, consumer, URLs, hashes, brief, and `deposited=1000000000000000`.
- Review: `0x970ef99425ed5f3bebd5b228970f074af9d50ed76fb515d3ccb7cdd888e71cc6`
  - `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`
  - Result: `retryable`, reason `malformed_model_output`; no approval or payout was created.
- Settlement/refund: `0x153f388c4e2b8dc585e9bf5f4d594caca90d3462d5b60b4d6d6c056a305a828d`
  - `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`
  - Result: `refunded_sponsor`; final state `settled`, `deposited=0`, `settled_amount=1000000000000000`.

The review outcome is an honest provider/model-format limitation and confirms
the contract remains fail closed. It is not an approved lifecycle claim.

## Current v0.2.1 deployment

- Source commit: `8d3073798c9583fcc9edae229fa44399cf18ca33`
- Local SHA-256: `bf54d33f3d1756920714d3d8ede4d8883b7a51760eb3cfd51a52374a5cab508b`
- Contract: `0x591f06AD9a5Ea228047B4b23209e2116df9Fd353`
- Deployment transaction: `0xe928f72a5cdfbe1c00fe519c069b50ccec3745a9b855f8b6a93c16ae857a9269`
- Explorer: https://explorer-studio.genlayer.com/address/0x591f06AD9a5Ea228047B4b23209e2116df9Fd353
- Finalization: `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`
- Deployed source: 17,572 bytes, SHA-256 `bf54d33f3d1756920714d3d8ede4d8883b7a51760eb3cfd51a52374a5cab508b`
- Source parity: `VERIFIED` via `gen_getContractCode`, byte-for-byte
- `get_info()`: `Custodia`, version `0.2.1`, min confidence `75`, max artifact bytes `16000`, max review attempts `3`, min deposit `1000000000000000`
- Change scope: deterministic normalization of fenced JSON and non-semantic metadata; strict bounded approval conditions are unchanged.

### v0.2.1 live verification

- Proposal: `0x555d812b3b0c55427cfb8ec91dc0ea2597445fee49d41696bd6ae49d8f86fcc7` — `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`; exact pending state verified.
- Review: `0x211ce41957d8c8531f5da37b5938f5a6c7e37071dde4cd23a440cff9da711bab` — `FINALIZED / MAJORITY_AGREE`; GenVM leader success; result `retryable / malformed_model_output`.
- Settlement: `0xe97e263bb86fc74a0576df0d8c049fb9704d192668aa15622ba427769b356a9e` — `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`; full deposit refunded; final state `settled`, `deposited=0`.

The run confirms fail-closed behavior, but does not claim an approved payout.

## v0.2.2 release candidate

- Source version: `0.2.2`
- Source commit: `17a3fbe4fc2309aec14f27b81e3988ac0bd2d967`
- Local SHA-256: `2f62f4d2e6ff62a4f8c83fe96a1f8973b83c9026ea715f750866483401e44ab3`
- Contract: `0xe27919aEd70acBE7773D125B1efD70a948d2285c`
- Deployment transaction: `0x6cfe58d6f3def5220b45a02e9827013db0d5e7f1e2883f2e0d6dfd1767421952`
- Explorer: https://explorer-studio.genlayer.com/address/0xe27919aEd70acBE7773D125B1efD70a948d2285c
- Finalization: `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`
- Deployed source: 17,875 bytes, SHA-256 `2f62f4d2e6ff62a4f8c83fe96a1f8973b83c9026ea715f750866483401e44ab3`
- Source parity: `VERIFIED` via `gen_getContractCode`, byte-for-byte
- `get_info()`: `Custodia`, version `0.2.2`, min confidence `75`, max confidence delta `20`, max artifact bytes `16000`, max review attempts `3`, min deposit `1000000000000000`
- Equivalence rule: final verdict must match; `deliverable_match`, `evidence_support`, and `risk` must match exactly; confidence may differ by at most 20 points; rationale is explanatory and non-authorizing.
- Release gate: 12 tests passed, preflight passed, GenVM lint passed, ABI/schema passed. Direct Mode includes approved consumer settlement, ledger-zeroing before payout, and settlement replay rejection.
The v0.2.1 deployment remains historical.

### v0.2.2 live verification

- Proposal: `0x6e5739fc937c214f88f768a25abea5ae46a833c953669b8d66875eff524c2c9f`
  - `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`
  - ID: `CUSTODIA-V22-LIVE-1790166530699`
  - Pending read matched proposer, beneficiary, consumer, URLs, hashes, brief, and `deposited=1000000000000000`.
- Review: `0x229a7501615ee458d0cf17ef2fa97a9102ca35577c38108f978b54485ad5f7a3`
  - `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`
  - Result: `retryable`, reason `malformed_model_output`; no approval or payout was created.

The current Studionet provider still returns a structured-output shape that
does not pass the contract's deterministic parser. This is recorded as safe
fail-closed behavior; no approved live payout is claimed.

## Historical v0.1.1 live lifecycle evidence

The v0.1.1 proposal
`0x57fcc744ed1e7cd689a95615bf75879de5330f5cd5baebb7902530a66d182d2a`
created `CUSTODIA-LIVE-002` with a 1 GEN deposit and finalized successfully.
The canonical read showed `pending` and the exact committed URLs and hashes.
The review transaction
`0x1d09556957145f9d4206e69bbd7f61a716fe247646d83a125748758ddad31e58`
finalized with GenVM `SUCCESS`; validators reached agreement on a
`malformed_model_output` observation, so the contract safely recorded
`retryable` (never `approved`). Settlement
`0x055c3cd72f22a2af2518f5237dbe97365206225f3466f0b178586b54f33fe955`
finalized with GenVM `SUCCESS`, refunded the sponsor 1 GEN, and left the
canonical state `settled`, `deposited = 0`, `settled_amount = 1 GEN`.

The immutable artifacts were:

- `https://raw.githubusercontent.com/Bibidee/custodia/2b8e414a8f1000a4679d6a7f1a9926009b4e36cd/evidence/live-deliverable.txt`
  - SHA-256 `0xb7071f431f30123d20f407f5819e7626792e9e6a8c26e3d7bb51f8cdc5ebeed8`
- `https://cdn.jsdelivr.net/gh/Bibidee/custodia@2b8e414a8f1000a4679d6a7f1a9926009b4e36cd/evidence/live-evidence.txt`
  - SHA-256 `0x090299995751c5a4e8c06fa36259b1e9ded8a0f544cbf4bda2af1ae8d7e035cd`

## Release gate

Run the complete release gate from the repository root:

```text
python scripts/preflight.py
python -m pytest tests -q
genvm-lint check contracts/custodia.py --json
genvm-lint schema contracts/custodia.py --output artifacts/custodia.abi.json
```

Freeze the contract source, record its raw SHA-256, deploy once to Studionet,
wait for `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`, retrieve source with
`gen_getContractCode`, and compare exact bytes before recording a deployment.
