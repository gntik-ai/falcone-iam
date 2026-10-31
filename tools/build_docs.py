#!/usr/bin/env python3
"""Regenerate the planning artifacts. This is planning tooling, not an IAM implementation."""
import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = 'gntik-ai/falcone-iam'
DATE = '2026-10-31'
BASELINE = 'b694e45e487b1c49238e30a544fb7076fc18a7d6'
EPICS = []

def epic(code, title, outcome):
    value = dict(id=f'IAM-{code}', category=code.lower(), title=title, outcome=outcome, stories=[])
    EPICS.append(value)
    return value

def story(e, title, persona, want, benefit, phase, effort, deps, requirements, acceptance):
    sid = f"{e['id']}-{len(e['stories']) + 1:03d}"
    e['stories'].append(dict(id=sid, title=title, description=want[0].upper()+want[1:]+'.',
        story=f'As {persona}, I want {want}, so that {benefit}.', phase=phase, effort=effort,
        dependencies=deps, requirements=[dict(id=f'FR-{sid[4:]}-{i+1}', statement=x) for i,x in enumerate(requirements)],
        acceptance=acceptance))

e=epic('CON','Falcone contracts and ownership','Freeze observable compatibility and a single writer for each security object.')
story(e,'Inventory Falcone IAM contracts and consumers','a platform maintainer','a versioned inventory of identity and permission contracts','replacement scope is measurable','P0','M',[],[
 'The system must preserve the approved Falcone IAM API paths, response schemas, errors and tenant/workspace semantics in a versioned contract suite.',
 'The migration inventory must classify every identity consumer and native Keycloak dependency as retained, adapted or retired.'
],[ 'Record current endpoints, issuer/audience assumptions, custom claims, role catalog and all consumers against a pinned Falcone commit.', 'Fixtures exercise positive and negative behavior in both control-plane implementations and the consoles.', 'Separate implemented contracts, source-declared capabilities and unverified deployment assumptions; product owners approve the compatibility list.' ])
story(e,'Define the identity and authorization ownership boundary','a system architect','one authoritative owner per identity, role, resource and quota','integrations avoid conflicting writes','P0','M',['IAM-CON-001'],[
 'The system must document one authoritative writer and a versioned projection contract for every shared identity and authorization entity.',
 'The system must consume Falcone plan and quota decisions without maintaining a second independently editable entitlement catalog.'
],[ 'Publish an ownership matrix for users, memberships, roles, resources, credentials, keys, quotas and audit events.', 'Preserve custom role semantics from the Falcone authorization model, including custom: names and subset-of-creator constraints.', 'Define bootstrap ordering so IAM login and authorization do not depend synchronously on workflow or serverless availability.' ])
story(e,'Select and qualify the protocol implementation','a security engineer','a maintained protocol library behind Falcone interfaces','the team can customize the product without inventing authentication protocols','P0','L',['IAM-CON-001'],[
 'The implementation must use maintained cryptographic and OIDC/OAuth libraries with pinned versions, dependency provenance and an upgrade owner.',
 'The release process must run the chosen OIDC conformance profile and documented OAuth negative tests against the configured Falcone service.'
],[ 'Prototype the proposed Node.js oidc-provider adapter with PostgreSQL persistence and production key custody; compare Go/Fosite or a Hydra adapter if a mandatory feature fails.', 'Record supported flows, unsupported extensions, license obligations, key-signing integration and measured operational costs in an ADR.', 'Passing library certification must not be represented as certification of Falcone; release requires tests of Falcone configuration and adapters.' ])

e=epic('IDN','Identity, tenancy and membership lifecycle','Manage tenant-isolated human and service principals with stable identifiers.')
story(e,'Implement principals and scoped memberships','a tenant administrator','stable identities with explicit tenant and workspace memberships','users can join multiple workspaces without crossing boundaries','P1','L',['IAM-CON-002'],[
 'The system must identify principals with immutable IDs and represent tenant/workspace membership separately from profile attributes.',
 'Every identity lookup and mutation must enforce its tenant boundary, including when two issuers use the same subject or client identifier.'
],[ 'Uniqueness and foreign-key checks include the relevant tenant scope; tests reuse identical display names across tenants.', 'Legacy identities map by verified issuer and subject, never by email alone.', 'Membership changes use optimistic version checks and cannot delete or demote the final active tenant owner without an approved transfer.' ])
story(e,'Implement invitations, provisioning and suspension','a tenant owner','idempotent invitation and deprovisioning flows','access follows the tenant lifecycle','P1','L',['IAM-IDN-001'],[
 'The system must support expiring single-use invitations, activation, suspension, reactivation and membership removal through Falcone APIs.',
 'Lifecycle mutations must commit an audit record and durable propagation event with their authoritative state change.'
],[ 'Invite redemption is tenant-bound and cannot be replayed or claimed through unverified account linking.', 'Repeated provisioning requests with one idempotency key return the original result; conflicting payload reuse fails.', 'Suspension stops new sessions immediately and produces observable downstream revocation jobs; incomplete cleanup is visible and retryable.' ])
story(e,'Implement self-service profile and safe account linking','an end user','verified profile updates and account linking','I can maintain my account without losing control of it','P2','M',['IAM-IDN-001','IAM-AUT-002'],[
 'The system must require fresh authentication and proof of both identities before linking local and federated accounts.',
 'The system must support verified email changes and configurable profile fields without allowing clients to set tenant, role or entitlement claims.'
],[ 'Email normalization and uniqueness policy are explicit per tenant and do not silently merge accounts.', 'Changing an email verifies the new address and notifies the existing address; recovery channel changes require step-up.', 'Unlinking the last usable authentication method fails; an administrator cannot silently impersonate the linked user.' ])

e=epic('AUT','Login, MFA and recovery','Provide first-party login and recovery without weakening administrator access.')
story(e,'Implement local authentication and abuse controls','an end user','a Falcone login flow with secure credential handling','I can sign in reliably','P1','L',['IAM-IDN-001','IAM-CON-003'],[
 'The system must hash local passwords using a reviewed adaptive password-hashing library and configurable cost policy, never reversible encryption.',
 'The system must rate-limit login, signup and recovery attempts by multiple signals and return non-enumerating public failure responses.'
],[ 'Use a measured Argon2id profile unless the approved cryptographic environment requires a reviewed alternative; rehash on successful login when policy changes.', 'Login interactions are CSRF-protected, expire and bind to the correct authorization request; credentials and tokens never enter logs.', 'Distributed abuse tests cover password spraying and limiter-store failure without permitting unbounded hashing work or permanent attacker-controlled lockout.' ])
story(e,'Implement passkeys, MFA and step-up','a security administrator','passkeys and enforced MFA for sensitive actions','account compromise has a smaller impact','P1','L',['IAM-AUT-001','IAM-KEY-001'],[
 'The system must support WebAuthn credentials and TOTP with audited enrollment, removal and recovery-code lifecycle.',
 'The system must require policy-defined recent MFA for administrator access and high-risk credential or permission changes.'
],[ 'WebAuthn verification checks RP ID, origin, challenge, user verification and credential ownership; challenges are single-use.', 'TOTP secrets are encrypted with managed keys and recovery codes are hashed and single-use; replay and clock-skew rules are tested.', 'Step-up freshness and authentication method are carried in trusted session state; losing a factor cannot bypass the recovery policy.' ])
story(e,'Implement recovery and lifecycle screens','an end user','recovery and account-status flows in the Falcone console','I can regain access without weakening authentication','P2','M',['IAM-AUT-002','IAM-SES-001'],[
 'The system must expose the existing login, signup, pending activation, suspended, expired credentials and password recovery states through Falcone contracts.',
 'Password resets must use expiring single-use secrets and revoke affected sessions according to the documented recovery policy.'
],[ 'Recovery does not reveal whether an address exists and cannot downgrade administrator MFA.', 'Email delivery uses a retryable outbox with redacted payload handling and no credential leakage in URLs or logs.', 'Console tests cover stale links, expired sessions, resumed navigation and accessible keyboard-driven login and recovery.' ])

e=epic('SES','OIDC, OAuth and sessions','Issue audience-bound credentials and manage their complete lifecycle.')
story(e,'Implement standards-based authorization and token endpoints','an application developer','OIDC discovery and authorization-code flows','Falcone and external clients can authenticate consistently','P1','L',['IAM-CON-003','IAM-IDN-001','IAM-KEY-001'],[
 'The system must provide OIDC discovery, JWKS, authorization, token and user-info endpoints for explicitly configured platform and tenant issuers.',
 'Public clients must use authorization code with PKCE S256, exact registered redirects and state/nonce validation; implicit and password grants must be disabled.'
],[ 'Clients cannot select another tenant by untrusted headers or arbitrary issuer URLs; issuer metadata and redirect allowlists are validated.', 'Access tokens validate issuer, audience, allowed algorithm, expiry and token purpose; ID tokens are rejected by resource APIs.', 'Authenticated confidential clients and public clients use distinct policies; consent is scoped, revocable and cannot expand requested permissions.' ])
story(e,'Implement refresh rotation and session APIs','an end user','inspectable sessions with safe refresh and logout','I can control signed-in devices','P1','L',['IAM-SES-001'],[
 'The system must rotate refresh tokens atomically, persist only protected token representations and invalidate a token family on confirmed reuse.',
 'The system must preserve Falcone session refresh/logout behavior and allow authorized users to list and revoke their sessions.'
],[ 'Concurrent refresh requests have a documented single-winner or bounded safe retry behavior; no indefinite reuse grace window exists.', 'Session idle and absolute lifetimes are enforced independently; refresh checks current membership, credential version and account status.', 'Console refresh failure clears authenticated state and returns to login; logout distinguishes local client, session and global-account revocation.' ])
story(e,'Implement token status and bounded authorization freshness','a resource service owner','explicit token-status and authorization freshness semantics','local validation does not hide revocation','P1','L',['IAM-SES-002','IAM-RBAC-002'],[
 'The system must expose authenticated introspection and revocation interfaces and define a measurable freshness bound for every enforcement surface.',
 'Authorization decisions must return the effective policy revision and refuse a minimum revision that cannot be satisfied.'
],[ 'JWT signature verification alone is never documented as immediate revocation; online and offline validation profiles have distinct limits.', 'Protected operations reject expired freshness leases when IAM or projection state is unavailable.', 'Tests revoke a credential, change a role and isolate the event broker, then verify each consumer honors its declared bound.' ])

e=epic('RBAC','Falcone permissions and policy decisions','Unify enforcement around Falcone roles, scopes and resource context.')
story(e,'Implement the canonical role catalog and custom roles','a tenant administrator','Falcone roles and bounded custom roles','I can delegate only permissions I control','P1','L',['IAM-CON-002','IAM-IDN-001'],[
 'The system must preserve the approved platform, tenant and workspace roles and resource/action permission matrix from Falcone internal contracts.',
 'Custom role creation and assignment must enforce namespace, scope, reserved-name and subset-of-delegable-permissions constraints.'
],[ 'Tests cover platform, tenant and workspace scope plus custom: prefix validation and cross-tenant role collisions.', 'Role edits are versioned and emit effective-permission recalculation events; stale writers receive a conflict.', 'An administrator cannot grant platform privileges or a permission beyond their authorized delegation set, including through nested membership.' ])
story(e,'Implement authorization decisions and batch checks','a backend developer','one explainable permission-check contract','all Falcone APIs enforce the same rules','P1','L',['IAM-RBAC-001'],[
 'The system must evaluate trusted actor, tenant, workspace, action, resource, scopes and delegation context with deny-by-default behavior.',
 'Single and batch authorization APIs must return Falcone decision IDs, effect, reason, matched policies, effective roles and correlation context.'
],[ 'Missing context, cross-tenant resources, insufficient scopes and invalid delegation produce the existing normalized error categories.', 'Resource ownership comes from authoritative service metadata; callers cannot authorize by supplying a forged owner or tenant field.', 'A golden suite verifies role grants intersect with client scopes and delegated authority, explicit denies win, and plan limits never grant access.' ])
story(e,'Implement bounded conditions and data authorization projections','a data service owner','versioned authorization projections','resource filtering stays consistent with permission checks','P2','L',['IAM-RBAC-002','IAM-REV-001'],[
 'The system must publish scoped projections for data, function, event and storage consumers with version and delegation context.',
 'Conditional policies must use a bounded approved schema with deterministic evaluation and explicit missing-attribute behavior.'
],[ 'No tenant-supplied code executes inside IAM; policy limits reject recursive or oversized rule sets.', 'List and read queries are filtered before pagination and counts are computed, preventing unauthorized existence disclosure.', 'PostgreSQL RLS and document-store enforcement receive equivalent tenant/workspace scope; a broad API-level allow cannot disable row filtering.' ])

e=epic('MAC','Machine identities and delegated execution','Give services, functions and workflows narrowly scoped renewable credentials.')
story(e,'Implement service accounts and API-key lifecycle','a workspace administrator','scoped service accounts and rotatable API credentials','automation does not use human accounts','P1','L',['IAM-IDN-001','IAM-RBAC-002','IAM-KEY-001'],[
 'The system must create, disable, rotate and revoke service-account credentials with tenant/workspace, scope and audience restrictions.',
 'API-key secrets must be shown only at issuance and stored as non-recoverable verifiers with a public identifier for lookup.'
],[ 'Client-credentials tokens use a distinct machine principal type and cannot impersonate a human subject.', 'Rotation supports a bounded overlap policy and revokes the correct credential version even for identically named clients in different tenants.', 'Credential use and failures are auditable without exposing secrets; unknown or deleted credential state is denied.' ])
story(e,'Implement scoped delegation for functions and workflows','a workflow author','short-lived delegated capabilities for activities','long-running work never stores a broad user token','P2','L',['IAM-MAC-001','IAM-SES-003'],[
 'Delegated credentials must identify actor and subject, restrict resource audience and intersect all parent scopes and tenant/workspace boundaries.',
 'Serverless and workflow execution must renew authorized machine credentials without persisting human refresh tokens in runtime payloads or histories.'
],[ 'Preserve current function invocation signature, audience, body binding and maximum lifetime until a versioned replacement contract is qualified.', 'A workflow paused beyond access-token expiry resumes only after fresh authorization; removed membership cannot be recovered by replaying history.', 'The adapter rejects delegation loops and excessive depth, binds callbacks to execution identity, and tests cancellation and permission loss in current and future runtimes.' ])
story(e,'Implement application client authentication and workload trust','a platform operator','explicit machine authentication policies','service-to-service trust is independent of network location','P2','L',['IAM-MAC-001','IAM-SES-001'],[
 'The system must support authenticated confidential clients with policy-controlled secret rotation and an asymmetric client-authentication option.',
 'Workload identity exchange must verify an allowlisted issuer, audience and subject binding before issuing a Falcone credential.'
],[ 'Qualify private_key_jwt and document optional mTLS; require short assertions, unique identifiers and replay checks.', 'Kubernetes service-account exchange, if enabled, binds namespace and service account and rejects arbitrary external JWTs.', 'No privileged daemon, runtime sandbox or cluster-wide operator is required for the baseline IAM service.' ])

e=epic('FED','Federation, external applications and MCP','Integrate enterprise identity and application access through Falcone controls.')
story(e,'Implement external OIDC federation','an enterprise tenant administrator','an allowlisted upstream identity provider','employees can use their existing corporate identity','P2','L',['IAM-SES-001','IAM-IDN-001'],[
 'The system must support tenant-scoped upstream OIDC providers with validated issuer, signing keys, redirects and claim mappings.',
 'Federated login must map verified external subjects to explicit Falcone memberships without granting privileges from untrusted group names.'
],[ 'Tests cover issuer mix-up, key rotation, malicious discovery URLs, provider outage and callback replay.', 'JIT provisioning is explicitly enabled per tenant and cannot create an owner or platform role implicitly.', 'Administrative provider changes require step-up and audit; failed federation has a documented recovery path.' ])
story(e,'Qualify enterprise SAML and directory lifecycle needs','an enterprise integrator','an explicit federation compatibility matrix','existing enterprise connections are not lost at migration','P0','M',['IAM-CON-001'],[
 'The project must inventory actual use of SAML, LDAP/AD and directory provisioning before approving Keycloak retirement.',
 'Every in-use enterprise integration must have a tested replacement or remain on an explicitly supported migration bridge.'
],[ 'Distinguish SAML declared in Falcone adapters from live integrations; verify inbound federation versus outbound application SSO requirements.', 'Record implementation stories and fixtures for every required SAML or SCIM profile; optional connectors remain disabled until qualified.', 'Validate subject mapping, deprovisioning latency and account-linking behavior with a representative corporate provider.' ])
story(e,'Implement external application and MCP registration','an application owner','Falcone-controlled client registration and tool scopes','applications get only approved capabilities','P2','L',['IAM-FED-001','IAM-RBAC-002','IAM-MAC-001'],[
 'External application and MCP clients must use Falcone tenant/workspace registration policies, redirect validation and existing plan limits.',
 'MCP authorization must enforce the approved mcp:<server>:<tool> scope mapping and resource audience at each tool invocation.'
],[ 'Preserve the curated registration and supported application-template contracts rather than exposing unrestricted provider-admin APIs.', 'Pin the actual MCP authorization specification and tested client transports; do not assume WebSockets define MCP authorization semantics.', 'Consent, credential rotation, registration abuse, tool-scope removal and cross-server token replay have integration tests.' ])

e=epic('KEY','Keys, secrets and bootstrap trust','Protect signing material and make rotation and emergency recovery explicit.')
story(e,'Implement managed signing keys and JWKS rotation','a security operator','managed key custody and tested rotation','token verification remains safe during normal and emergency changes','P1','L',['IAM-CON-003'],[
 'The system must store signing material and sensitive recoverable secrets using approved OpenBao/KMS-backed protection with least-privilege access.',
 'Key rotation must publish new public keys before use, retain required verification overlap and support emergency compromise handling.'
],[ 'Select a proven remote-signing or encrypted-key adapter and document private-key exposure in process memory; never claim non-exportability for an exported key.', 'JWKS caches are keyed by trusted issuer, key ID and algorithm; unknown key storms are rate-limited and cannot trigger arbitrary URL fetches.', 'Rotation tests cover mixed replicas, rolling upgrades, expired cache, compromise and recovery; private keys never appear in images, git or logs.' ])
story(e,'Implement first-owner bootstrap and break-glass recovery','a platform operator','audited bootstrap and emergency procedures','the platform can be recovered without a default privileged account','P1','M',['IAM-KEY-001','IAM-RBAC-001'],[
 'Initial privileged ownership must be created through a one-time authenticated bootstrap process that becomes unavailable after completion.',
 'Emergency access must have explicit scope, expiry, strong authentication and an immutable audit trail.'
],[ 'Concurrent bootstrap attempts create at most one initial owner; installations ship without a default admin password.', 'Recovery requires designated custodians and an approved operator procedure; it cannot be invoked by a tenant.', 'Run a locked-out-administrator exercise and rotate the bootstrap or emergency material afterward.' ])
story(e,'Implement secret references and credential export boundaries','a service integrator','scoped secret references','tenant credentials do not leak through workflow or provisioning payloads','P2','M',['IAM-KEY-001','IAM-MAC-001'],[
 'IAM and adapters must reference recoverable backend credentials through scoped secret handles rather than plaintext event or workflow payloads.',
 'Export and backup functions must enforce separate permissions for identity metadata, password verifiers and recoverable key material.'
],[ 'LLM BYOK, S3 credentials and federation secrets use explicit custodians and tenant-bound access policies.', 'A secret-reference consumer rechecks authorization and version; it cannot dereference a different tenant or stale revoked credential.', 'Backup and diagnostic exports are redacted by default and are tested for token, password and private-key leakage.' ])

e=epic('INT','Falcone service integrations','Enforce the same identity model across every current and planned Falcone subsystem.')
story(e,'Integrate APISIX, control planes, consoles and SDKs','a Falcone user','consistent authentication across Falcone entry points','existing API and console workflows continue to work','P2','L',['IAM-SES-003','IAM-RBAC-002','IAM-AUT-003'],[
 'APISIX and Falcone backends must validate configured issuers and audiences and strip caller-controlled identity-context headers.',
 'Both control-plane paths, both consoles and supported SDKs must pass the approved login, refresh, authorization and error compatibility fixtures.'
],[ 'Authenticated downstream context is mandatory in production; gateway trust secrets or authenticated transport are rotated and tenant headers cannot bypass validation.', 'Direct access to backends with forged roles or missing attestation fails; gateway success does not bypass resource authorization.', 'Document each approved API-key route and its stored authoritative scope; preserve existing sessionStorage behavior only during the explicit console migration window.' ])
story(e,'Integrate data services, object storage and secret access','a workspace owner','consistent data and storage permissions','credentials cannot access adjacent workspaces or buckets','P2','L',['IAM-RBAC-003','IAM-KEY-003'],[
 'Data and storage adapters must enforce scoped authorization on both credential issuance and resource use, including direct protocol access.',
 'SeaweedFS identity projections must preserve per-bucket privilege isolation and expose rotation, revocation and reconciliation status.'
],[ 'PostgreSQL RLS, pooled connection context and FerretDB/document filtering are tested for cross-tenant leakage and connection reuse.', 'S3 tests prove an identity cannot accumulate grants to another bucket; presigned URL expiry and direct credential limitations are documented.', 'OpenBao secret access, LLM BYOK and provisioning adapters honor actor, resource scope and audit context; unsupported backend revocation is surfaced rather than claimed complete.' ])
story(e,'Integrate eventing, realtime and execution services','a Falcone application developer','identity propagation across asynchronous work','events and executions remain attributable and authorized','P2','L',['IAM-MAC-002','IAM-REV-002'],[
 'Kafka/event ingress, realtime gateways and webhooks must preserve verified actor and tenant/workspace context without treating it as an unrestricted bearer credential.',
 'Current Temporal/Knative and future falcone-workflow/falcone-serverless adapters must implement the same versioned delegation and revocation contract.'
],[ 'Test publish, consume, subscribe, callback and retry paths with expired, revoked and cross-tenant credentials.', 'WebSocket upgrade, subscription and periodic revalidation use current authorization; permission loss suspends or disconnects affected access.', 'Workflow event histories and function logs contain references and correlation IDs, never broad session tokens; replayed events cannot regain revoked rights.' ])

e=epic('REV','Revocation and durable propagation','Make permission changes observable, ordered and bounded across distributed consumers.')
story(e,'Implement transactional outbox and projection workers','an operator','durable versioned identity events','a broker outage cannot silently lose security changes','P1','L',['IAM-IDN-001','IAM-RBAC-001'],[
 'Every security-state mutation must atomically persist its event in an outbox and deliver it with at-least-once semantics.',
 'Projection consumers must be idempotent, reject obsolete versions and expose applied revision and reconciliation state.'
],[ 'Crash tests cover before commit, after commit, after publish and before acknowledgement without event loss or duplicate effects.', 'Tenant-scoped aggregate sequence numbers prevent stale role or credential resurrection after out-of-order delivery.', 'Retries have bounded backoff, dead-letter handling and an audited replay tool; periodic reconciliation repairs missed projections.' ])
story(e,'Implement revocation fan-out and long-lived connection handling','a tenant administrator','measurable revocation progress','suspended identities stop using Falcone services within declared bounds','P2','L',['IAM-SES-003','IAM-REV-001'],[
 'Revocation must target sessions, refresh families, service credentials, authorization caches and registered backend projections with per-surface status.',
 'Long-lived connections and executions must revalidate authorization on a bounded schedule and on sensitive operations.'
],[ 'Measure the proposed 30-second online revocation bound with a healthy network and test stale-lease denial during outages.', 'WebSocket reconnection cannot restore a revoked subscription; DB session cleanup and S3 credential projection are reported independently.', 'A revocation response distinguishes authoritative commit, downstream completion and irreversible already-delivered data or external effects.' ])
story(e,'Implement tenant suspension, deletion and retention workflows','a platform administrator','recoverable tenant offboarding','removing a tenant cannot leave usable credentials behind','P2','L',['IAM-REV-002','IAM-IDN-002'],[
 'Tenant suspension must deny new authorization before asynchronous cleanup begins and expose cleanup progress through Falcone APIs.',
 'Deletion must follow configurable retention, legal-hold and tombstone rules without reusing principal or tenant identifiers.'
],[ 'Inventory and invalidate clients, keys, memberships, secret references and backend projections before declaring offboarding complete.', 'Repeated cleanup is safe after process crashes; a delayed event cannot recreate a deleted account or tenant.', 'Restore and retention tests verify deleted identities are not reactivated unintentionally; destructive final deletion requires the approved product workflow.' ])

e=epic('AUD','Audit, privacy and support visibility','Explain access decisions without exposing credentials or cross-tenant personal data.')
story(e,'Implement security audit events and decision correlation','a security analyst','searchable correlated security events','I can reconstruct changes and access decisions','P1','M',['IAM-CON-002','IAM-REV-001'],[
 'The system must audit authentication, credential, membership, role, key and administrative changes with actor, tenant, outcome, revision and correlation ID.',
 'Audit access and export must be separately authorized and must redact secrets and unnecessary personal information.'
],[ 'Security-state audit records are committed with mutations and cannot be edited by tenant administrators.', 'Measure delivery completeness; security mutations fail safely if durable audit acceptance is unavailable.', 'Trace a login, API call, workflow delegation and S3 issuance end-to-end without storing bearer tokens.' ])
story(e,'Implement authorized access explanations and privacy controls','a tenant auditor','scoped explanations and retention settings','support can diagnose denial without broad data access','P2','M',['IAM-AUD-001','IAM-RBAC-002'],[
 'The system must expose authorized decision explanations that redact policies and resources outside the caller scope.',
 'Identity and audit data must have configurable retention, export and erasure behavior with documented legal-hold exceptions.'
],[ 'Explain endpoints cannot enumerate another tenant or expose secret attributes through denial reasons.', 'Access to audit exports is logged and paginated exports remain scope-filtered.', 'Minimize profile attributes and distinguish pseudonymized immutable audit history from erasable profile data; retention is approved before production.' ])
story(e,'Implement audit export and operational dashboards','an on-call engineer','metrics and reliable security-event export','I can detect abuse and failed propagation','P2','M',['IAM-AUD-001','IAM-OPS-002'],[
 'The system must export structured logs, metrics and traces using Falcone observability conventions without unbounded user-ID metric labels.',
 'The system must provide authenticated audit export and alerts for abuse, key failure, authorization errors and projection lag.'
],[ 'Dashboards separate expected denies from service errors and report issuer, endpoint and latency class with bounded cardinality.', 'SIEM delivery retries preserve event IDs and do not duplicate logical records at an idempotent consumer.', 'Exercise alerts for stalled outbox, lost signing access, refresh reuse and unusual administrative grants with linked runbooks.' ])

e=epic('OPS','Deployment, reliability and ownership','Operate IAM under restricted Kubernetes and OpenShift permissions.')
story(e,'Package restricted namespace deployments','a platform operator','reproducible least-privilege manifests','IAM runs in corporate OpenShift and vanilla Kubernetes','P1','M',['IAM-CON-003','IAM-KEY-001'],[
 'The baseline deployment must run with arbitrary non-root UID, dropped capabilities, read-only root filesystem and no privileged or host access.',
 'Installation must use ordinary namespaced workloads without requiring a custom operator, CRDs, cluster-admin or a sandbox runtime.'
],[ 'Document the prerequisite PostgreSQL, OpenBao, Kafka, TLS, network and backup services and their actual operator-owned permissions.', 'Qualify two supported Kubernetes minors and the administrator-confirmed OpenShift build; a Kubernetes patch number alone is not an OpenShift support matrix.', 'Multiple replicas, readiness/liveness, graceful shutdown, network policies, disruption budgets and migration jobs pass rollout tests.' ])
story(e,'Benchmark and define service objectives','a product owner','measured IAM capacity and availability objectives','capacity planning matches identity traffic','P0','M',['IAM-CON-001'],[
 'The project must benchmark token issuance, password login, authorization checks, refresh, key lookup and revocation separately.',
 'The project must define availability, latency, recovery and freshness objectives with a documented workload, topology and measurement boundary.'
],[ 'Use the provisional objectives in operations.md as hypotheses; record hardware, policy size, cache hit rate, tenant skew and failure mode.', 'Do not equate prior 100k event messages per second or 10k deployed functions with login or token issuance rate.', 'Test noisy-neighbor limits, broker failure and database failover; revise objectives and sizing from results before making an SLA commitment.' ])
story(e,'Implement recovery, upgrade and on-call procedures','an SRE','tested restoration and upgrades with named owners','IAM failures do not lock out the platform indefinitely','P2','L',['IAM-OPS-001','IAM-REV-002','IAM-AUD-001'],[
 'The service must provide tested backup, restore, schema migration and rollback procedures covering identity state, key access and revocation state.',
 'Production release must name runtime maintainers, on-call responders, security qualification owners and product decision owners.'
],[ 'Restore from PostgreSQL and managed-key backups in isolation; rotate a recovery epoch or invalidate sessions to prevent restored stale tokens becoming valid.', 'Prove backward-compatible rolling migrations and define the stop point for irreversible schema or credential changes.', 'Run incident exercises for IdP outage, compromised signing key, stolen refresh family and lost database quorum with measured recovery times.' ])

e=epic('MIG','Keycloak migration and retirement','Move by tenant and issuer while retaining explicit rollback and compatibility gates.')
story(e,'Build a migration inventory and dry-run importer','a migration engineer','repeatable identity and client mapping','the cutover has measurable coverage','P1','L',['IAM-CON-001','IAM-IDN-001','IAM-FED-002'],[
 'Migration tooling must dry-run and report users, issuer-subject mappings, memberships, roles, clients, federation and credential portability without modifying production.',
 'The importer must be idempotent, tenant-scoped and produce reconciled counts and a report of unsupported or conflicting objects.'
],[ 'Validate actual Keycloak deployment versions and enabled extensions; never assume all declared adapter versions are deployed.', 'Determine password-hash portability by algorithm and parameters; unsupported credentials require a controlled reset or approved bridge, never plaintext export.', 'Classify sessions, MFA secrets, WebAuthn RP IDs and signing keys independently; do not claim seamless portability for all of them.' ])
story(e,'Implement dual-issuer shadow checks and tenant canaries','a rollout owner','a reversible staged migration','behavior differences are found before all tenants move','P3','L',['IAM-MIG-001','IAM-INT-001','IAM-INT-002','IAM-INT-003','IAM-DEV-003'],[
 'Migration mode must explicitly allowlist old and new issuers, audiences and principal mappings without accepting arbitrary token sources.',
 'Tenant canaries must compare authorization outcomes and projection completion before switching the authoritative writer.'
],[ 'Shadow checks produce no duplicate grants, user mutations or external side effects; mismatches are classified and approved.', 'Canary gates cover login, refresh, custom roles, federation, S3, DB, events, MCP, workflows and serverless; native Keycloak passthrough usage is inventoried.', 'Rollback reconciles post-cutover membership and credential changes; it is not an unconditional database snapshot restore.' ])
story(e,'Retire Keycloak after compatibility and security gates','a Falcone product owner','a controlled retirement checklist','the custom service becomes the supported IAM implementation','P3','M',['IAM-MIG-002','IAM-OPS-003'],[
 'Keycloak retirement must require signed-off compatibility, security, recovery and operational readiness evidence for every in-use integration.',
 'Retirement must revoke obsolete credentials and trust entries, archive required audit evidence and remove approved legacy routes.'
],[ 'Observe a defined rollback window and confirm no unsupported client or enterprise connector remains.', 'Explicitly retire or document operator-only /_native/keycloak paths; do not promise raw Keycloak Admin API compatibility.', 'Record owners, runbook locations, residual exceptions and support policy; removing Keycloak is a separate authorized deployment change.' ])

e=epic('DEV','Developer experience and release qualification','Make integrations testable and releases reviewable before production trust changes.')
story(e,'Publish API schemas, SDK helpers and local fixtures','an integration developer','versioned schemas and local test identities','I can build a Falcone integration without production credentials','P1','M',['IAM-CON-001','IAM-RBAC-002'],[
 'The project must publish OpenAPI and event schemas plus TypeScript and Go integration examples for the approved contracts.',
 'Development fixtures must include multiple tenants, machines, custom roles, expired credentials and negative authorization cases.'
],[ 'Examples distinguish end-user tokens, machine credentials and delegated invocation tokens with correct audiences.', 'Local setup uses synthetic data and generated development keys and cannot enable unverified identity mode in production.', 'Schema compatibility checks detect breaking changes and document deprecation periods and adapter version negotiation.' ])
story(e,'Implement secure build and dependency maintenance','a maintainer','reproducible builds and dependency checks','IAM releases have attributable provenance','P1','M',['IAM-CON-003'],[
 'Release builds must pin dependencies and publish an SBOM, signed image provenance and migration compatibility notes.',
 'The project must define security patch ownership, vulnerability reporting and dependency update qualification.'
],[ 'CI checks secrets, licenses, vulnerable dependencies and container permissions; exceptions have an owner and expiry.', 'Protocol-library upgrades rerun the configured conformance and regression suites.', 'Select an owner-approved repository license before redistributing third-party code; research references do not authorize copying proprietary extensions.' ])
story(e,'Qualify isolation, protocol security and failure behavior','a security reviewer','adversarial and failure-injection evidence','Keycloak is replaced only after the new service proves its boundaries','P2','L',['IAM-SES-003','IAM-AUT-002','IAM-MAC-002','IAM-RBAC-003','IAM-OPS-003','IAM-DEV-002'],[
 'A release candidate must pass tenant-isolation, protocol-negative, credential-replay and recovery tests against all enabled integration profiles.',
 'Production cutover must require independent security review of authentication, authorization, key custody and deployment configuration.'
],[ 'Threat tests cover confused deputy, forged context, OAuth mix-up, CSRF, SSRF, privilege escalation, stale grants and refresh races.', 'Fault tests cover replica crashes, broker partitions, delayed/out-of-order events, DB restore and key rotation with declared fail-closed behavior.', 'Document residual findings, remediation owners and approved exceptions; ordinary containers are not represented as a security sandbox for hostile tenant code.' ])

def generate():
    mapping_path=ROOT/'docs/github-issues.json'
    mapping=json.loads(mapping_path.read_text()) if mapping_path.exists() else {}
    by_id={s['id']:s for e in EPICS for s in e['stories']}
    assert len(by_id)==sum(len(e['stories']) for e in EPICS)
    def visit(sid, stack):
        assert sid not in stack, f'Dependency cycle: {stack} -> {sid}'
        for d in by_id[sid]['dependencies']:
            assert d in by_id, f'Unknown dependency: {d}'
            visit(d, stack+[sid])
    for sid in by_id: visit(sid,[])
    def link(sid):
        n=mapping.get(sid,{}).get('number')
        return f'[{sid}](https://github.com/{REPO}/issues/{n})' if n else sid
    requirements=['# Functional requirements\n',f'Planning baseline: {DATE}. Each statement is testable and traces to one story. All requirements describe the target, not delivered functionality. See [architecture](architecture.md), [security](security.md) and [operations](operations.md) for normative design detail.\n']
    backlog=['# Epics and user stories\n','Generated by `python3 tools/build_docs.py`. S = small, M = medium, L = large; relative complexity, not time promises. No assignees or delivery dates are assumed. P0 = discovery/qualification; P1 = core; P2 = integrations/hardening; P3 = canary/retirement. Phase indicates earliest stage; dependency and release gates still apply.\n','Each issue uses a stable IAM identifier. Parent links and epic task lists express the hierarchy; no GitHub Project board or native sub-issue relationship is implied.\n']
    issues=[]; rows=[]
    for e in EPICS:
        requirements += [f"## {e['title']}\n",'| ID | Requirement | Story |','|---|---|---|']
        backlog += [f"- **{link(e['id'])}: {e['title']}** — {e['outcome']}\n"]
        epic_body=f"<!-- falcone-iam:{e['id']} -->\n\n## Outcome\n\n{e['outcome']}\n\n## Scope\n\nA custom Falcone service; preserve Falcone contracts and enforce tenant/workspace boundaries. See [architecture](https://github.com/{REPO}/blob/main/docs/architecture.md) and [requirements](https://github.com/{REPO}/blob/main/docs/requirements.md).\n\n## Stories\n\n"
        for s in e['stories']: epic_body+=f"- [ ] {link(s['id'])}: {s['title']}\n"
        epic_body+='\n## Exit criteria\n\nAll child acceptance criteria are met, evidence is linked, and the integration/security impact is reviewed. Planning publication does not mark this epic implemented.\n'
        issues.append(dict(id=e['id'],title=f"[Epic][{e['id']}] {e['title']}",body=epic_body,labels=['type:epic',f"area:{e['category']}"]))
        rows.append(dict(ID=e['id'],Type='Epic',Title=e['title'],Parent='',Phase='',Effort='',Dependencies='',URL=f"https://github.com/{REPO}/issues/{mapping[e['id']]['number']}" if e['id'] in mapping else ''))
        for s in e['stories']:
            assert len(s['acceptance'])>=3 and len(s['requirements'])==2
            body=f"<!-- falcone-iam:{s['id']} -->\n\nParent: {link(e['id'])}\n\n## User story\n\n{s['story']}\n\n## Description\n\n{s['description']}\n\nPhase: {s['phase']} · Effort: {s['effort']}\n\n## Requirements\n\n"
            for r in s['requirements']:
                requirements.append(f"| {r['id']} | {r['statement']} | {link(s['id'])} |")
                body+=f"- **{r['id']}**: {r['statement']}\n"
            body+='\n## Acceptance criteria\n\n'+''.join(f'- [ ] {a}\n' for a in s['acceptance'])
            body+='\n## Dependencies\n\n'+(', '.join(link(d) for d in s['dependencies']) or 'None; discovery can start independently.')+'\n'
            body+=f"\n## Design reference\n\n[Architecture](https://github.com/{REPO}/blob/main/docs/architecture.md) · [Integration matrix](https://github.com/{REPO}/blob/main/docs/integration-matrix.md) · [Security](https://github.com/{REPO}/blob/main/docs/security.md).\n"
            issues.append(dict(id=s['id'],title=f"[{s['id']}] {s['title']}",body=body,labels=['type:story',f"area:{e['category']}",f"phase:{s['phase'].lower()}",f"effort:{s['effort'].lower()}"]))
            backlog += [f"  - **{link(s['id'])}: {s['title']}** ({s['phase']}, {s['effort']})",f"    - {s['story']}",f"    - Description: {s['description']}",f"    - Requirements: {', '.join(r['id'] for r in s['requirements'])}",f"    - Dependencies: {', '.join(link(d) for d in s['dependencies']) or 'None'}"]
            backlog += [f"    - Acceptance: {a}" for a in s['acceptance']]
            backlog.append('')
            rows.append(dict(ID=s['id'],Type='Story',Title=s['title'],Parent=e['id'],Phase=s['phase'],Effort=s['effort'],Dependencies=';'.join(s['dependencies']),URL=f"https://github.com/{REPO}/issues/{mapping[s['id']]['number']}" if s['id'] in mapping else ''))
        requirements.append('')
    (ROOT/'docs/requirements.md').write_text('\n'.join(requirements)+'\n')
    (ROOT/'docs/backlog.md').write_text('\n'.join(backlog)+'\n')
    (ROOT/'docs/backlog.json').write_text(json.dumps(dict(schema_version=1,date=DATE,baseline=BASELINE,epics=EPICS),indent=2)+'\n')
    (ROOT/'docs/issue-payloads.json').write_text(json.dumps(issues,indent=2)+'\n')
    output=io.StringIO(); writer=csv.DictWriter(output,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (ROOT/'docs/backlog.csv').write_text(output.getvalue())
    print(json.dumps(dict(epics=len(EPICS),stories=len(by_id),requirements=sum(len(s['requirements']) for s in by_id.values()),issues=len(issues),mapped=len(mapping))))

if __name__=='__main__': generate()
