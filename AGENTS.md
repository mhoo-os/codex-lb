# AGENTS

## Environment

- Python: .venv/bin/python (uv, CPython 3.13.3)
- GitHub auth for git/API is available via env vars: `GITHUB_USER`, `GITHUB_TOKEN` (PAT). Do not hardcode or commit tokens.
- For authenticated git over HTTPS in automation, use: `https://x-access-token:${GITHUB_TOKEN}@github.com/<owner>/<repo>.git`

## Mhoo operational boundary

`codex-lb` owns application and provider-routing source, not its live
deployment authority. The sibling `../infrastructure` repository owns VPS
deployment, private networking, recovery/rollback custody, provider-facing operational evidence,
and production cutover. Editing this repository, passing tests, or publishing a
build does not authorize a deployment, client-route change, credential change,
or cutover. Those live effects require explicit authorization and the
infrastructure evidence for the exact target.

For Mhoo-wide authority, tenancy, connector, or ownership changes, use an
accepted ADR in `../mhoo/ADR/`; keep this repository's behavior requirements
under the OpenSpec workflow below. This supplements rather than replaces the existing
OpenSpec, merge-gate, migration, compatibility, and regression rules.

## Repository head setup and evidence reuse

Before continuation or handoff, record the primary issue (or explicitly none),
implementation-owning repository, coordinating repo head and retained worker
(or none), exact source commit and PR/evidence links, existing run-ledger
location, dependencies/blockers and their owners (or explicitly none/unknown),
and the authorized next step. Carry this mapping into the handoff and acknowledge
the authoritative instructions commit and reading path. Resolve unknown or
conflicting ownership with the owning head before dependent work; a project
label or issue status does not grant authority or create a new task.

- Verify the remote repository and default branch before starting; the Mhoo
  source is `mhoo-os/codex-lb` (`main` at the 2026-09-07 setup checkpoint).
  Record remote default-branch SHA, local HEAD/branch, dirty state, and retained
  worktrees. Missing files in a sparse checkout do not prove remote absence.
  Use an isolated branch for authorized edits; preserve other workers' changes.
- This is maintained routing source for a retained service. A newer source
  checkout does not identify the deployed image. Historical branches, published
  candidates, and infrastructure receipts retain their original scope and date.
  Workspace UI/identity and business state remain with Twenty; cross-repository
  ownership follows the accepted Mhoo ADR, not an app or project name.
- Reuse the issue's existing checkpoint or evidence index as its run ledger;
  retain the [Mhoo coordinator's instructions](https://github.com/mhoo-os/mhoo/blob/main/AGENTS.md).
  Consult it **before tests, probes, or dispatch**. Reuse matching inputs and
  scope; before a rerun record the changed input, missing receipt, or concrete
  freshness requirement. Required validation gates below remain binding.
- Record each run's actual timestamp (or unknown), source/script hash, target,
  safe command reference, result including failures, evidence location, what it
  proves, and remaining gaps in that existing ledger. Keep secrets and private
  payloads in protected custody; link sanitized references from the issue/PR.
  Source/dependency/test changes invalidate affected source results; deployment,
  restart, configuration changes, or a stated freshness window invalidate the
  corresponding live observation. Neither kind proves the other.
- At the 2026-09-06 retirement checkpoint, [MHO-236](https://linear.app/mhoo/issue/MHO-236)
  scoped preservation to codex-lb; [MHO-249's existing ledger](https://linear.app/mhoo/document/mho-249-retirement-ledger-and-acceptance-handoff-470f0989f837)
  and comment `c854000e-3ac0-425b-a4fe-e8b8d6c28dd9` hold the decision packet.
  These are historical evidence pointers, not current runtime checks or deletion
  approval. [MHO-237](https://linear.app/mhoo/issue/MHO-237) recovery,
  [MHO-241](https://linear.app/mhoo/issue/MHO-241),
  [MHO-248](https://linear.app/mhoo/issue/MHO-248) later work, and MHO-249
  retirement retain separate scopes and gates. Legacy retirement does not block
  fresh Oracle application readiness. Infrastructure owns live-service evidence;
  the Mhoo coordinator retains retirement-evidence coordination.
- Continue only the assigned source scope while its next safe step is clear.
  Finish when the requested artifact and applicable verification are delivered;
  report exact commit/PR, proof limits, next owner/action, and remaining gates.
  Do not manufacture follow-on work or restart parked workers. A handoff requires
  explicit custody acceptance and notification to retained workers; new docs on
  a branch are not automatically available in their existing checkouts.
- Escalate an ownership conflict, missing authorization, incompatible evidence,
  or a required check that cannot be completed with the exact gap and proposed
  next step. Do not change service routes, deploy, hand off credentials, or retire
  resources through a source task. Classify cleanup candidates from receipts;
  a prunable worktree, stopped service, or missing access is not deletion approval.

### Existing verification commands

Read [Makefile](Makefile), [pyproject.toml](pyproject.toml),
[frontend/package.json](frontend/package.json), and
[CI](.github/workflows/ci.yml) at the assigned source SHA before selecting checks.
The following are existing commands, not a record that they have been run:

| Scope | Command from repository root |
| --- | --- |
| Python lint / types | `make lint` / `make typecheck` |
| Focused regression | `uv run pytest <existing-test-path> -q` |
| Unit / bridge integration | `make test-unit` / `make test-integration-bridge` |
| Frontend lint / types / tests | `make frontend-lint` / `make frontend-typecheck` / `make frontend-test` |
| Frontend / package build | `make frontend-build` / `make package` |
| Full local gate | `uv run pre-commit run local-ci --hook-stage manual --all-files` (runs `make ci`) |

`make test-unit`, bridge tests, and packaging build the frontend; frontend
targets install the frozen Bun dependencies. The full gate includes Docker,
PostgreSQL, migrations, and a local Kubernetes smoke cluster. Use isolated test
resources with explicit targets, never an operational database. Select relevant
checks after ledger review; avoid redundant builds. For documentation-only work,
check the diff, links, and applicable documentation/governance checks, and state
why code tests do not apply. This does not waive current-head remote merge gates.

## Code Conventions

The `/project-conventions` skill is auto-activated on code edits (PreToolUse guard).

| Convention | Location | When |
|-----------|----------|------|
| Code Conventions (Full) | `/project-conventions` skill | On code edit (auto-enforced) |
| Git Workflow | `.agents/conventions/git-workflow.md` | Commit / PR |

## Workflow (OpenSpec-first)

This repo uses **OpenSpec as the primary workflow and SSOT** for change-driven development.

### How to work (default)

1) Find the relevant spec(s) in `openspec/specs/**` and treat them as source-of-truth.
2) If the work changes behavior, requirements, contracts, or schema: create an OpenSpec change in `openspec/changes/**` first (proposal -> tasks).
3) Implement the tasks; keep code + specs in sync (update `spec.md` as needed).
4) Validate specs locally: `openspec validate --specs`
5) When done: verify + archive the change (do not archive unverified changes).

### Source of Truth

- **Specs/Design/Tasks (SSOT)**: `openspec/`
  - Active changes: `openspec/changes/<change>/`
  - Main specs: `openspec/specs/<capability>/spec.md`
  - Archived changes: `openspec/changes/archive/YYYY-MM-DD-<change>/`

## Documentation & Release Notes

- Do not manually edit a generated Mhoo context block. Run the central checker
  for Mhoo context changes. Upstream product and contributor content outside
  the bounded notice remains upstream-owned; Mhoo operational claims require
  Infrastructure evidence.
- **OpenSpec is the SSOT for feature/behavior documentation.** User-facing rendering lives under `docs/` (the published docs pages), and each spec-governed page MUST link back to the owning `openspec/specs/<capability>/` entry. Do not create `docs/` content that has no OpenSpec counterpart, and do not add feature docs as new README sections. Keep normative requirements in `openspec/specs/<capability>/spec.md` and free-form rationale in the capability's `context.md` (or change-level context under `openspec/changes/<change>/context.md`).
- **Do not edit `CHANGELOG.md` directly.** Leave changelog updates to the release process; record change notes in OpenSpec artifacts instead.

### Documentation Model (Spec + Context)

- `spec.md` is the **normative SSOT** and should contain only testable requirements.
- Use `openspec/specs/<capability>/context.md` for **free-form context** (purpose, rationale, examples, ops notes).
- If context grows, split into `overview.md`, `rationale.md`, `examples.md`, or `ops.md` within the same capability folder.
- Change-level notes live in `openspec/changes/<change>/context.md` or `notes.md`, then **sync stable context** back into the main context docs.

Prompting cue (use when writing docs):
"Keep `spec.md` strictly for requirements. Add/update `context.md` with purpose, decisions, constraints, failure modes, and at least one concrete example."

### Commands (recommended)

- Start a change: `/opsx:new <kebab-case>`
- Create artifacts (step): `/opsx:continue <change>`
- Create artifacts (fast): `/opsx:ff <change>`
- Implement tasks: `/opsx:apply <change>`
- Verify before archive: `/opsx:verify <change>`
- Sync delta specs → main specs: `/opsx:sync <change>`
- Archive: `/opsx:archive <change>`

## Contributing & Merge Gates

When authoring or merging a PR (as a human contributor, a collaborator,
or an AI assistant acting on behalf of either), the binding workflow is
in [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md). The sections
an AI assistant most often needs are:

- [Merge gates](.github/CONTRIBUTING.md#merge-gates) — CI green +
  actionable CodeRabbit findings addressed + `mergeable=CLEAN` +
  OpenSpec change folder for behavior changes + `Fixes #N` /
  `Closes #N` for issue cover + the five simplicity rules
  (PRINCIPLES.md P1-P5; see
  [Simplicity gates](.github/CONTRIBUTING.md#simplicity-gates)).
- [Collaborator rules](.github/CONTRIBUTING.md#collaborator-rules) —
  no self-merge by default; large PRs get split (≈1-concern per PR,
  ~800 net lines / scoped capability ceiling).
- [Bus factor escape hatch](.github/CONTRIBUTING.md#bus-factor-escape-hatch)
  — self-merge allowed after **14 days** with all gates met and a
  comment invoking the clause.

An assistant preparing a merge MUST verify the gates against the
actual GitHub state (status check rollup, current-head CodeRabbit review
threads, `mergeable` field) rather than asserting them from local history.
Local `uv run pytest` / `uv run ruff` / `codex review --base origin/main`
are encouraged but not substitutes for the cloud gates.

## PR Readiness / Review Trapdoors

These rules encode recurring review blockers observed across codex-lb PRs.

- OpenSpec is a hard gate for behavior, API, schema, CLI,
  dashboard-visible, proxy-routing, operator-contract, and compatibility
  changes. Create or update `openspec/changes/<slug>/` before coding, keep
  `spec.md` normative with MUST/SHALL-style requirements, put rationale and
  examples in `context.md` or change notes, and run strict OpenSpec validation
  before calling the PR ready. Code/tests alone are not enough when OpenSpec is
  required.
- CodeRabbit review state must come from current-head GitHub evidence.
  Unresolved, non-outdated actionable review threads block readiness until
  their findings are fixed or explicitly addressed or dismissed in-thread;
  a top-level summary does not override active thread evidence.
- Proxy failover and retry patches must prove account ownership and settlement
  invariants. File-pinned requests must not cross accounts; API-key reservations
  must settle before error-health writes; excluded accounts must actually leave
  the selection loop; idle disconnects must not mark otherwise healthy accounts
  unhealthy; security/trusted-access routing must degrade only along the
  documented path.
- Async, fan-out, and session-lifecycle patches must prove task ownership and
  cleanup. Do not share one `AsyncSession` across concurrent tasks; cancel or
  await spawned tasks on failure; preserve finalization/settlement paths after
  partial errors; bound fan-out; and test partial-failure behavior, not only
  the all-success path.
- Database migrations must prove Alembic graph and data hygiene. New revisions
  must sit on the current intended parent with a single-head upgrade path, have
  downgrade/upgrade coverage where the project expects it, and include
  historical-row backfills or compatibility handling when new fields affect
  existing data.
- Issue-resolving PRs must name the exact `Fixes #N` / `Closes #N`, or state
  that they are partial. Keep PRs one concern wide. Revive stale work by making
  a focused branch on current `main`; do not drag an old broad/conflicted branch
  forward unless the maintainer explicitly wants that shape.
- Bug fixes need regression coverage at the externally failing product path:
  route, bridge, websocket, CLI, schema, dashboard UI, or migration path as
  applicable. Helper-only tests are not enough when the failing surface is
  elsewhere.
- Compatibility work must verify canonical and equivalent paths, trailing slash
  behavior, external error envelopes, env-var semantics, and response-schema
  contracts. Update OpenSpec/context and tests together so docs cannot promise
  behavior the code does not implement.
- Simplicity gates are a merge gate (`PRINCIPLES.md` +
  [CONTRIBUTING.md Simplicity gates](.github/CONTRIBUTING.md#simplicity-gates)).
  New features must default off or work zero-config; new `CODEX_LB_*` settings
  need a why-not-a-default justification in the PR body; README top-level
  sections, `.env.example`, and dashboard core-nav items are budgeted per
  `.github/simplicity-budgets.toml` and exceptions need the maintainer-applied
  `simplicity-budget-approved` label; feature documentation goes to `docs/` +
  openspec (never new README sections); dashboard-visible PRs include
  before/after screenshots.
