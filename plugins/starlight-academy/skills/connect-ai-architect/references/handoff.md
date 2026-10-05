# Academy handoff contract

| Owner | Contract | Current behavior |
| --- | --- | --- |
| Starlight Academy plugin | Public teaching method and local handoff plan | Four public remote catalog tools; no account or private-resource authentication |
| AI Architect Academy repository | Human/agent entries and deployment discovery | Consume the actual deployment's `/.well-known/academy.json`; this plugin does not host the portal |
| AI Architect repository | Local conductor, artifact gates, stdio MCP and source deploy kits | Runs in the selected repository on the owner's keys; no duplicated server here |
| Customer tenant | Secrets, runtime, storage, execution and observability | Validate separately in the selected tenant; a template link is source access |

Generate a plan with Node 20+ from the connection plugin root:

```sh
node scripts/architect_handoff.mjs --academy-origin https://academy.example --lane agent --architect-root /absolute/path/to/ai-architect
```

`academy.example` is an illustrative input, not a live Academy deployment.
Use a verified HTTPS origin without path, query, credentials or fragment. A local
checkout must contain the canonical package name and regular `mcp/server.mjs`.
These checks establish location and declared identity, not trust in executable
source. Review the checkout before installing its stdio configuration.

The JSON includes `starlight.architect_handoff.v1`, `prepared-not-installed`,
the selected human/agent URL, discovery URL, canonical sources, optional stdio
configuration and explicit false authority/entitlement/validation flags. It has
no private token, checkout URL or cloud-commission promise. Preserve the JSON
with the task's exact source revision when the user requests a handoff artifact.

Keep three evidence transitions separate:

1. Learning: a preserved attempt, assistance, critique, revision and transfer.
2. Engineering: specification/PRD, decisions, gates, costs, rights/provenance,
   test output and fresh-context review of the exact artifact revision.
3. Operations: configured tenant, access/revocation tests, observed deployment,
   observability, maintenance owner, rollback and measured consumption.

Payment must be confirmed by the actual server's authenticated entitlement
contract, scoped to purchaser or sponsored agent, resource/version and expiry.
Absent infrastructure remains unconfigured. A locally saved purchase claim,
public URL, sponsor name, plugin install or HTTP 200 is insufficient evidence.
Keep public Apache-2.0 plugin/team source and separately licensed Academy content
distinct. Curated books require documented rights for any retained text.
