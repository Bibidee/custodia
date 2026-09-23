import { createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";
import { privateKeyToAccount } from "viem/accounts";
import keytar from "keytar";
import { setTimeout as delay } from "node:timers/promises";

const address = "0xa2F83008C4a1d3c4e39A59502765648d6902dfD9";
const id = process.env.CUSTODIA_V23_ID;
if (!id) throw new Error("CUSTODIA_V23_ID is required");
const key = await keytar.getPassword("genlayer-cli", "account:fresh-bob");
if (!key) throw new Error("fresh-bob keychain entry unavailable");
const client = createClient({ chain: studionet, endpoint: "https://studio.genlayer.com/api", account: privateKeyToAccount(key) });
const hash = await client.writeContract({ address, functionName: "cancel", args: [id], consensusMaxRotations: 5 });
for (let attempt = 0; attempt < 180; attempt++) {
  await delay(10000);
  const tx = await client.getTransaction({ hash });
  if (["FINALIZED", "UNDETERMINED", "CANCELED"].includes(tx.statusName)) {
    console.log(JSON.stringify({ hash, status: tx.statusName, result: tx.result_name, execution: tx.consensus_data?.leader_receipt?.[0]?.execution_result }));
    const state = await client.readContract({ address, functionName: "get_escrow", args: [id], transactionHashVariant: "latest-final" });
    console.log(JSON.stringify({ state }, (_, value) => typeof value === "bigint" ? value.toString() : value));
    break;
  }
}
