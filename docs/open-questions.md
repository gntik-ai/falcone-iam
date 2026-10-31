# Open questions and decision log

The architecture is concrete enough to start discovery without blocking this documentation/backlog publication. The following answers are required before the relevant implementation or production gates. Defaults are proposals, not inferred user approvals.

| Question | Proposed working assumption | Decision gate |
|---|---|---|
| Is TypeScript/Node.js acceptable for IAM, or must the service be Go? | Align with current Falcone JS contracts; qualify protocol library before commitment | P0 protocol ADR |
| Which open-source license should this repository use? | No license selected or third-party source copied by this bootstrap | Before code redistribution |
| Which Keycloak versions/extensions and native APIs are used in production? | Source adapter catalog is not a deployment inventory; preserve Falcone contracts only, inventory all direct dependencies | P0 / migration |
| Must current issuer URLs and subject IDs remain byte-for-byte stable? | Preserve Falcone principal identity via mappings; allow explicitly planned issuer transition | Before clients/token schema |
| How many users, sessions, machines, clients, groups and authorization checks are expected? | Prior message/function estimates are not identity capacity; benchmark a measured workload | P0 SLO/sizing |
| Which enterprise federation profiles are mandatory: inbound/outbound SAML, OIDC, LDAP/AD, SCIM? | OIDC baseline; every in-use profile gets parity or an explicit bridge | Before Keycloak retirement |
| Is automatic signup allowed, and who may invite, link or approve identities? | Tenant-controlled invitation, explicit linking, no email-only auto-merge | Identity lifecycle |
| Are built-in roles, custom: roles and current workspace semantics final? | Preserve pinned catalog and subset rules; changes need product review | Authorization contract |
| Do resources require sharing across workspaces or tenants? | Deny cross-tenant access by default; do not add a graph engine without concrete sharing semantics | Policy model |
| Which MFA methods and recovery channels are mandatory? Any FIPS or cryptographic constraints? | Passkeys/TOTP and step-up for administrators; reviewed password policy | Authentication/security |
| Is a BFF cookie-based console transition acceptable? | Maintain current session behavior for compatibility, plan a separate secure client migration | Console integration |
| Must revocation be under 30 seconds for direct S3/SQL/Kafka access, and can proxying be required? | Online Falcone paths target 30 seconds; direct backend guarantees must be tested individually | Security/SLO |
| What exact OpenShift release/build, network policy, arbitrary-UID and secret integration are permitted? | Namespaced nonprivileged application; administrator provides approved shared services | Deployment qualification |
| Which SeaweedFS releases and notification/identity modes are actually deployed? | Preserve current per-bucket credential behavior and verify selected releases | Storage adapter |
| Is OpenBao/KMS remote signing available, or is encrypted key material in service memory acceptable? | Prefer managed custody; qualify actual library/adapter and organizational requirements | Key-management ADR |
| What are the actual MCP specification/version, clients and transports? | Preserve observed curated registration/tool scopes; do not equate generic WebSockets with MCP auth requirements | MCP integration |
| Are workflow/serverless replacements implemented, and which adapter versions should be tested? | Maintain contracts for current Temporal/Knative and planned first-party replacements | Integration qualification |
| What audit retention, data residency, erasure and legal-hold policies apply? | Configurable policy, least-privilege access; no compliance claim | Production privacy review |
| Is single-region HA sufficient? What downtime/data loss is acceptable? | Provisional 99.95%, RPO 5 min, RTO 60 min; validate against infrastructure | SLO/DR acceptance |
| Who owns code, protocol patches, keys, on-call and independent security review? | Roles in operations.md; no named team assumed | Production readiness |
| What canary tenants, rollback window and forced reauthentication are acceptable? | Dry-run then explicit dual-issuer tenant canaries; no seamless-session promise | Migration go/no-go |

Record answers as ADR updates with owner, date, evidence and affected story IDs. New mandatory functionality should become an issue before P3; a documentation exception is not an implemented feature.
