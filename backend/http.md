# Backend — HTTP Conventions
[ID: backend-http]

## Handler design
- Handlers are thin: decode request → call service → encode response
- No business logic in handlers — delegate to a service layer
- Validate all incoming request data before processing

## URI design
- Use lowercase letters and hyphens to separate words — never underscores or camelCase
- Use nouns, not verbs: `/orders`, not `/getOrders`
- Use plural nouns for collections: `/orders`, `/products`
- Use singular for individual resources beneath a collection: `/orders/{orderId}`
- Use hierarchical paths for related resources: `/customers/{id}/orders`
- A URI MUST NOT end with a trailing slash
- Use American English — no abbreviations or acronyms in URIs

## Query parameters
- Use camelCase for query parameter names
- Use query parameters for filtering, sorting, and pagination
- Reserved names — do not use these for other purposes:
  `limit`, `skip`, `offset`, `expand`, `sortedBy`

## Request headers
- Use Hyphenated-Pascal-Case for all HTTP headers: `Order-Metadata-Header`
- Custom headers SHOULD NOT use the `X-` prefix (deprecated per RFC 6648)

## HTTP methods
| Method | Use for | Idempotent |
|--------|---------|-----------|
| GET | Retrieve a resource or collection — no side effects | Yes |
| POST | Create a new resource — server assigns URI | No |
| PUT | Replace a resource entirely | Yes |
| PATCH | Partially update a resource | No |
| DELETE | Remove a resource | Yes |

## Resource representation
- Use JSON as the default format; XML where explicitly required
- Use ISO standards for field types:
  - Dates/times: ISO 8601
  - Languages: ISO 639
  - Countries: ISO 3166-1 alpha-2
  - Currencies: ISO 4217
- Integers larger than 9007199254740992 (2^53) MUST be represented as strings
  to avoid JavaScript floating-point precision loss
- Include only necessary fields — keep response payloads small

## HATEOAS
- Embed hyperlinks in responses to enable resource discovery
- Use a `links` array with `href`, `rel`, `type`, and `media` fields:
  ```json
  "links": [
    {
      "href": "documents/a12231e4-46ef-4adf-82e2-8a74fc017447",
      "rel": "documents",
      "type": "deliveryNote",
      "media": "application/pdf"
    }
  ]
  ```
- Support at minimum: `self`, `next`, `prev` relations on paginated collections

## Error responses
- Use consistent error response shape across all endpoints
- Follow RFC 9457 (`application/problem+json`) for error format
- Use 4xx for client errors, 5xx for server errors — never use 200 for errors
- Never return stack traces, internal paths, or implementation details to the client
- Set explicit `Content-Type: application/json` on all JSON responses

## Authentication and authorisation
- MUST use HTTPS — never serve APIs over plain HTTP
- Use token-based authentication with expiring access tokens (JWT)
- External APIs MUST have both authentication and authorisation
- Internal APIs SHOULD have at least authentication
- Never expose unauthenticated write endpoints