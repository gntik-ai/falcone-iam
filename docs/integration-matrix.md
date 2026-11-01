# Falcone integration matrix

Source-derived inventory at the pinned baseline; exact deployed capabilities and integration tests remain P0/P2 work. IAM changes only identity/authorization boundaries; it does not replace these services. Every row requires negative tenant/workspace tests, credential expiry and revocation evidence.

| Consumer | Required contract / responsibility | Qualification and failure behavior |
|---|---|---|
| APISIX | OIDC/JWKS trust, route audiences, stripped identity headers, authenticated downstream context | Wrong issuer/audience or direct forged context fails; trusted key cache is bounded and scoped by issuer/key/algorithm |
| Control plane and executor | Existing Falcone auth/admin APIs, custom roles, effective-permission recalculation and normalized security context | Test both implementations. No production unverified identity mode or undocumented internal bypass |
| Current and next console | Login states, session refresh/logout, tenant/workspace switch, role-aware UI and recovery | UI visibility is not backend authorization. Test refresh races, global revoke, MFA and redirect restoration |
| SDKs, CLI and external apps | Discovery, PKCE, client registration, API keys on approved routes, normalized errors | Browser clients cannot keep confidential secrets. Native redirect handling is separately qualified |
| Corporate SAML/OIDC providers and SAML applications | Mandatory tenant-scoped federation adapters, provider metadata, subject mappings and application SSO | Authenticate to the same Falcone principal; verify audience, trust, replay, certificate/key rotation and session behavior |
| LDAP directories and Active Directory | Mandatory secure bind/search and user/group lifecycle synchronization | Test generic LDAP and AD, TLS and applicable directory policy, stable IDs, group mapping and detection lag; directory credentials stay upstream |
| SCIM provisioning clients and target applications | Mandatory SCIM 2.0 User/Group lifecycle endpoints and managed outbound adapters | Authenticate tenant-scoped connectors; apply attribute authority, conflict handling, idempotent reconciliation and Falcone deprovisioning/revocation |
| PostgreSQL data API / direct access | Role and RLS projections, tenant/workspace and correlation context | Reset connection-pool state; transaction-scoped context; direct credentials and active sessions need their own revocation mechanism |
| FerretDB / document layer | Equivalent query filters and scoped credentials for supported paths | Filter before pagination/counts; verify actual engine behavior rather than assuming PostgreSQL RLS covers every document request |
| SeaweedFS S3 | Per-bucket identity/action projection, programmatic credentials, presigned access, rotation/revocation | Prevent merge-based grant accumulation. Test chosen stable releases and actual filer/notification configuration; no claim that arbitrary SeaweedFS supports every AWS IAM/STS feature |
| Kafka and event bus | Publish/consume permission, trusted tenant envelope, ACL or gateway projection | Authentication of producer is distinct from authority carried in an event; replay cannot grant a removed role |
| Realtime/WebSockets | Upgrade identity, subscription scope and periodic freshness checks | Push invalidation plus bounded revalidation; token expiration or role removal suspends access even without reconnect |
| Webhooks and callbacks | Per-endpoint secret or authenticated callback identity, execution binding, replay prevention | A valid signature does not authorize another tenant or unrelated execution; retry preserves event ID |
| Current Knative/function runtime | Existing audience/body-bound invocation credentials, workspace authorization | Runtime accepts only invocation purpose; issuer/signature contract changes are versioned and tested |
| `falcone-serverless` | Versioned delegation, machine credential renewal, quota and audit context | No IAM secret mounts in tenant code. Permission loss blocks new sensitive operations; execution isolation remains runtime ownership |
| Current Temporal adapters | Service identity, worker permissions, activity delegation and secret references | Do not store user refresh tokens in workflow histories; authorize resumed activity and callbacks |
| `falcone-workflow` | Same Falcone actor/delegation contract across durable execution and retries | IAM must work while workflow is down; noncritical IAM integrations may emit events but cannot depend on this engine to authenticate |
| MCP server/gateway | Curated registration, client/resource audience and `mcp:<server>:<tool>` scopes | Check each tool call; distinguish actual Model Context Protocol profiles from generic event transports. Pin version after inventory |
| OpenBao and LLM/BYOK | Tenant-bound secret handles, least-privilege service access, credential usage audit | IAM does not become an arbitrary secret proxy; never return unrelated BYOK material via identity exports |
| Provisioning orchestrator | Idempotent realm/client/user/role/scope lifecycle requests and status | Provisioning retries cannot expand grants. Required actions and application templates need mapping from current adapters |
| Plans, quota and metering | Authoritative Falcone entitlement decision and usage events | Failed attempts, retries, cold starts and idle execution accounting remain defined by Falcone; IAM abuse limits complement rather than replace product quota rules |
| Audit, metrics and SIEM | Stable event IDs, actor and decision correlation, redacted logs | Durable security changes are never silently unaudited; telemetry outages have bounded buffers and alerts |
| Backup/restore and platform automation | Explicit service credentials, separation of duties and recovery epoch | Restored snapshots must not revive revoked sessions or keys; automation uses dedicated machine accounts |

## Projection contract

Suggested event fields: event ID, schema version, tenant/workspace, entity type/ID, monotonic aggregate version, event type, occurred-at timestamp, actor/correlation reference and changed-state reference. Do not put bearer tokens, password verifiers or secret bytes on the event bus. Consumers store their last applied version and report `pending`, `applied`, `failed` or `reconciling`, plus revision and timestamp. Kafka partitioning preserves per-aggregate order where possible; version checks remain required after retry or replay.

Initial events include principal suspended, membership changed, effective permissions changed, credential rotated/revoked, client changed, tenant suspended and key metadata changed. Exact names adapt existing Falcone event contracts, including `tenant.effective_permissions.recalculate`; introduce aliases/versioning rather than an unannounced rename.

## Direct access limitations

JWT validation, S3 credentials, SQL sessions, Kafka consumers and WebSockets have different revocation mechanisms. A single IAM transaction cannot make all backends atomically revoke access. Publish the maximum allowed stale interval for each path and reject new grants when its enforcement state is too old. For direct presigned URLs, guarantee only the tested expiry/key-removal behavior; use a scoped proxy if stronger per-request revocation is required. An object already downloaded cannot be recalled.
