# ADR 0001 — A Falcone-owned IAM service with qualified protocol components

Date: 2026-10-31. Status: **proposed**, pending P0 evidence and owner decisions. The request authorizes planning publication, not acceptance of every technical choice or production cutover.

Scope amendment: [ADR 0002](0002-mandatory-enterprise-protocols.md), accepted 2026-11-01, makes SAML, OIDC, LDAP/AD and SCIM mandatory. Other technical proposals in this ADR retain their status.

## Decision

Build a custom Falcone identity and authorization service. Retain Falcone contracts and permission semantics. Start with a modular TypeScript/Node.js service, a qualified `oidc-provider` adapter, PostgreSQL, OpenBao/KMS and Kafka outbox/projections. Separate protocol/API and worker deployments; avoid a large microservice topology until measured needs justify it.

Use scoped RBAC and bounded attributes as the initial authorization model, with a stable decision contract and revision metadata. Do not add a relationship engine unless product sharing requirements exceed that model. Keep resource facts and enforcement in the owning Falcone service.

## Why

Observed Falcone code already has custom role semantics, resource authorization and normalized context. Preserving them reduces product migration risk. Existing infrastructure supplies durable transactions, secret custody and event transport. Reusing a protocol library lowers specialist implementation scope while keeping Falcone's UI, administration and data ownership custom.

The major cost is taking responsibility for credential lifecycle, protocol configuration, key handling, migration, patching, security qualification and 24/7 failure recovery. Custom IAM must earn retirement of the existing provider through evidence.

## Options and trade-offs

| Option | Scalability | Developer experience | Operations | Falcone compatibility / decision |
|---|---|---|---|---|
| Custom Falcone core with embedded qualified protocol library | Replicate core; qualify database and signing bottlenecks | Reuses existing language/contracts; library extension boundaries matter | Fewer independently deployed services; team owns configuration and security lifecycle | Proposed baseline; protocol/persistence spike is a gate |
| Custom Go core with Fosite or equivalent library | Efficient service runtime; real limits still depend on data/crypto | Fits Go teams but requires new bridges to current JS contracts and more protocol assembly | Similar deployment count, different library expertise | Viable if team preference or required profiles rule out baseline; evaluate, do not claim interchangeability |
| Falcone core with Hydra protocol subsystem | Independently scale protocol and product APIs | Clear login/consent boundary; extra service contracts | Additional deployment, upgrade and edition/license qualification | Custom Falcone remains product owner; useful fallback if it reduces protocol risk |
| Transitional Keycloak authentication plus custom Falcone authorization | Gradual independent rollout | Faster validation of native permissions | Two systems and temporary reconciliation complexity | Migration phase, not the final requested replacement |
| Optional OpenFGA/SpiceDB for relationship sharing | Graph engines can scale checks; model fan-out matters | Better graph semantics, additional model expertise | Tuple projection and revision-consistency responsibilities | Defer until concrete cross-resource sharing requires it |
| Optional Cerbos/OPA/Casbin evaluation | Local or remote policy execution | More reusable policy tooling but another policy model/language | Distribution and policy-version drift need control | Preserve the decision interface; choose one only after parity benchmark |
| Optional shared cache / local decision agents | Lower repeated-check latency | Requires explicit cache contract | More failure modes and stale-state risk | Add only with revision leases and measured need |
| Dedicated issuer/data partitions for selected tenants | Stronger fault/noisy-neighbor boundaries | Same product contract | Higher operational cost and migration work | Optional premium isolation, not a blanket requirement for ~20 tenants |
| BFF sessions and passkey-first experience | Reduces exposed browser bearer tokens; backend state needed | Improved browser session control but changes console integration | Cookie/CSRF and websocket handshake qualification | Recommended evolution with explicit rollout; does not describe current console behavior |

## Hard boundaries

No new cryptographic algorithms, handwritten OAuth stack, arbitrary tenant IAM plugins, blanket shared admin credentials or unlimited offline authorization. No new cluster-level operator is required by the baseline. IAM remains usable when workflow or serverless is unavailable. Libraries, project license, concrete enterprise provider/profile details and actual OpenShift support remain explicit qualification decisions; support for all four enterprise protocol families is mandatory.
