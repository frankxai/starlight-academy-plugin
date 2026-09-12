#!/usr/bin/env node
// Explicit offline stdin runner, separate from the MCP transport. No files are read or written.
import { runAcceptanceSuite } from "./acceptance.mjs";
import { writeSync } from "node:fs";
let bytes = 0;
const chunks = [];
process.stdin.on("data", (chunk) => {
  bytes += chunk.length;
  if (bytes > 96000) {
    writeSync(2, "Suite input exceeds 96000 bytes.\n"); process.exit(2);
  }
  chunks.push(chunk);
});
process.stdin.on("end", () => {
  try {
    const input = Buffer.concat(chunks).toString("utf8").replace(/^\uFEFF/, "");
    // A browser export contains its original suite; accept either representation.
    const value = JSON.parse(input);
    const suite = value?.schema === "starlight.acceptance_run.v1" ? value.suite : value;
    const result = runAcceptanceSuite(JSON.stringify(suite));
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    process.exitCode = result.matched === result.total ? 0 : 1;
  } catch (error) {
    process.stderr.write(`${error instanceof Error ? error.message : "Invalid suite"}\n`);
    process.exitCode = 2;
  }
});
