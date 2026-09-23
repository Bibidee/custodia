import { createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";
import { privateKeyToAccount } from "viem/accounts";
import keytar from "keytar";
import { setTimeout as delay } from "node:timers/promises";

const address = "0xa2F83008C4a1d3c4e39A59502765648d6902dfD9";
const key = await keytar.getPassword("genlayer-cli", "account:fresh-bob");
if (!key) throw new Error("fresh-bob keychain entry unavailable");
const client = createClient({ chain: studionet, endpoint: "https://studio.genlayer.com/api", account: privateKeyToAccount(key) });
const json = value => JSON.stringify(value, (_, item) => typeof item === "bigint" ? item.toString() : item);
const fixture = "2b8e414a8f1000a4679d6a7f1a9926009b4e36cd";
const deliverableUrl = `https://raw.githubusercontent.com/Bibidee/custodia/${fixture}/evidence/live-deliverable.txt`;
const evidenceUrl = `https://cdn.jsdelivr.net/gh/Bibidee/custodia@${fixture}/evidence/live-evidence.txt`;
const deliverableHash = "0xb7071f431f30123d20f407f5819e7626792e9e6a8c26e3d7bb51f8cdc5ebeed8";
const evidenceHash = "0x090299995751c5a4e8c06fa36259b1e9ded8a0f544cbf4bda2af1ae8d7e035cd";
const id = `CUSTODIA-V23-REVIEW-${Date.now()}`;

async function wait(hash) {
  for (let attempt = 0; attempt < 180; attempt++) {
    await delay(10000);
    const tx = await client.getTransaction({ hash });
    if (["FINALIZED", "UNDETERMINED", "CANCELED"].includes(tx.statusName)) return tx;
  }
  throw new Error(`timed out waiting for ${hash}`);
}

async function write(functionName, args, value = 0n) {
  const hash = await client.writeContract({ address, functionName, args, value, consensusMaxRotations: 5 });
  const tx = await wait(hash);
  console.log(json({ functionName, hash, status: tx.statusName, result: tx.result_name, execution: tx.consensus_data?.leader_receipt?.[0]?.execution_result }));
  return { hash, tx };
}

const proposal = await write("create_escrow", [
  id, client.account.address, client.account.address, deliverableUrl, deliverableHash,
  evidenceUrl, evidenceHash,
  "Custodia v0.2.3 controlled review fixture authorizes the completed deliverable exactly.",
  21600n,
], 1000000000000000n);
const pending = await client.readContract({ address, functionName: "get_escrow", args: [id], transactionHashVariant: "latest-final" });
console.log(json({ step: "pending", id, state: pending }));
const review = await write("review", [id]);
const reviewed = await client.readContract({ address, functionName: "get_escrow", args: [id], transactionHashVariant: "latest-final" });
console.log(json({ step: "reviewed", id, state: reviewed }));
