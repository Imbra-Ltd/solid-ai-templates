# Base — TypeScript
[ID: base-typescript]
[DEPENDS ON: base/quality.md]

## Type design
[ID: base-typescript-type-design]

- Use `interface` for object shapes; use `type` for unions and aliases
- Use discriminated unions (tagged unions) for type families — a literal
  `type` or `kind` field plus a union is safer than class hierarchies
- Compose sub-interfaces when a domain has multiple categories with
  different fields; keep single-purpose types flat
- No enums — use `as const` objects or string literal unions
- No `any` — use `unknown` and narrow, or define a proper type

## Naming
[ID: base-typescript-naming]

- Booleans: prefix with `is`, `has`, or `can` (`isActive`, `hasPermission`)
- Import types with `import type { ... }`
- Explicit return types on non-trivial functions

## Strictness
[ID: base-typescript-strictness]

- `strict: true` — no exceptions
- Follow `@typescript-eslint/recommended`
