# Custodia deployment

Custodia is not deployed yet. Before deployment, run the complete release gate
from the repository root:

```text
python scripts/preflight.py
python -m pytest tests -q
genvm-lint check contracts/custodia.py --json
genvm-lint schema contracts/custodia.py --output artifacts/custodia.abi.json
```

Freeze the contract source, record its raw SHA-256, deploy once to Studionet,
wait for `FINALIZED / MAJORITY_AGREE / GenVM SUCCESS`, retrieve source with
`gen_getContractCode`, and compare exact bytes before recording a deployment.
