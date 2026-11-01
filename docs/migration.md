# Migration from Keycloak

No migration or production change is performed by this documentation bootstrap. This plan preserves Falcone interfaces while changing their identity implementation.

## Stage 0 — inventory and acceptance baseline

Pin the actual deployed Keycloak versions, extensions, realms, issuers, keys, clients, callback URLs, protocols, scopes, users, federation connections, required actions, sessions and machine credentials. Compare with source catalogs rather than assuming every declared feature is live. Capture sanitized golden fixtures for login, refresh, role decisions, delegation and each backend integration.

Inventory direct Keycloak SDKs, issuer URLs, Admin API callers, service-account tokens, native gateway passthrough, scripts and emergency procedures. Separate user-facing Falcone compatibility from operator-only `/_native/keycloak/admin/*` routes. SAML, OIDC, LDAP/AD and SCIM are all mandatory, regardless of current usage. Qualify their concrete profiles and provider configurations. Every in-use capability gets a tested replacement; a temporary bridge may support migration but cannot satisfy the final mandatory-protocol gate.

## Stage 1 — establish mappings and dry-run imports

Create immutable mappings from old verified issuer/subject to Falcone principal, and tenant/client identifiers to the new client records. Preserve membership and custom-role authority from Falcone's database; do not replace it with a shallow realm-role export. Validate owner coverage, role subsets, resource scope, conflicts and duplicate identities. Import is tenant-scoped, idempotent and versioned; dry run emits counts and unsupported objects without touching production.

| Data | Portability strategy |
|---|---|
| Profile, verified external links and membership | Explicit schema mapping, normalization and conflict review; no email-only merging |
| Built-in/custom roles and grants | Canonical Falcone catalog plus approved grants; compare effective decisions |
| Password verifiers | Import only if algorithm/parameters are supported and securely reviewed; otherwise controlled reset or approved temporary bridge. Never require plaintext password export |
| MFA and recovery | Assess each factor and secret format; re-enroll when portability or custody is unsafe |
| WebAuthn | RP ID, origin and credential behavior may prevent seamless transfer; test or schedule re-enrollment |
| Sessions and refresh tokens | Plan reauthentication; do not assume portable server state or token-family semantics |
| Client/service credentials | Controlled rotation with explicit overlap where supported; notify dependent automation |
| Signing keys and issuer URLs | Decide continuity deliberately; new issuer with explicit dual trust is the default migration proposal, stable public issuer is a separately qualified option |
| Audit history | Retain source identifiers and migration mapping for traceability under retention policy |

## Stage 2 — adapter and shadow qualification

Allow only explicit old/new issuers and audiences. Validate each token under its own provider configuration and map subjects after verification. A matching `sub` string across issuers is not enough. Do not transform a signed Keycloak token by editing its claims.

Run the new policy engine in shadow mode against existing authorized requests. Record decision differences without issuing duplicate grants, sending duplicate messages or repeating backend writes. Require classified resolution of mismatches, including custom roles, data filters and negative cases. Test login and token flows in isolated nonproduction tenants; shadow authorization alone cannot validate authentication.

Keep a single authoritative writer for each tenant and entity throughout the transition. Record the final migration revision, catch up durable events, verify projections, then change the writer. Do not run unconstrained bidirectional synchronization.

## Stage 3 — tenant canaries

Move approved low-risk tenants/clients first. Gates include login/refresh/recovery/MFA, SAML and OIDC federation, LDAP/AD authentication/synchronization, SCIM lifecycle and deprovisioning, API keys/service accounts, role edits, Postgres/document isolation, S3 bucket isolation, event and WebSocket revocation, MCP registration/tool scopes, functions and workflow resumption. Verify current and future execution adapters where enabled. Reference integrations cover mandatory protocols not yet used by a canary tenant.

Measure decision mismatches, latency, availability, outbox lag, revocation bounds, error codes and support incidents. Define go/no-go thresholds and an observation window with owners before execution. Keep old trust only as long as necessary and never widen audiences to make a test pass.

## Rollback

Rollback includes routing, issuer trust, authoritative writer, identity mapping and credential divergence. Password resets, newly enrolled factors, revoked credentials and permission changes after cutover may not exist in Keycloak. Reconcile them or require reauthentication/reset; restoring an old snapshot blindly can resurrect revoked access. Never replay side-effecting shadow requests.

Declare an irreversible boundary for unsupported credential transformation, schema cleanup or key retirement. Before that boundary, prove rollback on a canary with changes made after cutover. After it, recovery is a forward repair or restore under the explicit incident procedure, not a promise of instant rollback.

## Stage 4 — retire Keycloak

Require approved compatibility evidence, configured-service protocol qualification, independent security review, recovery drill, on-call ownership and all projection/revocation gates. SAML, OIDC, LDAP/AD and SCIM must each pass the [enterprise qualification matrix](enterprise-federation.md), even if a protocol has no existing production tenant. Confirm no required integration remains on the bridge. End the agreed rollback window; revoke old clients and trust, retire approved native routes, retain audit/export evidence securely and document supported interfaces.

The owner authorizes the actual production deployment and removal separately. Publishing this repository does not disable or modify Keycloak in Falcone.
