# falcone-iam

Design and implementation backlog for **Falcone's custom identity and authorization service**, intended to replace Keycloak while preserving Falcone product contracts.

**Status: proposed architecture and planning artifacts; no IAM runtime has been implemented or deployed by this repository bootstrap.** Falcone remains the owner of tenant/workspace semantics, roles, entitlements and integration contracts. The design reuses maintained protocol and cryptographic libraries rather than creating new authentication protocols.

Research baseline: 2026-10-31. Falcone source examined at [`b694e45`](https://github.com/gntik-ai/falcone/tree/b694e45e487b1c49238e30a544fb7076fc18a7d6). Source presence is evidence of an integration contract, not proof that every path is deployed or production-qualified.

## Start here

| Document | Purpose |
|---|---|
| [Scope and observed baseline](docs/scope-and-baseline.md) | What exists, what changes, and what remains an assumption |
| [Open-source survey](docs/open-source-survey.md) | Keycloak plus 12 alternative projects, reusable patterns and trade-offs |
| [Architecture](docs/architecture.md) | Components, stack, ownership, data model and request flows |
| [Integration matrix](docs/integration-matrix.md) | Contracts for every identified Falcone subsystem |
| [Functional requirements](docs/requirements.md) | 84 testable requirements with story traceability |
| [Epics and stories](docs/backlog.md) | 14 epics and 42 stories with acceptance criteria and dependencies |
| [Security model](docs/security.md) | Trust boundaries, token lifecycle, revocation and threat controls |
| [Operations](docs/operations.md) | Proposed SLOs, sizing, restricted deployment and ownership |
| [Migration](docs/migration.md) | Inventory, import, canary, rollback and Keycloak retirement |
| [Decisions and alternatives](docs/decisions/0001-baseline.md) | Proposed choices and optional implementation paths |
| [Open questions](docs/open-questions.md) | Decisions needed before implementation/cutover |
| [Sources](docs/sources.md) | Primary sources and pinned Falcone evidence |

## Delivery plan

1. **P0 — qualify the boundary:** freeze Falcone contracts, establish actual identity load and enterprise federation needs, and qualify the protocol library.
2. **P1 — build the core:** identity lifecycle, scoped RBAC, OIDC, sessions, keys, machines, outbox and restricted deployment.
3. **P2 — integrate and qualify:** consoles, gateway, data/storage, realtime, workflows, functions, security review and recovery drills.
4. **P3 — migrate:** explicit dual-issuer trust, shadow decisions, tenant canaries, then separately approved Keycloak retirement.

See [GitHub issues](https://github.com/gntik-ai/falcone-iam/issues) for the tracked backlog. [CSV](docs/backlog.csv), [JSON](docs/backlog.json), [issue payloads](docs/issue-payloads.json) and the [issue map](docs/github-issues.json) support board population and traceability. GitHub Projects can add these repository issues; the CSV is a portable interchange file, not a claim that GitHub has a universal native CSV importer. Epic checklists and parent/dependency links express the hierarchy.

## Planning maintenance

Edit story definitions in `tools/build_docs.py`, then run `python3 tools/build_docs.py`. It validates dependency references/cycles and regenerates requirements, Markdown, JSON, CSV and issue bodies. Existing issue numbers come from `docs/github-issues.json`. Regeneration does not change remote issues automatically. Architecture and operational documents are maintained directly.

This repository does not yet select a project license or claim production readiness. The owner must choose the open-source license before code distribution; third-party licenses and commercial extensions are assessed separately.
