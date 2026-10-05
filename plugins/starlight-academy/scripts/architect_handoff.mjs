#!/usr/bin/env node
// Prepare a local connection plan. No networking, installation, model calls or writes.
import { lstatSync, readFileSync, realpathSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ARCHITECT_REPO = 'https://github.com/frankxai/ai-architect';
const ACADEMY_REPO = 'https://github.com/frankxai/ai-architect-academy';
const PUBLIC_MCP = 'https://starlightintelligence.academy/mcp';

function academyOrigin(value) {
  if (typeof value !== 'string' || value !== value.trim()) throw new Error('Supply one HTTPS Academy origin.');
  const url = new URL(value);
  if (url.protocol !== 'https:' || url.username || url.password || url.search || url.hash || url.pathname !== '/') {
    throw new Error('Academy origin must be HTTPS without credentials, path, query or fragment.');
  }
  return url.origin;
}

function localArchitect(root) {
  if (typeof root !== 'string' || !path.isAbsolute(root)) throw new Error('Architect root must be an absolute local checkout path.');
  const resolved = realpathSync(root);
  const server = path.join(resolved, 'mcp', 'server.mjs');
  const stat = lstatSync(server);
  if (!stat.isFile() || stat.isSymbolicLink()) throw new Error('Architect MCP must be a regular local source file.');
  const packageFile = path.join(resolved, 'package.json');
  const packageStat = lstatSync(packageFile);
  if (!packageStat.isFile() || packageStat.isSymbolicLink() || packageStat.size > 64 * 1024) {
    throw new Error('Architect package metadata must be a bounded regular local file.');
  }
  const metadata = JSON.parse(readFileSync(packageFile, 'utf8'));
  if (metadata.name !== '@frankxai/ai-architect') throw new Error('The selected checkout is not the AI Architect package.');
  return { root: resolved, server, version: metadata.version ?? null, license: metadata.license ?? null };
}

export function prepareHandoff({ origin, lane = 'human', architectRoot } = {}) {
  const academy = academyOrigin(origin);
  if (!['human', 'agent'].includes(lane)) throw new Error('Lane must be human or agent.');
  const local = architectRoot === undefined ? null : localArchitect(architectRoot);
  return {
    schema: 'starlight.architect_handoff.v1',
    status: 'prepared-not-installed',
    lane,
    academy: {
      origin: academy,
      entry: `${academy}/start#${lane}`,
      discovery: `${academy}/.well-known/academy.json`,
      repository: ACADEMY_REPO,
      reachability: 'not-checked',
    },
    architect: {
      repository: ARCHITECT_REPO,
      local,
      sourceTrust: local ? 'identity-and-path-checked-not-executed' : 'checkout-required',
      installArguments: ['npx', 'skills', 'add', 'frankxai/ai-architect'],
      artifacts: 'docs/architecture/',
      workflow: `${ARCHITECT_REPO}/blob/main/WORKFLOW.md`,
      conductor: `${ARCHITECT_REPO}/blob/main/scripts/architect-conductor.mjs`,
      templates: [
        { id: 'request-scoped-agent', provider: 'Vercel', source: `${ARCHITECT_REPO}/tree/main/templates/deploy/request-scoped-agent`, state: 'reference-source-not-tenant-validated' },
        { id: 'durable-worker', provider: 'Railway', source: `${ARCHITECT_REPO}/tree/main/templates/deploy/durable-worker`, state: 'reference-source-not-tenant-validated' },
      ],
    },
    connections: {
      starlight: { transport: 'streamable-http', url: PUBLIC_MCP, scope: 'public-catalog-ids-only' },
      architectMcp: local ? { mcpServers: { 'ai-architect': { command: process.execPath, args: [local.server] } } } : null,
      privateResources: { state: 'discover-deployment-contract-first', entitlement: 'not-checked', credentials: 'none-in-this-plan' },
    },
    record: {
      sponsor: lane === 'agent' ? 'name-human-sponsor-in-local-record' : null,
      attempt: 'preserve-before-assistance',
      evidence: 'exact-artifact-revision-plus-observed-checks',
      review: 'fresh-context-verifier-separate-from-maker',
      production: 'requires-tenant-smoke-tests-and-rollback-evidence',
    },
    grantsAuthority: false,
    provesEntitlement: false,
    verifiesArchitecture: false,
    installed: false,
  };
}

function parseArguments(args) {
  const allowed = new Map([['--academy-origin', 'origin'], ['--lane', 'lane'], ['--architect-root', 'architectRoot']]);
  const options = {};
  for (let i = 0; i < args.length; i += 2) {
    const key = allowed.get(args[i]);
    if (!key || Object.hasOwn(options, key) || args[i + 1] === undefined || args[i + 1].startsWith('--')) {
      throw new Error('Use --academy-origin URL [--lane human|agent] [--architect-root ABSOLUTE_PATH], once each.');
    }
    options[key] = args[i + 1];
  }
  return options;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    process.stdout.write(`${JSON.stringify(prepareHandoff(parseArguments(process.argv.slice(2))), null, 2)}\n`);
  } catch (error) {
    // Avoid echoing paths, supplied origins or local package contents into errors.
    const message = error?.code ? 'Local AI Architect source could not be inspected.' : 'Connection plan refused: check the Academy origin, lane and local checkout identity.';
    process.stderr.write(`${JSON.stringify({ status: 'refused', message })}\n`);
    process.exitCode = 1;
  }
}
