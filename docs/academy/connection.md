# Starlight Academy conversation plugin

Two skills and four public HTTP MCP tools connect eight fictional teaching methods and four challenges to your AI host. Version 0.1.1 adds a local handoff to the separate AI Architect Academy human or sponsored-agent path and its canonical architect team. The host supplies the conversation; the public teaching connection uses no Academy account, model key or learner database. Work stays subject to your host's privacy policies.

[Choose a challenge and connect](https://starlightintelligence.academy/academy/connect).

## Codex

```sh
codex plugin marketplace add frankxai/starlight-academy-plugin --ref main
codex plugin add starlight-academy@starlight-academy
```

## Claude Code

```sh
claude plugin marketplace add frankxai/starlight-academy-plugin
claude plugin install starlight-academy@starlight-academy
```

If you already registered this marketplace at an older revision, use your host's marketplace update command. Do not silently replace another registered source. Open a fresh conversation after installation. The historical hosted connection ZIP contains 0.1.0; use the Git marketplace for the 0.1.1 handoff.

Ask: Use Starlight Academy to help me choose a challenge. Ask for my first attempt, offer one hint at a time, critique my evidence and test transfer.

The public directory listing is not submitted or approved. ChatGPT custom setup and its interactive card still need authenticated host verification; see the connection page for current status. Git installation does not constitute provider endorsement. The offline Department Lab remains available through its unchanged pinned installation guide.

Claude 0.1.1 payload commit: `817285bcb45d871308cdda1c5b2fddae0107ee6c`. Read the [current Git source receipt](connection-release.json) and [local handoff contract](../../plugins/starlight-academy/skills/connect-ai-architect/references/handoff.md). Verify with `node scripts/verify_academy_connection.mjs` from a complete repository checkout.

The [historical 0.1.0 receipt](connection-release-0.1.0.json) retains payload `5a03a810f2abfd6b744c1677b6b410f310f6f595` and hosted ZIP SHA-256 `69506f8278c14b981e044e3b3107998a3c70f462e25cdeca056151a8896d7fe5`. Hashes establish content consistency, not host execution, private access, architecture correctness or provider endorsement.
