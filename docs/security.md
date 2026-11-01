# Security and trust model

This document defines proposed release requirements, not an assertion that the system is secure or implemented. Security qualification is part of replacing an identity service.

## Trust boundaries

The public browser/API boundary, gateway-to-backend boundary, tenant/workspace boundary, IAM-to-secret-custodian boundary and trusted-control-plane-to-untrusted-runtime boundary are separate. Tenant code cannot run in an IAM process or load IAM plugins. Extensions are reviewed platform-owned adapters with bounded inputs, timeouts and explicit permissions.

Tenant IDs, role lists and resource ownership supplied by clients are claims to validate, never authorization evidence. Authenticate gateway context or revalidate the original token at the backend; never trust the presence of `X-Tenant-Id` or similar headers alone. Preserve APISIX stripping and authenticated forwarding. Development shortcuts must fail startup in production configuration.

Identity and token signing are not runtime isolation. Without an approved sandbox, the serverless platform must explicitly own residual hostile-code risks, egress restrictions and node isolation. A compromised workload credential must be bounded to its audience, resource and lifetime.

SAML, OIDC, LDAP/AD and SCIM are mandatory integration surfaces. Apply the [enterprise profile](enterprise-federation.md) to XML-signature validation, directory transport/bind policy and provisioning authority. External identity/group assertions cannot bypass Falcone role-delegation limits. Connector credentials and metadata changes require scoped administration and audit.

## Authentication and sessions

- Use a qualified OIDC provider and maintained JOSE, password-hashing and WebAuthn implementations. Pin allowed algorithms; reject unsigned tokens, key-type confusion and unknown token purposes.
- Apply [OAuth Security BCP, RFC 9700](https://datatracker.ietf.org/doc/html/rfc9700): authorization code with PKCE, exact redirect matching, issuer checks, constrained token audiences and refresh protection. Disable implicit and password grants. Falcone-owned login interactions do not require exposing passwords to OAuth clients.
- Bind authorization requests to the client, tenant issuer, callback, state/nonce and short-lived interaction. Validate corporate discovery URLs against SSRF policy; do not fetch arbitrary `jku`, `x5u` or issuer URLs from tokens.
- Use measured adaptive password hashing; encrypt only data that must be recovered, such as TOTP or federation secrets. Recovery codes and high-entropy API-key verifiers are non-recoverable. Authentication failures are non-enumerating; abuse controls combine account, tenant, client and network signals.
- Require MFA and fresh step-up for privileged grants, recovery changes and key/credential operations. WebAuthn checks RP ID/origin/challenge/user verification. Recovery must not be a weaker route around administrator MFA.
- Refresh rotation is transactional and single-use. Store hashed token identifiers or equivalently protected provider state; reuse invalidates the family under the reviewed race policy. Refresh rechecks active membership, session and credential version.
- Proposed initial access-token lifetime is five minutes, with shorter execution credentials; this is a sizing/security hypothesis. Idle and absolute session limits are separate, configurable policy. Short JWT lifetime alone is not immediate revocation.
- For browser evolution, prefer a same-origin BFF with Secure, HttpOnly, appropriately SameSite cookies and CSRF protection when compatible with Falcone. Existing sessionStorage clients need an explicit transition and XSS controls; do not silently claim they already use cookies. WebSocket credentials must not appear in query-string logs; use the qualified cookie or short-lived handshake mechanism supported by the actual client.

## Authorization and credential versioning

Separate human subjects, machine principals, application clients and delegated actors. Bind client-credentials tokens to their tenant and service account. Where possible use an explicit monotonically increasing credential/security version rather than timestamp-only invalidation; this avoids same-second ambiguity in the observed legacy invalidation watermark.

Custom roles remain bounded by the creator's delegation set, the canonical action catalog and tenant/workspace scope. A service may act on behalf of a user only through explicit delegation, never by changing the subject header. A parent grant caps every child grant. Plan entitlement is an additional limit, not evidence of permission.

Protected writes, permission changes and secret issuance require current authoritative decisions. Cache entries include scope and policy/credential revision; no cache fallback may convert an error into allow. A service unable to satisfy a required policy revision must fail or retry within a deadline. Return detailed explanations only to authorized operators; public denial responses avoid resource enumeration.

## Revocation guarantees to qualify

| Surface | Proposed behavior | Limitation / failure handling |
|---|---|---|
| Login, token issuance, refresh and permission changes | Read authoritative state; suspension takes effect at committed state | Database unavailability denies these operations |
| Online Falcone APIs and sensitive delegated actions | Push invalidation plus maximum 30-second freshness lease; current decision for highest-risk actions | A disconnected consumer denies after lease expiry; network partition does not justify indefinite cached grants |
| Offline/local JWT profile, only where approved | Token lifetime bounds stale acceptance; proposed maximum five minutes | Explicit exception with owner and threat acceptance; not the default for administrative or secret access |
| WebSockets | Invalidate affected subscription and periodically revalidate within the online bound | Token expiry/role loss suspends delivery; queued messages must be checked before release where sensitive |
| Service-account/API credentials | Version invalidation plus provider/backend credential removal | Report IAM invalidation separately from backend-applied status; unknown credential state denies |
| Database sessions | Revoke role/credential and reap or reauthorize affected active sessions | Rotation alone may not end an already authenticated connection; qualify actual pool/protocol behavior |
| S3 keys / presigned URLs | Project key revocation and bound URL lifetime | Direct URL invalidation depends on backend behavior; no blanket immediate guarantee. Use a proxy if mandatory |
| Running functions/workflows | Reauthorize new sensitive operations and credential renewal; cancel where supported | Already executed external side effects cannot be undone; checkpoint/compensation is owned by execution services |

The 30-second target includes transport, consumer processing and local cache lease, with clock skew accounted for; it is not 30 seconds per stage. Measure from authoritative commit to denial in each consumer. A global revoke operation returns per-target progress and exceptions. Event delivery is at least once, never marketed as exactly-once distributed revocation.

For LDAP/AD and SCIM-originated changes, measure external detection/delivery delay separately from this internal bound. Configure directory synchronization freshness and provisioning outage policies explicitly; an upstream account change is not yet an authoritative Falcone commit. Removing a membership through one tenant connector must not disable unrelated tenant memberships.

## Keys, bootstrap and recovery

Use separate signing and encryption purposes, explicit key versions, least-privilege OpenBao/KMS access and approved algorithms. Stage public keys before signing, retain overlap for the accepted token lifetime plus skew, and test mixed-replica rotations. Emergency compromise handling may intentionally invalidate sessions and availability; the incident commander owns that decision.

Remote signing must work with the chosen protocol library. If an encrypted private key is decrypted in process memory, document that exposure and restrict the process; do not claim HSM-like guarantees. Key metadata, identity backups and custodian recovery material must be recoverable together without putting all keys in the identity database.

Bootstrap uses a one-time operator-controlled authenticated procedure and atomically creates the first privileged owner. No default admin credentials. Break-glass access is time-limited, strongly authenticated, separately held and fully audited. A restore changes recovery/security epoch or invalidates potentially stale sessions so an old backup cannot revive revoked authority.

## Threat-to-control qualification

| Threat | Required control and evidence |
|---|---|
| Cross-tenant ID/client collisions | Scoped keys and verified issuer mapping; negative tests with identical IDs across tenants |
| OAuth mix-up, redirect abuse, replay and CSRF | Protocol conformance and adversarial flow tests; exact redirect and interaction binding |
| Forged gateway context or confused deputy | Authenticated context and audience/resource-bound delegation; direct-backend bypass tests |
| Privilege escalation through custom role/group | Subset checks, bounded hierarchy and golden authorization fixtures |
| Stale grant resurrection | Monotonic versions, outbox ordering defense, tombstones and restore exercises |
| Token theft/refresh race | Short access lifetimes, protected client storage, atomic rotation, family reuse detection |
| Federated account takeover | No email-only linking; proof of both identities and reviewed mapper rules |
| Secret leakage in history/logs/export | Secret references, redaction, scoped export and automated leak fixtures |
| Signing-key compromise | Managed custody, emergency rotation, consumer trust updates and practiced incident recovery |
| Noisy neighbor or expensive auth abuse | Tenant/client admission limits, bounded policy evaluation and measured hashing concurrency |

Independent review and an evidence-based residual-risk sign-off are required before production retirement of Keycloak. Audit retention, cryptographic/FIPS constraints and legal holds must be confirmed with the responsible owners; this proposal does not assert regulatory compliance.
