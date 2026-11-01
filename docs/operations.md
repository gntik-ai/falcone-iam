# Operations, performance and ownership

## Proposed objectives

These are initial engineering targets for qualification, not an SLA or measured performance. Start with a single-region deployment across available failure domains. Active-active cross-region identity writes are out of scope until conflict, residency and recovery requirements justify them.

| Objective | Proposed target | Measurement and qualification |
|---|---|---|
| Authentication/control API availability | 99.95% per calendar month | Valid supported requests served without platform-caused failure; include required database/key dependencies. Track internal availability and end-user federation availability separately |
| Online authorization decision latency | p95 ≤20 ms, p99 ≤50 ms | Warm same-region service boundary, bounded policy, specified dataset/concurrency; excludes downstream resource work. Report cold-cache results separately |
| Token issuance / refresh | p95 ≤200 ms | Service time under declared load, excluding human interaction and upstream federation; distinguish KMS and database time |
| Local password login | p95 ≤1 s after credentials arrive | Includes reviewed password hashing and rate limits; benchmark cost without weakening password protection |
| Online revocation | ≤30 s under qualified conditions | From authoritative commit to access denial; freshness leases deny after the same bound during disconnected operation |
| Mutation durability | No acknowledged committed mutation lost in tested replica/process failure | Requires suitable synchronous durable database topology; does not imply zero regional-disaster loss |
| Disaster recovery | RPO ≤5 min, RTO ≤60 min initially | Proposed backup/PITR and key-custodian recovery objective; measure in isolated full restoration drills |
| Outbox/projection recovery | Alert before freshness budget is exceeded | Dashboard pending/applied revisions, oldest event age and failed targets; security freshness takes precedence over availability |

99.95% is approximately 21.6 minutes of error budget in a 30-day month. Track expected authentication denials separately from service errors without hiding incorrect denials. Assign ownership and a measurement boundary before committing publicly.

## Capacity model

Do not scale IAM from function count or total event throughput. Size separately for active users, concurrent sessions, tenants/workspaces, memberships, clients/service accounts, role bindings, checks per resource request, refresh interval, federation volume, audit events and projection churn.

Approximate token refresh rate is active refreshing sessions divided by mean refresh interval, plus machine issuance and bursts. Authorization QPS is protected operations multiplied by checks per operation and the uncached fraction, plus online status checks. WebSocket connection count and revalidation interval create a separate steady load. Cache hit ratio never excuses violating a revocation bound.

Benchmark tenant skew, bursty login, large custom roles, cold keys, hash CPU/memory cost, key-custodian latency, database lock contention and broker backlog. Hot signing or high-cardinality policy loads may need separate deployment roles; do not prematurely split every module into a microservice. Enforce Falcone quotas and system-protection admission controls separately, with documented ownership.

## Restricted deployment

Use ordinary namespaced Deployments, Services, ConfigMaps, Secrets/references, Jobs and the platform's approved ingress/route. Run arbitrary non-root UID; drop capabilities, deny privilege escalation, use read-only root filesystems and writable bounded temporary storage. Do not require a custom SCC, privileged pod, cluster-wide RBAC, CRD/operator or unavailable sandbox runtime. Namespace administrators still need to provide the approved service accounts, networking, storage access and TLS routing.

Deploy API/protocol replicas with readiness gates, graceful shutdown, PodDisruptionBudgets and anti-affinity where available. Database migrations run as a narrowly scoped job with expand/contract compatibility. IAM's normal request path should not need Kubernetes API credentials; optional provisioning integrations use separately scoped identities.

The earlier request for an OpenShift version bundling Kubernetes 1.33.12 must be resolved to the actual installed OpenShift release/build and support policy. Do not infer an OpenShift product version from a patch alone. CI will qualify the latest two administrator-approved supported Kubernetes minors at implementation/release time and the confirmed OpenShift build. Similarly, pin tested SeaweedFS releases and actual notification settings rather than claiming compatibility with an undefined moving 'latest'.

PostgreSQL, Kafka, OpenBao/KMS, TLS, DNS, mail delivery and backup storage remain external dependencies with named owners. A minimal-privilege IAM application does not remove the operational work needed to provide those dependencies.

Mandatory SAML/OIDC connections, LDAP/AD directories and SCIM endpoints also need tenant-scoped configuration, approved network egress, trusted certificates and named connector owners. Monitor certificate expiry, synchronization checkpoints, detection lag, outbound provisioning failures and applied membership revisions. Set per-connector detection/freshness budgets in addition to internal revocation objectives; qualify corporate AD bind/signing/channel-binding policy without requiring privileged runtime access.

## Failure handling

| Failure | Required behavior |
|---|---|
| IAM database unavailable | Deny new grants, login, refresh and mutations; approved cached/offline validation lasts only within its declared profile |
| Kafka unavailable | Commit state with outbox until safe backlog capacity; projection stale state fails according to leases; alert and reconcile |
| OpenBao/KMS unavailable | Stop operations requiring unavailable signing/decryption; only already-loaded approved key material follows its explicit cache policy |
| External corporate IdP unavailable | Explain sign-in failure safely; existing Falcone sessions follow normal expiry. No automatic insecure local-password fallback |
| Audit export unavailable | Durable local acceptance and bounded backlog; if durable audit acceptance itself fails, fail security mutations safely |
| Replica crash/rolling upgrade | Shared durable sessions, idempotent mutations and transactions prevent duplicate grants or lost refresh rotation |
| Snapshot restore | Reconcile keys, epochs, outbox and projections; invalidate uncertain credentials before reopening traffic |

## Responsibility model

Runtime ownership means responsibility for correctness, dependency upgrades, schema evolution, protocol behavior and integration compatibility. It is broader than owning a Kubernetes container. On-call ownership means responding to incidents, restoring service, managing error budgets and communicating impact. Security qualification means demonstrating that threats and required controls have been independently assessed before production trust changes.

| Responsibility | Typical accountable role/team | Collaborators / deliverables |
|---|---|---|
| Product scope and compatibility | Falcone product owner / platform architect | Approves required login/federation flows, role semantics, migration scope and exceptions |
| Runtime and protocol maintenance | IAM/backend engineering maintainers | Owns code, provider library, schemas, tests, patching and release compatibility |
| Integration enforcement | Owners of gateway, data, storage, events, serverless and workflow | Owns consumer-side authorization, credential lifecycle and revocation evidence |
| Deployment and reliability | SRE / platform operations / DevOps | Owns manifests, capacity, alerts, backups, restoration and incident runbooks |
| On-call incident response | Named primary and secondary SRE/IAM responders | Defines escalation, incident commander, communications and credential compromise response |
| Security qualification | Application security / identity security engineers, with independent reviewers | Threat model, protocol review, penetration testing, key custody and residual-risk evidence |
| Key custody and emergency access | Security operations / infrastructure custodians | Approves cryptographic controls, secret access, recovery material and break-glass exercises |
| Privacy and retention | Data protection / governance owner | Approves profile retention, audit access, erasure and legal-hold policy |

One small team may hold several roles, but privileged changes still need appropriate review and recovery access must not depend on one person. Record actual people/rotations before P3; this planning document assigns no real person without confirmation.
