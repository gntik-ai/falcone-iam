# ADR 0002 — Mandatory enterprise identity protocols

Date: 2026-11-01. Status: **accepted for product scope**, explicitly confirmed by the owner. Detailed implementation choices still require qualification.

## Decision

`falcone-iam` must support **SAML, OIDC, LDAP/AD and SCIM**. These are required capabilities of the custom Falcone service. They are not conditional on whether a current tenant uses them, and they cannot be deferred as optional enhancements to declare the Keycloak replacement complete.

## Consequences

- Retain the existing OIDC provider and upstream federation stories.
- Add dedicated implementation stories for SAML 2.0, LDAP/Active Directory and SCIM 2.0. The [enterprise profile](../enterprise-federation.md) makes their initial implementation scope concrete.
- Route all protocols through the same Falcone principal, membership, custom-role, tenant/workspace, audit and revocation contracts.
- Qualify the distinct libraries/adapters needed; an OIDC library does not supply SAML, directory or SCIM functionality.
- Require all four protocol families to pass interoperability, isolation and lifecycle tests before Keycloak retirement. A temporary bridge is a migration mechanism, not completion of first-party support.

## Boundary of this decision

The owner confirmed the four protocol families. The proposed profiles and directions in the enterprise document are planning detail to qualify against actual corporate providers; this decision does not claim support for every optional standard extension or accept unrelated open questions. Other architecture choices retain their existing status.
