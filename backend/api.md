# Backend — API Design
[ID: backend-api]

## API-first
- Software MUST be designed API-first — define the contract before writing
  implementation
- Exceptions require a documented Architecture Decision Record (ADR)
- API-first enables: multiple clients (web, mobile) sharing one contract,
  headless testing, and API-as-a-product exposure

## API types
- REST — SHOULD be the default choice
- gRPC — SHOULD be used for internal service-to-service communication where
  performance is critical
- GraphQL — COULD be used for frontend-facing APIs where flexible querying
  is needed
- Other types (SOAP, WebSockets) require a per-case ADR

## OpenAPI specification
- Every API MUST have an OpenAPI specification
- The spec MUST be kept up to date — a stale spec is worse than no spec
- Include: all resources, methods, parameters, response schemas, error responses,
  and authentication requirements
- Provide a changelog documenting API changes across versions

## Versioning
- APIs in a given version MUST maintain backward compatibility
- Version the API in the URI path prefix: `/v1/`, `/v2/`
- Start versioning from `v1`; introduce `v2` only when breaking changes are
  unavoidable
- Alternatively, use a custom request header: `Api-Version: 2`
- MUST NOT use media type to control API versions

## Backward compatibility
Breaking changes require a new major version. A change is breaking when:
- A field or object is removed or renamed in the response
- A field type is changed
- The authentication type changes
- An HTTP verb or URI path changes
- The protocol or Content-Type changes
- Business logic or flow changes in a way that alters observable behaviour

A change is **not** breaking when:
- A new field or object is added to the response
- A new path or HTTP verb is added
- Additional optional query parameters are added

## Deprecation strategy
When a breaking change is introduced:

1. Deploy the new version alongside the old one
2. Add the `Deprecation` header to all responses from the old version:
   `Deprecation: @1688169599` (Unix timestamp of when it became deprecated)
3. Optionally add the `Sunset` header with the removal date:
   `Sunset: Sat, 31 Dec 2025 23:59:59 GMT`
4. Notify all consumers and agree on a migration timeline
5. Remove the old version only after the sunset date has passed

```
Deprecation: @1688169599
Sunset: Sat, 31 Dec 2025 23:59:59 GMT
```

## Statelessness
- APIs MUST be stateless — no client context stored on the server between requests
- All information needed to process a request MUST be in the request itself
- Session state belongs in the client or a dedicated session store, not in the
  API service

## Pagination
- Collection endpoints MUST be paginated — never return unbounded lists
- Use `limit` and `offset` (or cursor-based) pagination
- Include navigation links (`next`, `prev`) in the response per HATEOAS
  (see `backend/http.md`)