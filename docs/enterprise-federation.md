# Mandatory enterprise identity integrations

Scope accepted by the owner on 2026-11-01: **SAML, OIDC, LDAP/AD and SCIM must all be supported**. This document proposes concrete initial profiles so implementation and acceptance are measurable. Provider versions, protocol options and deployment settings are qualified in IAM-FED-002; the four protocol families themselves are no longer open questions.

## Initial implementation profile

| Protocol | Proposed Falcone role and coverage | Qualification |
|---|---|---|
| OIDC | Provider for Falcone/external applications and relying party for corporate sign-in; existing SES-001 and FED-001 scope | Code/PKCE, issuer/audience binding, trusted discovery, key rotation, explicit subject mapping and session lifecycle |
| SAML 2.0 | Service provider for inbound corporate login and identity provider for outbound application SSO | Browser SSO, selected POST/Redirect bindings, metadata, signed messages, certificate rollover, NameID/attributes and documented logout behavior |
| LDAP/AD | Connector to generic LDAPv3 and Active Directory for authentication and controlled user/group synchronization | Validated TLS, compatible bind mode, scoped search, stable identifiers, group mapping, disabling/removal and outage/reconciliation behavior |
| SCIM 2.0 | Service provider accepting enterprise User/Group lifecycle updates and managed client provisioning connected applications | Core resources/discovery, supported CRUD/PATCH/filter/pagination behavior, source ownership, protected credentials and reconciliation |

LDAP/AD support means integration with an existing directory, not implementing an LDAP server or Active Directory domain controller. SCIM is lifecycle provisioning, not a substitute for login authentication. Supporting these protocols does not give a caller the right to choose roles, tenant IDs or workspace ownership.

## Shared Falcone identity boundary

All adapters resolve an external identity into the same Falcone principal and explicit tenant/workspace memberships. For OIDC, use the verified issuer/subject pair. For SAML, use the configured trusted provider and qualified NameID/subject mapping. Directory identities use connector-scoped immutable entry identifiers rather than a renameable DN. SCIM keeps stable server IDs and separately scoped external mappings. Never merge users merely because email addresses match.

Every connector belongs to a tenant and has an explicit administrative owner. Claim and group mappings can assign only approved, delegable tenant/workspace roles. They cannot silently create platform privileges or tenant ownership. Authentication method/assurance feeds Falcone MFA and step-up policy; an upstream success does not automatically satisfy local administrator assurance requirements.

External systems retain external credentials. Falcone owns its local credentials and sessions. Attribute/membership authority is configured per source and field. A read-only directory field cannot be overwritten locally then pushed back by SCIM. Source tracking and revision checks prevent cycles and stale membership resurrection.

## Component responsibilities

| Adapter | Reused Falcone components | Additional responsibility |
|---|---|---|
| SAML | Interaction/session service, membership resolver, signing-key custody, audit | Qualified XML-security library, SP/IdP configuration, metadata trust and replay state |
| LDAP/AD | Secret custody, memberships, group mapping, outbox and revocation | TLS/bind/search, directory policy compatibility, synchronization checkpoints and reconciliation |
| SCIM | Lifecycle transactions, role-delegation checks, machine credentials, outbox | Protocol validation, resource/attribute mapping, version conflicts and outbound delivery status |

The proposed OIDC library supplies none of these additional protocol implementations. Select maintained components during P0, preserve Falcone-native administration APIs and keep adapters inside the custom service boundary. Synchronization workers use ordinary restricted workloads; no extra operator or privileged directory agent is assumed.

## Acceptance and failure rules

For SAML, validate the exact signed content and expected issuer, audience, destination/recipient, request association and validity window; reject replays and unsafe XML. Certificate rollover and explicit trust changes require audit. Document single-logout support and incomplete remote logout; never promise universal logout of all upstream sessions. Optional profiles and unsolicited login are enabled only after explicit review.

For LDAP/AD, require validated LDAPS or StartTLS without downgrade, escaped filters and least-privilege directory credentials. Test generic LDAP and actual AD environments separately. Signing/channel-binding requirements depend on the chosen authentication mechanism and corporate policy; do not claim that simple TLS bind satisfies every AD policy. Failed or partial scans must not be interpreted as mass deletion. Directory availability cannot trigger a silent insecure local-password fallback.

For SCIM, authenticate every connector and bind it to its tenant before resolving resource identifiers. Implement the declared resource operations and advertise unsupported optional capabilities accurately. Treat `active=false`, deletion and group removal as lifecycle changes governed by the same Falcone authorization and audit rules. A tenant-scoped provisioning operation must not disable another tenant's membership. Outbound retries reconcile ambiguous outcomes rather than assuming exactly-once remote side effects.

The existing online revocation target starts at **authoritative Falcone commit**. Total external deprovisioning time also includes detection: LDAP polling delay or SCIM delivery delay, transaction acceptance, then Falcone propagation. Record and monitor each part. Do not claim a 30-second end-to-end directory-disable guarantee merely because internal propagation has a 30-second target. Set detection/freshness budgets per connector and stop granting sensitive access from state that exceeds its approved lease.

## Release evidence

- IAM-FED-001 / IAM-SES-001: OIDC relying-party and provider fixtures.
- IAM-FED-004: reference inbound SAML IdP and outbound SAML SP, including negative and rollover cases.
- IAM-FED-005: generic LDAP plus Active Directory, including rename, nested groups, disablement, outages and synchronization recovery.
- IAM-FED-006: reference SCIM provisioning client and target provider, including conflicting updates, cross-tenant attempts and deprovisioning.
- IAM-DEV-003: independent security/isolation qualification covering all four protocol families; IAM-MIG-002/003 require this evidence before canary completion and retirement.

Missing current production usage does not waive a protocol test. A reference integration provides evidence until the actual corporate provider is available; compatibility with that provider is claimed only after its own qualification.

## Primary references

[OASIS SAML standard and approved errata](https://wiki.oasis-open.org/security/), [SAML security considerations](https://docs.oasis-open.org/security/saml/v2.0/saml-sec-consider-2.0-os.pdf), [OIDC Core](https://openid.net/specs/openid-connect-core-1_0.html), [SCIM schema RFC 7643](https://datatracker.ietf.org/doc/rfc7643/), [SCIM protocol RFC 7644](https://www.rfc-editor.org/info/rfc7644/), [Microsoft LDAP signing](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/ldap-signing) and [channel binding](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/ldap-channel-binding). Reviewed 2026-11-01. Falcone profiles and acceptance gates above are engineering requirements, not claims of upstream certification.
