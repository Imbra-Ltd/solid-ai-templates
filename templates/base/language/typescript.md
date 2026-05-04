# Base — TypeScript
[ID: base-typescript]
[DEPENDS ON: templates/base/core/quality.md]

## Type design
[ID: base-typescript-type-design]

- Use `interface` for object shapes; use `type` for unions and aliases
- Use discriminated unions (tagged unions) for type families — a literal
  `type` or `kind` field plus a union is safer than class hierarchies
- Compose sub-interfaces when a domain has multiple categories with
  different fields; keep single-purpose types flat
- When declaring data arrays that use a discriminated union, type each
  section with its specific sub-interface (`FlashItem[]`), not the
  broad union (`Item[]`) — spread into the union array at the end
- No enums — use `as const` objects or string literal unions
- No `any` — use `unknown` and narrow, or define a proper type

## Naming
[ID: base-typescript-naming]

- Booleans: prefix with `is`, `has`, or `can` (`isActive`, `hasPermission`)
- Import types with `import type { ... }`
- Explicit return types on non-trivial functions

## Comments
[ID: base-typescript-comments]

- Prefer self-documenting names — a field that needs a comment needs a
  better name (see `templates/base/core/quality.md`)
- Use inline comments for units that cannot be encoded in the name:
  `weight: number; // grams` not a standalone `// Grams` above the field
- Keep inline comments lowercase, short, and consistent across the interface

## Strictness
[ID: base-typescript-strictness]

- `strict: true` — no exceptions
- Follow `@typescript-eslint/recommended`
