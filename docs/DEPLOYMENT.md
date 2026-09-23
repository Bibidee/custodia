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

## Current v0.2.0 deployment

- Frozen source commit: `a3696e40b8bb1d3f8ce3505806e273ba93fb25e0`
- Local SHA-256: `402e67122ad88fdb2d315cfb50cedf010624f04ac99eee75b6eb9eff022ff7c9`
- Contract: `0xeb971A2d98B20f3908F116136A3A8A4A68a6efaf`
- Deployment transaction: `0xedaf83645cd92d2572b3bb5459c25eb7c91f614389200c40b848e315272d30c5`
- Explorer: https://explorer-studio.genlayer.com/address/0xeb971A2d98B20f3908F116136A3A8A4A68a6efaf
- Finalization: `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`
- Deployed source: 16,891 bytes, SHA-256 `402e67122ad88fdb2d315cfb50cedf010624f04ac99eee75b6eb9eff022ff7c9`
- Source parity: `VERIFIED` via `gen_getContractCode`, byte-for-byte
- `get_info()`: `Custodia`, version `0.2.0`, min confidence `75`, max artifact bytes `16000`, max review attempts `3`, min deposit `1000000000000000`

### v0.2.0 live verification

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
