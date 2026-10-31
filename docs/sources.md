# Sources and evidence

Research date: 2026-10-31. External product descriptions use official documentation or upstream repositories. Links may evolve; dependency intake must pin releases and review corresponding source/license files. No source code is copied from these reference products.

## Falcone source baseline

Repository examined at commit [`b694e45e487b1c49238e30a544fb7076fc18a7d6`](https://github.com/gntik-ai/falcone/tree/b694e45e487b1c49238e30a544fb7076fc18a7d6).

| Evidence | What it supports |
|---|---|
| [README](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/README.md) | Platform stack and integration inventory |
| [Authorization model](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/packages/internal-contracts/src/authorization-model.json) | Roles, security context, decisions, propagation targets, errors and resource/action semantics |
| [Tenant custom roles](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/apps/control-plane-executor/src/iam-tenant-roles.mjs) | Falcone-owned persisted roles, prefix/scope/subset rules and recalculation event |
| [Workspace authorization](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/apps/control-plane/workspace-authz.mjs) | Resource checks and administrator/internal paths requiring qualification |
| [Keycloak adapter](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/packages/adapters/src/keycloak-admin.mjs) | Normalized management resources/actions, roles, scopes, protocol catalog and required actions |
| [IAM administration](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/apps/control-plane-executor/src/iam-admin.mjs) | Falcone management surface |
| [Gateway auth/passthrough](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/docs/reference/architecture/gateway-authentication-and-passthrough.md) | Gateway trust, API-key scope and product/native route distinction |
| [Session invalidation](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/docs/reference/architecture/console-session-invalidation.md) | Console refresh, invalidation and navigation contract |
| [Console auth](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/apps/control-plane-executor/src/console-auth.mjs) | Login and lifecycle states |
| [Identity guard](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/apps/control-plane-executor/src/runtime/identity-guard.mjs) | Production verifier requirement and development distinction |
| [Service-account revocation](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/apps/control-plane-executor/src/runtime/sa-revocation.mjs) | Verified realm/client scoping and timestamp watermark limitations |
| [SeaweedFS identity issuance](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/apps/control-plane/seaweedfs-identity.mjs) | Per-bucket grants, key lifecycle and runtime/provisioning distinctions |
| [Invocation verifier](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/apps/fn-runtime/invocation-auth.mjs) | Existing short-lived signed invocation audience, body binding and tenant context |
| [Realtime token validation](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/packages/realtime-gateway/src/auth/token-validator.mjs) | JWT validation and normalized scopes/workspaces |
| [Realtime scope revocation](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/packages/realtime-gateway/src/actions/handle-scope-revocation.mjs) | Active-session suspension and audit |
| [MCP OAuth](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/apps/control-plane-executor/src/mcp-oauth.mjs) | Curated client registration and tool scopes |
| [External application IAM](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/apps/control-plane-executor/src/external-application-iam.mjs) | Application templates, redirects, mapper validation and plan limits |
| [Provisioning IAM applier](https://github.com/gntik-ai/falcone/blob/b694e45e487b1c49238e30a544fb7076fc18a7d6/packages/provisioning-orchestrator/src/appliers/iam-applier.mjs) | Existing IAM provisioning adapter boundary |

## External primary references

| Reference | Design use |
|---|---|
| [Keycloak](https://www.keycloak.org/) | Current identity/federation baseline |
| [Ory Hydra repository](https://github.com/ory/hydra), [Ory Kratos repository](https://github.com/ory/kratos), [OSS scope](https://www.ory.com/docs/oss/getting-started) | Protocol/lifecycle separation; distinguish upstream artifacts and commercial offerings |
| [ZITADEL organizations](https://zitadel.com/docs/guides/manage/console/organizations-overview), [projects](https://zitadel.com/docs/guides/manage/console/projects-overview), [repository](https://github.com/zitadel/zitadel) | Organization and application boundaries; current repository license |
| [authentik providers](https://docs.goauthentik.io/add-secure-apps/providers/), [license](https://github.com/goauthentik/authentik/blob/main/LICENSE) | Federation/flow patterns and OSS/enterprise separation |
| [Casdoor repository](https://github.com/casdoor/casdoor) | Application onboarding, identity-provider and administration patterns |
| [Dex documentation](https://dexidp.io/docs/), [connectors](https://dexidp.io/docs/connectors/) | Broker boundary and connector limitations |
| [Authelia](https://www.authelia.com/), [OIDC integration](https://www.authelia.com/integration/openid-connect/) | Edge authentication and MFA patterns |
| [OpenFGA](https://openfga.dev/) | Model-driven relationship authorization |
| [SpiceDB consistency](https://authzed.com/docs/spicedb/concepts/consistency) | Explicit revision and fresh-after-write checks |
| [Cerbos documentation](https://docs.cerbos.dev/cerbos/latest/index.html) | Stateless PDP and resource policy boundary |
| [OPA documentation](https://www.openpolicyagent.org/docs) | Policy decision/enforcement separation and bundle distribution |
| [Casbin overview](https://v3.casbin.org/docs/overview) | Embedded RBAC/ABAC patterns |
| [node-oidc-provider](https://github.com/panva/node-oidc-provider), [OpenID certification listings](https://openid.net/certification/certified-openid-connect-implementations-2/) | Protocol-library candidate; certification does not transfer to our deployment |
| [OAuth security BCP, RFC 9700](https://datatracker.ietf.org/doc/html/rfc9700) | Current OAuth threat controls and prohibited legacy flows |
| [OIDC Core](https://openid.net/specs/openid-connect-core-1_0.html) | Protocol qualification reference |
| [WebAuthn](https://www.w3.org/TR/webauthn-3/) | RP/origin/challenge/credential verification reference; pin supported level during implementation |

Recommendations, proposed SLOs, effort estimates and the final architecture are engineering judgments based on this evidence. They are not benchmark claims or upstream guarantees.
