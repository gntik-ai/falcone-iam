# Functional requirements

Planning baseline: 2026-11-01. Each statement is testable and traces to one story. All requirements describe the target, not delivered functionality. See [architecture](architecture.md), [security](security.md) and [operations](operations.md) for normative design detail.

## Falcone contracts and ownership

| ID | Requirement | Story |
|---|---|---|
| FR-CON-001-1 | The system must preserve the approved Falcone IAM API paths, response schemas, errors and tenant/workspace semantics in a versioned contract suite. | [IAM-CON-001](https://github.com/gntik-ai/falcone-iam/issues/15) |
| FR-CON-001-2 | The migration inventory must classify every identity consumer and native Keycloak dependency as retained, adapted or retired. | [IAM-CON-001](https://github.com/gntik-ai/falcone-iam/issues/15) |
| FR-CON-002-1 | The system must document one authoritative writer and a versioned projection contract for every shared identity and authorization entity. | [IAM-CON-002](https://github.com/gntik-ai/falcone-iam/issues/16) |
| FR-CON-002-2 | The system must consume Falcone plan and quota decisions without maintaining a second independently editable entitlement catalog. | [IAM-CON-002](https://github.com/gntik-ai/falcone-iam/issues/16) |
| FR-CON-003-1 | The implementation must use maintained cryptographic and OIDC/OAuth libraries with pinned versions, dependency provenance and an upgrade owner. | [IAM-CON-003](https://github.com/gntik-ai/falcone-iam/issues/17) |
| FR-CON-003-2 | The release process must run the chosen OIDC conformance profile and documented OAuth negative tests against the configured Falcone service. | [IAM-CON-003](https://github.com/gntik-ai/falcone-iam/issues/17) |

## Identity, tenancy and membership lifecycle

| ID | Requirement | Story |
|---|---|---|
| FR-IDN-001-1 | The system must identify principals with immutable IDs and represent tenant/workspace membership separately from profile attributes. | [IAM-IDN-001](https://github.com/gntik-ai/falcone-iam/issues/18) |
| FR-IDN-001-2 | Every identity lookup and mutation must enforce its tenant boundary, including when two issuers use the same subject or client identifier. | [IAM-IDN-001](https://github.com/gntik-ai/falcone-iam/issues/18) |
| FR-IDN-002-1 | The system must support expiring single-use invitations, activation, suspension, reactivation and membership removal through Falcone APIs. | [IAM-IDN-002](https://github.com/gntik-ai/falcone-iam/issues/19) |
| FR-IDN-002-2 | Lifecycle mutations must commit an audit record and durable propagation event with their authoritative state change. | [IAM-IDN-002](https://github.com/gntik-ai/falcone-iam/issues/19) |
| FR-IDN-003-1 | The system must require fresh authentication and proof of both identities before linking local and federated accounts. | [IAM-IDN-003](https://github.com/gntik-ai/falcone-iam/issues/20) |
| FR-IDN-003-2 | The system must support verified email changes and configurable profile fields without allowing clients to set tenant, role or entitlement claims. | [IAM-IDN-003](https://github.com/gntik-ai/falcone-iam/issues/20) |

## Login, MFA and recovery

| ID | Requirement | Story |
|---|---|---|
| FR-AUT-001-1 | The system must hash local passwords using a reviewed adaptive password-hashing library and configurable cost policy, never reversible encryption. | [IAM-AUT-001](https://github.com/gntik-ai/falcone-iam/issues/21) |
| FR-AUT-001-2 | The system must rate-limit login, signup and recovery attempts by multiple signals and return non-enumerating public failure responses. | [IAM-AUT-001](https://github.com/gntik-ai/falcone-iam/issues/21) |
| FR-AUT-002-1 | The system must support WebAuthn credentials and TOTP with audited enrollment, removal and recovery-code lifecycle. | [IAM-AUT-002](https://github.com/gntik-ai/falcone-iam/issues/22) |
| FR-AUT-002-2 | The system must require policy-defined recent MFA for administrator access and high-risk credential or permission changes. | [IAM-AUT-002](https://github.com/gntik-ai/falcone-iam/issues/22) |
| FR-AUT-003-1 | The system must expose the existing login, signup, pending activation, suspended, expired credentials and password recovery states through Falcone contracts. | [IAM-AUT-003](https://github.com/gntik-ai/falcone-iam/issues/23) |
| FR-AUT-003-2 | Password resets must use expiring single-use secrets and revoke affected sessions according to the documented recovery policy. | [IAM-AUT-003](https://github.com/gntik-ai/falcone-iam/issues/23) |

## OIDC, OAuth and sessions

| ID | Requirement | Story |
|---|---|---|
| FR-SES-001-1 | The system must provide OIDC discovery, JWKS, authorization, token and user-info endpoints for explicitly configured platform and tenant issuers. | [IAM-SES-001](https://github.com/gntik-ai/falcone-iam/issues/24) |
| FR-SES-001-2 | Public clients must use authorization code with PKCE S256, exact registered redirects and state/nonce validation; implicit and password grants must be disabled. | [IAM-SES-001](https://github.com/gntik-ai/falcone-iam/issues/24) |
| FR-SES-002-1 | The system must rotate refresh tokens atomically, persist only protected token representations and invalidate a token family on confirmed reuse. | [IAM-SES-002](https://github.com/gntik-ai/falcone-iam/issues/25) |
| FR-SES-002-2 | The system must preserve Falcone session refresh/logout behavior and allow authorized users to list and revoke their sessions. | [IAM-SES-002](https://github.com/gntik-ai/falcone-iam/issues/25) |
| FR-SES-003-1 | The system must expose authenticated introspection and revocation interfaces and define a measurable freshness bound for every enforcement surface. | [IAM-SES-003](https://github.com/gntik-ai/falcone-iam/issues/26) |
| FR-SES-003-2 | Authorization decisions must return the effective policy revision and refuse a minimum revision that cannot be satisfied. | [IAM-SES-003](https://github.com/gntik-ai/falcone-iam/issues/26) |

## Falcone permissions and policy decisions

| ID | Requirement | Story |
|---|---|---|
| FR-RBAC-001-1 | The system must preserve the approved platform, tenant and workspace roles and resource/action permission matrix from Falcone internal contracts. | [IAM-RBAC-001](https://github.com/gntik-ai/falcone-iam/issues/27) |
| FR-RBAC-001-2 | Custom role creation and assignment must enforce namespace, scope, reserved-name and subset-of-delegable-permissions constraints. | [IAM-RBAC-001](https://github.com/gntik-ai/falcone-iam/issues/27) |
| FR-RBAC-002-1 | The system must evaluate trusted actor, tenant, workspace, action, resource, scopes and delegation context with deny-by-default behavior. | [IAM-RBAC-002](https://github.com/gntik-ai/falcone-iam/issues/28) |
| FR-RBAC-002-2 | Single and batch authorization APIs must return Falcone decision IDs, effect, reason, matched policies, effective roles and correlation context. | [IAM-RBAC-002](https://github.com/gntik-ai/falcone-iam/issues/28) |
| FR-RBAC-003-1 | The system must publish scoped projections for data, function, event and storage consumers with version and delegation context. | [IAM-RBAC-003](https://github.com/gntik-ai/falcone-iam/issues/29) |
| FR-RBAC-003-2 | Conditional policies must use a bounded approved schema with deterministic evaluation and explicit missing-attribute behavior. | [IAM-RBAC-003](https://github.com/gntik-ai/falcone-iam/issues/29) |

## Machine identities and delegated execution

| ID | Requirement | Story |
|---|---|---|
| FR-MAC-001-1 | The system must create, disable, rotate and revoke service-account credentials with tenant/workspace, scope and audience restrictions. | [IAM-MAC-001](https://github.com/gntik-ai/falcone-iam/issues/30) |
| FR-MAC-001-2 | API-key secrets must be shown only at issuance and stored as non-recoverable verifiers with a public identifier for lookup. | [IAM-MAC-001](https://github.com/gntik-ai/falcone-iam/issues/30) |
| FR-MAC-002-1 | Delegated credentials must identify actor and subject, restrict resource audience and intersect all parent scopes and tenant/workspace boundaries. | [IAM-MAC-002](https://github.com/gntik-ai/falcone-iam/issues/31) |
| FR-MAC-002-2 | Serverless and workflow execution must renew authorized machine credentials without persisting human refresh tokens in runtime payloads or histories. | [IAM-MAC-002](https://github.com/gntik-ai/falcone-iam/issues/31) |
| FR-MAC-003-1 | The system must support authenticated confidential clients with policy-controlled secret rotation and an asymmetric client-authentication option. | [IAM-MAC-003](https://github.com/gntik-ai/falcone-iam/issues/32) |
| FR-MAC-003-2 | Workload identity exchange must verify an allowlisted issuer, audience and subject binding before issuing a Falcone credential. | [IAM-MAC-003](https://github.com/gntik-ai/falcone-iam/issues/32) |

## Federation, external applications and MCP

| ID | Requirement | Story |
|---|---|---|
| FR-FED-001-1 | The system must support tenant-scoped upstream OIDC providers with validated issuer, signing keys, redirects and claim mappings. | [IAM-FED-001](https://github.com/gntik-ai/falcone-iam/issues/33) |
| FR-FED-001-2 | Federated login must map verified external subjects to explicit Falcone memberships without granting privileges from untrusted group names. | [IAM-FED-001](https://github.com/gntik-ai/falcone-iam/issues/33) |
| FR-FED-002-1 | The system must support SAML 2.0, OpenID Connect, LDAP including Active Directory integration, and SCIM 2.0 as mandatory product capabilities. | [IAM-FED-002](https://github.com/gntik-ai/falcone-iam/issues/34) |
| FR-FED-002-2 | Keycloak retirement must require passing integration and security evidence for all four protocol families, regardless of whether current tenants already use each one. | [IAM-FED-002](https://github.com/gntik-ai/falcone-iam/issues/34) |
| FR-FED-003-1 | External application and MCP clients must use Falcone tenant/workspace registration policies, redirect validation and existing plan limits. | [IAM-FED-003](https://github.com/gntik-ai/falcone-iam/issues/35) |
| FR-FED-003-2 | MCP authorization must enforce the approved mcp:<server>:<tool> scope mapping and resource audience at each tool invocation. | [IAM-FED-003](https://github.com/gntik-ai/falcone-iam/issues/35) |
| FR-FED-004-1 | The system must implement tenant-scoped SAML 2.0 service-provider and identity-provider adapters with metadata, trusted certificate lifecycle and approved attribute mappings. | [IAM-FED-004](https://github.com/gntik-ai/falcone-iam/issues/57) |
| FR-FED-004-2 | SAML authentication must resolve to the same Falcone principal, membership, MFA policy and authorization contracts as OIDC authentication. | [IAM-FED-004](https://github.com/gntik-ai/falcone-iam/issues/57) |
| FR-FED-005-1 | The system must connect to generic LDAPv3 directories and Active Directory over validated TLS using scoped connector credentials and configured authentication methods. | [IAM-FED-005](https://github.com/gntik-ai/falcone-iam/issues/58) |
| FR-FED-005-2 | Directory synchronization must map stable external identities and groups to Falcone memberships, propagate disabling/removal and preserve explicit attribute ownership. | [IAM-FED-005](https://github.com/gntik-ai/falcone-iam/issues/58) |
| FR-FED-006-1 | The system must implement tenant-scoped SCIM 2.0 User and Group provisioning with discovery, lifecycle operations, group membership and protected connector credentials. | [IAM-FED-006](https://github.com/gntik-ai/falcone-iam/issues/59) |
| FR-FED-006-2 | SCIM inbound and outbound adapters must apply Falcone identity ownership, role-delegation limits, audit and revocation rules without cross-tenant grants or synchronization loops. | [IAM-FED-006](https://github.com/gntik-ai/falcone-iam/issues/59) |

## Keys, secrets and bootstrap trust

| ID | Requirement | Story |
|---|---|---|
| FR-KEY-001-1 | The system must store signing material and sensitive recoverable secrets using approved OpenBao/KMS-backed protection with least-privilege access. | [IAM-KEY-001](https://github.com/gntik-ai/falcone-iam/issues/36) |
| FR-KEY-001-2 | Key rotation must publish new public keys before use, retain required verification overlap and support emergency compromise handling. | [IAM-KEY-001](https://github.com/gntik-ai/falcone-iam/issues/36) |
| FR-KEY-002-1 | Initial privileged ownership must be created through a one-time authenticated bootstrap process that becomes unavailable after completion. | [IAM-KEY-002](https://github.com/gntik-ai/falcone-iam/issues/37) |
| FR-KEY-002-2 | Emergency access must have explicit scope, expiry, strong authentication and an immutable audit trail. | [IAM-KEY-002](https://github.com/gntik-ai/falcone-iam/issues/37) |
| FR-KEY-003-1 | IAM and adapters must reference recoverable backend credentials through scoped secret handles rather than plaintext event or workflow payloads. | [IAM-KEY-003](https://github.com/gntik-ai/falcone-iam/issues/38) |
| FR-KEY-003-2 | Export and backup functions must enforce separate permissions for identity metadata, password verifiers and recoverable key material. | [IAM-KEY-003](https://github.com/gntik-ai/falcone-iam/issues/38) |

## Falcone service integrations

| ID | Requirement | Story |
|---|---|---|
| FR-INT-001-1 | APISIX and Falcone backends must validate configured issuers and audiences and strip caller-controlled identity-context headers. | [IAM-INT-001](https://github.com/gntik-ai/falcone-iam/issues/39) |
| FR-INT-001-2 | Both control-plane paths, both consoles and supported SDKs must pass the approved login, refresh, authorization and error compatibility fixtures. | [IAM-INT-001](https://github.com/gntik-ai/falcone-iam/issues/39) |
| FR-INT-002-1 | Data and storage adapters must enforce scoped authorization on both credential issuance and resource use, including direct protocol access. | [IAM-INT-002](https://github.com/gntik-ai/falcone-iam/issues/40) |
| FR-INT-002-2 | SeaweedFS identity projections must preserve per-bucket privilege isolation and expose rotation, revocation and reconciliation status. | [IAM-INT-002](https://github.com/gntik-ai/falcone-iam/issues/40) |
| FR-INT-003-1 | Kafka/event ingress, realtime gateways and webhooks must preserve verified actor and tenant/workspace context without treating it as an unrestricted bearer credential. | [IAM-INT-003](https://github.com/gntik-ai/falcone-iam/issues/41) |
| FR-INT-003-2 | Current Temporal/Knative and future falcone-workflow/falcone-serverless adapters must implement the same versioned delegation and revocation contract. | [IAM-INT-003](https://github.com/gntik-ai/falcone-iam/issues/41) |

## Revocation and durable propagation

| ID | Requirement | Story |
|---|---|---|
| FR-REV-001-1 | Every security-state mutation must atomically persist its event in an outbox and deliver it with at-least-once semantics. | [IAM-REV-001](https://github.com/gntik-ai/falcone-iam/issues/42) |
| FR-REV-001-2 | Projection consumers must be idempotent, reject obsolete versions and expose applied revision and reconciliation state. | [IAM-REV-001](https://github.com/gntik-ai/falcone-iam/issues/42) |
| FR-REV-002-1 | Revocation must target sessions, refresh families, service credentials, authorization caches and registered backend projections with per-surface status. | [IAM-REV-002](https://github.com/gntik-ai/falcone-iam/issues/43) |
| FR-REV-002-2 | Long-lived connections and executions must revalidate authorization on a bounded schedule and on sensitive operations. | [IAM-REV-002](https://github.com/gntik-ai/falcone-iam/issues/43) |
| FR-REV-003-1 | Tenant suspension must deny new authorization before asynchronous cleanup begins and expose cleanup progress through Falcone APIs. | [IAM-REV-003](https://github.com/gntik-ai/falcone-iam/issues/44) |
| FR-REV-003-2 | Deletion must follow configurable retention, legal-hold and tombstone rules without reusing principal or tenant identifiers. | [IAM-REV-003](https://github.com/gntik-ai/falcone-iam/issues/44) |

## Audit, privacy and support visibility

| ID | Requirement | Story |
|---|---|---|
| FR-AUD-001-1 | The system must audit authentication, credential, membership, role, key and administrative changes with actor, tenant, outcome, revision and correlation ID. | [IAM-AUD-001](https://github.com/gntik-ai/falcone-iam/issues/45) |
| FR-AUD-001-2 | Audit access and export must be separately authorized and must redact secrets and unnecessary personal information. | [IAM-AUD-001](https://github.com/gntik-ai/falcone-iam/issues/45) |
| FR-AUD-002-1 | The system must expose authorized decision explanations that redact policies and resources outside the caller scope. | [IAM-AUD-002](https://github.com/gntik-ai/falcone-iam/issues/46) |
| FR-AUD-002-2 | Identity and audit data must have configurable retention, export and erasure behavior with documented legal-hold exceptions. | [IAM-AUD-002](https://github.com/gntik-ai/falcone-iam/issues/46) |
| FR-AUD-003-1 | The system must export structured logs, metrics and traces using Falcone observability conventions without unbounded user-ID metric labels. | [IAM-AUD-003](https://github.com/gntik-ai/falcone-iam/issues/47) |
| FR-AUD-003-2 | The system must provide authenticated audit export and alerts for abuse, key failure, authorization errors and projection lag. | [IAM-AUD-003](https://github.com/gntik-ai/falcone-iam/issues/47) |

## Deployment, reliability and ownership

| ID | Requirement | Story |
|---|---|---|
| FR-OPS-001-1 | The baseline deployment must run with arbitrary non-root UID, dropped capabilities, read-only root filesystem and no privileged or host access. | [IAM-OPS-001](https://github.com/gntik-ai/falcone-iam/issues/48) |
| FR-OPS-001-2 | Installation must use ordinary namespaced workloads without requiring a custom operator, CRDs, cluster-admin or a sandbox runtime. | [IAM-OPS-001](https://github.com/gntik-ai/falcone-iam/issues/48) |
| FR-OPS-002-1 | The project must benchmark token issuance, password login, authorization checks, refresh, key lookup and revocation separately. | [IAM-OPS-002](https://github.com/gntik-ai/falcone-iam/issues/49) |
| FR-OPS-002-2 | The project must define availability, latency, recovery and freshness objectives with a documented workload, topology and measurement boundary. | [IAM-OPS-002](https://github.com/gntik-ai/falcone-iam/issues/49) |
| FR-OPS-003-1 | The service must provide tested backup, restore, schema migration and rollback procedures covering identity state, key access and revocation state. | [IAM-OPS-003](https://github.com/gntik-ai/falcone-iam/issues/50) |
| FR-OPS-003-2 | Production release must name runtime maintainers, on-call responders, security qualification owners and product decision owners. | [IAM-OPS-003](https://github.com/gntik-ai/falcone-iam/issues/50) |

## Keycloak migration and retirement

| ID | Requirement | Story |
|---|---|---|
| FR-MIG-001-1 | Migration tooling must dry-run and report users, issuer-subject mappings, memberships, roles, clients, federation and credential portability without modifying production. | [IAM-MIG-001](https://github.com/gntik-ai/falcone-iam/issues/51) |
| FR-MIG-001-2 | The importer must be idempotent, tenant-scoped and produce reconciled counts and a report of unsupported or conflicting objects. | [IAM-MIG-001](https://github.com/gntik-ai/falcone-iam/issues/51) |
| FR-MIG-002-1 | Migration mode must explicitly allowlist old and new issuers, audiences and principal mappings without accepting arbitrary token sources. | [IAM-MIG-002](https://github.com/gntik-ai/falcone-iam/issues/52) |
| FR-MIG-002-2 | Tenant canaries must compare authorization outcomes and projection completion before switching the authoritative writer. | [IAM-MIG-002](https://github.com/gntik-ai/falcone-iam/issues/52) |
| FR-MIG-003-1 | Keycloak retirement must require signed-off compatibility, security, recovery and operational readiness evidence for every in-use integration and all mandatory SAML, OIDC, LDAP/AD and SCIM capabilities. | [IAM-MIG-003](https://github.com/gntik-ai/falcone-iam/issues/53) |
| FR-MIG-003-2 | Retirement must revoke obsolete credentials and trust entries, archive required audit evidence and remove approved legacy routes. | [IAM-MIG-003](https://github.com/gntik-ai/falcone-iam/issues/53) |

## Developer experience and release qualification

| ID | Requirement | Story |
|---|---|---|
| FR-DEV-001-1 | The project must publish OpenAPI and event schemas plus TypeScript and Go integration examples for the approved contracts. | [IAM-DEV-001](https://github.com/gntik-ai/falcone-iam/issues/54) |
| FR-DEV-001-2 | Development fixtures must include multiple tenants, machines, custom roles, expired credentials and negative authorization cases. | [IAM-DEV-001](https://github.com/gntik-ai/falcone-iam/issues/54) |
| FR-DEV-002-1 | Release builds must pin dependencies and publish an SBOM, signed image provenance and migration compatibility notes. | [IAM-DEV-002](https://github.com/gntik-ai/falcone-iam/issues/55) |
| FR-DEV-002-2 | The project must define security patch ownership, vulnerability reporting and dependency update qualification. | [IAM-DEV-002](https://github.com/gntik-ai/falcone-iam/issues/55) |
| FR-DEV-003-1 | A release candidate must pass tenant-isolation, protocol-negative, credential-replay and recovery tests for mandatory SAML, OIDC, LDAP/AD and SCIM profiles as well as other enabled integrations. | [IAM-DEV-003](https://github.com/gntik-ai/falcone-iam/issues/56) |
| FR-DEV-003-2 | Production cutover must require independent security review of authentication, authorization, key custody and deployment configuration. | [IAM-DEV-003](https://github.com/gntik-ai/falcone-iam/issues/56) |

