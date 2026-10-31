# Open-source survey and feature selection

Reviewed 2026-10-31. This is a representative survey across complete IAM, federation, relationship authorization and policy engines, not an exhaustive claim about every open-source project. The products solve different parts of the problem; authorization engines are not login replacements. Links refer to primary project documentation or repositories. Scaling descriptions are architectural models, not independently verified Falcone benchmarks.

## Identity and federation references

| Project | Functions and extension points | Scaling model | Relative to Keycloak and fit for Falcone |
|---|---|---|---|
| [Keycloak](https://www.keycloak.org/) — current baseline | Login, OIDC/OAuth, SAML, realm/client roles, federation, MFA; themes, mappers and provider SPIs | Replicated services with database/cache coordination; realm and session design affect operations | Broad integrated baseline. Falcone still needs product-specific resource enforcement. Upgrade coupling, configuration spread and administration footprint motivate replacement; actual operational problems must be measured |
| [Ory Hydra](https://github.com/ory/hydra) | OAuth/OIDC authorization server; separate login/consent application and persistence integration | Replicated protocol servers sharing durable state | Cleaner protocol/product split; not a user directory. Adopt headless boundaries. Running it as a subsystem reduces protocol implementation effort but adds an independently operated component and edition/version qualification |
| [Ory Kratos](https://github.com/ory/kratos) | Identity schemas, login/registration/recovery, credentials and sessions; custom UI and integrations | Replicated identity service with shared database | Strong identity-lifecycle reference; combine with a protocol provider for OAuth/OIDC. Tenant/workspace policy still belongs to Falcone. Check exact OSS features against the chosen release, not managed-service marketing |
| [ZITADEL](https://zitadel.com/docs/guides/manage/console/organizations-overview) | Organization/project/application boundaries, roles and federation; APIs and configurable integration points | Horizontally deployed service with durable identity state; topology and database cost require measurement | Useful B2B organization and delegated-administration model. More platform breadth than Falcone needs; preserve Falcone tenant IDs instead of creating a parallel hierarchy |
| [authentik](https://docs.goauthentik.io/add-secure-apps/providers/) | OIDC/OAuth, SAML, LDAP and proxy providers; configurable authentication flows and policies | Server/worker roles and shared persistence; provider/outpost topology adds services | Useful flow composition and federation adapters; more operational pieces than a focused IAM service. Do not copy enterprise-only features into an OSS baseline |
| [Casdoor](https://github.com/casdoor/casdoor) | Organization/user/application management, SSO protocols, identity-provider connectors and MFA; APIs/SDKs and adapters | Replicated application service with shared database; qualify stateful flow behavior | Useful application onboarding and admin UX patterns. Feature breadth does not prove fit for Falcone workspace isolation or revocation; validate those separately |
| [Dex](https://dexidp.io/docs/) | OIDC federation broker with upstream connectors | Replicated broker using configured storage; upstream provider is part of availability | Smaller federation boundary than Keycloak. Useful optional enterprise bridge, but not a full user lifecycle or Falcone authorization system; refresh/group behavior varies by connector |
| [Authelia](https://www.authelia.com/) | SSO/MFA, reverse-proxy access control and OIDC provider | Replicated authentication service with configured storage/session coordination | Useful edge protection and step-up patterns. Falcone needs deeper resource, data and delegation controls than proxy authorization alone |

## Authorization references

| Project | Functions and extension points | Scaling model | Relative to Keycloak and fit for Falcone |
|---|---|---|---|
| [OpenFGA](https://openfga.dev/) | Relationship tuples, model-driven checks and conditional relationships; APIs/SDKs | Stateless API replicas over a tuple datastore; graph fan-out and model shape affect latency | Better reference for fine-grained resource relationships than realm roles alone. Optional when sharing graphs become complex; introduces tuple ownership, projection and consistency work |
| [SpiceDB](https://authzed.com/docs/spicedb/concepts/consistency) | Relationship schema, permission checks, caveats and consistency tokens | Distributed checks, cache and datastore; revision freshness is explicit | Adopt revision-aware authorization and read-after-write semantics. A graph engine is additional infrastructure; it does not provide login or solve Falcone data filtering automatically |
| [Cerbos](https://docs.cerbos.dev/cerbos/latest/index.html) | Resource/principal policies, RBAC/ABAC and policy decisions; APIs and policy tests | Stateless policy decision replicas with policy distribution | Useful separation of policy decision and enforcement. OSS PDP is distinct from commercial management offerings. Falcone must own trusted attributes, grants and synchronized policy versions |
| [Open Policy Agent](https://www.openpolicyagent.org/docs) | Rego policy evaluation, bundles, decision APIs and tests | Embedded, sidecar or remote evaluation; bundle distribution controls freshness | Flexible conditional policy reference. Extra language/tooling and stale input risk; keep tenant rules bounded and auditable rather than exposing unrestricted policy execution |
| [Casbin](https://v3.casbin.org/docs/overview) | Embedded authorization models including RBAC/ABAC; model, storage-adapter and synchronization extensions | In-process decisions; applications own replicated policy consistency | Lightweight evaluation option. Unlike Keycloak it supplies no identity/session stack; embedding everywhere risks divergent policy revisions unless distribution is disciplined |

## Features to take into Falcone

These are original requirements inspired by public designs, not a plan to copy source code wholesale.

| Pattern | Reference | Falcone decision | Backlog |
|---|---|---|---|
| Protocol engine separate from product UX and user lifecycle | Hydra/Kratos | Reuse a qualified library; own Falcone API and UI orchestration | CON, AUT, SES |
| Organization and application administration | ZITADEL, Casdoor | Keep Falcone tenant/workspace IDs, delegated membership and custom roles | IDN, RBAC, FED |
| Composable login and federation | authentik, Dex, Authelia | Reviewed flow primitives, provider adapters, MFA and step-up; no tenant code in IAM | AUT, FED |
| Relationship-aware sharing | OpenFGA, SpiceDB | Preserve a decision interface that can gain a graph backend later; do not require one for existing scoped RBAC | RBAC |
| Explicit decision freshness | SpiceDB | Policy revision, minimum required revision, lease expiry and safe read-after-write | SES, REV |
| Policy decision separated from enforcement | Cerbos, OPA, Casbin | Central contract with shared fixtures and scoped data projections; resource services still enforce | RBAC, INT |
| Lifecycle, standards and federation breadth | Keycloak | Preserve in-use capabilities and standards, qualify custom service before retirement | MIG, DEV |

## Licensing and maturity qualification

Repository metadata on the review date reports Apache-2.0 for Hydra, Kratos, Casdoor, Dex, Authelia, OpenFGA, SpiceDB, Cerbos and OPA; ZITADEL reports AGPL-3.0. [authentik's license](https://github.com/goauthentik/authentik/blob/main/LICENSE) distinguishes MIT-covered code from enterprise code. Casbin's exact chosen language package and all transitive dependencies still require release-specific review. These are intake observations, not a legal compatibility determination or a project-license choice.

Use exact tags and license files during dependency intake. Ory and authentik offer commercial/managed functionality beyond the selected OSS artifacts; Cerbos Hub is not the same deliverable as the OSS PDP. A maintained reference project does not make our implementation or its chosen configuration certified. Survey maturity does not substitute for security review, release cadence assessment, restore tests and a patch owner.

The [proposed protocol library](https://github.com/panva/node-oidc-provider) is a separate implementation component, not another full IAM platform. Its certification history supports evaluating it; Falcone must qualify its own adapters and selected conformance profile.
