# Base — Release Management
[ID: base-release]

## Versioning
- All packages and services MUST follow semantic versioning (`MAJOR.MINOR.BUILD.PATCH`)
- MAJOR — breaking changes
- MINOR — new backward-compatible functionality
- BUILD - increments that belong to the next release
- PATCH — backward-compatible bug fixes

## Version bump propagation
When upgrading a dependency, the consuming package MUST bump its own version
to the same level or higher:
- Dependency bumps MINOR → consumer MUST bump at least MINOR (not just PATCH)
- Dependency bumps MAJOR → consumer MUST bump MAJOR

> Rationale: A patch bump implies a drop-in replacement. If a dependency
> changed its minor version, the consumer is no longer a drop-in replacement
> of its previous patch — failing to bump breaks downstream consumers.

## Backward compatibility
- APIs SHOULD remain backward compatible across minor and patch versions
- Never remove or rename a field in a response without a deprecation period
- Communicate breaking changes to all consumers before making them

## Cut-over phases
When a breaking change is unavoidable:

1. Deploy the new version alongside the old one
2. Notify all consumers that the old version is deprecated and set a removal date
3. Allow consumers to migrate at their own pace within the deprecation window
4. Remove the old version only after the window has closed

```
Server:   [--- v1 ---|--- v1 + v2 ---|--- v2 ---]
Client A: [--- v1 ---|------ v2 -----]
Client B: [--- v1 ----------|-------- v2 --------]
```

## Release gate
- MUST: All automated tests (unit, integration, e2e) MUST be green on the
  staging/QA environment before releasing to production
- If tests are not green, DO NOT release to production
- The team consuming a service is responsible for verifying the overall
  system — not just the service under change
