# Scope and observed baseline

## Goal

Create a first-party Falcone IAM service that replaces Keycloak's required capabilities and unifies Falcone authorization. Preserve the approved **Falcone** APIs, URLs, error contracts, identity context and tenant/workspace rules. Standard OIDC/OAuth interoperability remains required. Raw Keycloak Admin APIs, internal database schemas and operator-only passthrough routes are not automatically compatibility targets; their real usage must be inventoried before retirement.

This is a custom Falcone service, not a proposal to rename or deploy a different complete IAM product. The survey supplies proven design patterns, optional libraries and alternative paths.

## Evidence and implications

Baseline: [Falcone commit b694e45](https://github.com/gntik-ai/falcone/tree/b694e45e487b1c49238e30a544fb7076fc18a7d6). Exact source links are in [sources](sources.md).

| Observed in source | Implication for the replacement |
|---|---|
| Keycloak tenant realms and normalized IAM-admin requests; OIDC and SAML appear in the adapter catalog | Preserve product administration semantics; establish which federation profiles are actually used |
| A Falcone authorization model defines actor, tenant, workspace, scopes, effective roles, correlation and propagation targets | This is the starting contract; do not invent a parallel generic role model |
| `custom:` tenant roles are persisted by the control plane, with subset-of-creator and scope checks | Falcone already owns important RBAC; migrate authority deliberately rather than treating realm roles as the entire policy source |
| Both control-plane and executor paths contain identity and authorization enforcement | Both need qualification; replacing one verifier is insufficient |
| APISIX authenticates requests, strips caller context headers and uses downstream trust configuration | Backend resource authorization remains necessary; production must not inherit development trust shortcuts |
| Console sessions refresh through a Falcone login-session endpoint; current console stores its snapshot in sessionStorage | Keep the contract during migration; a BFF/cookie transition is a separate client change |
| Service-account invalidation is scoped by verified realm and client ID | Preserve this anti-collision property; improve to explicit credential versions where feasible |
| Realtime has JWT validation, subscription scope checks and scope-revocation suspension | Permission changes must reach existing WebSocket sessions, not only new handshakes |
| Per-bucket SeaweedFS identities and key rotation exist | Preserve bucket-level isolation and avoid accumulating grants on reused identities |
| Function invocation uses short-lived signed, audience- and body-bound credentials | Keep that internal contract until a versioned replacement is proven; ordinary user tokens are not a substitute |
| MCP uses curated registration and `mcp:<server>:<tool>` scopes | Retain Falcone policy and plan checks; do not expose unrestricted dynamic registration |
| PostgreSQL/RLS, FerretDB/document data, Kafka, OpenBao, LLM/BYOK, provisioning and observability participate in the platform | IAM needs adapters and ownership boundaries across the platform, not only login |

Comments and pure contract helpers do not establish end-to-end production enforcement. P0 produces runnable compatibility fixtures and a deployment inventory.

## Constraints carried forward

- Deploy on vanilla Kubernetes and restricted corporate OpenShift using namespaced ordinary workloads. No new operator, privileged pod or sandbox runtime is assumed available.
- User code is untrusted. IAM never executes tenant code or places its private keys in a tenant runtime. Container hardening is not a substitute for hostile-code isolation in the execution platform.
- Falcone manages quota definitions, plan entitlement decisions and accounting. IAM applies them and reports usage; it does not become a second billing engine.
- Integrate both current Keycloak-era Temporal/Knative consumers and proposed `falcone-workflow`/`falcone-serverless` contracts during migration. Those repositories are design/integration targets, not assumed deployed replacements.
- Previous figures of roughly 20 tenants, 10,000 **deployed functions**, and 100,000 messages/second describe the execution/event platform. Identity count, login rate, token rate, authorization calls and concurrent sessions remain unknown.

## Initial product boundary

Include local and federated identity, tenant/workspace memberships, sessions, MFA, OIDC/OAuth, machine identities, scoped delegation, custom roles, decisions, audit and revocation projections. Include enterprise connectors required by actual current usage; optional SAML/LDAP/SCIM breadth follows inventory and qualification.

Exclude custom cryptography, a replacement for OpenBao, global human-resources provisioning, a general-purpose workflow engine, unlimited tenant policy scripting, and a second resource database. Application teams continue to own resource facts and enforce decisions. The proposal does not assert full Keycloak feature parity, a production SLA or compatibility with unobserved plugins.
