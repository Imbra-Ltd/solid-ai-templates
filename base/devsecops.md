# Base — DevSecOps
[ID: base-devsecops]

## Principle
Security is not a phase — it is part of every build, review, and release.
Detect risks as early as possible in the development process.

## SAST (Static Application Security Testing)
- SAST MUST run in every CI pipeline
- A failed SAST scan MUST fail the build — code with security issues cannot
  be merged or deployed
- Fix SAST findings before merging; document false positives explicitly

## SCA (Software Composition Analysis)
- All dependencies MUST be tracked for known vulnerabilities and license risks
- SCA MUST run on every deployment to QA, staging, and production
- A SBOM (Software Bill of Materials) MUST be generated per release
- Dependencies with unacceptable licenses MUST NOT be merged

## Secret detection
- Secret detection MUST run in CI — commits containing credentials, tokens,
  or API keys MUST be rejected
- Never store sensitive information in source files, commit history, issue
  trackers, or documentation tools
- Secrets used at runtime MUST be stored in a secret vault — never in
  environment files committed to the repository

## License compliance
- Before adding a dependency, verify its license is acceptable
- Copyleft licenses (GPL, AGPL) require explicit approval before use
- Document and justify any dependency with a non-standard or ambiguous license

## DAST (Dynamic Application Security Testing)
- DAST MUST run against the staging/QA environment after every deployment
- Never run DAST against production
- Automated DAST scans MUST complete before any production release
- Critical findings MUST block the release and be treated as incidents
- Lower-severity findings MUST be tracked and resolved within a defined timeframe

## IaC scanning (Infrastructure-as-Code)
- All infrastructure code (Terraform, Dockerfiles, Helm charts, Kubernetes
  manifests) MUST be scanned for security misconfigurations in CI
- A failed IaC scan MUST fail the build — the same rule as SAST
- Common issues to detect: overprivileged roles, exposed ports, unencrypted
  storage, hardcoded values, use of `latest` image tags
- IaC scan results MUST be reviewed in the same PR that introduces the change

## Penetration testing
- Schedule regular penetration testing by a qualified party
- Critical findings (severity A) MUST be treated as incidents and resolved
  immediately
- Lower-severity findings MUST be tracked and resolved within a defined
  timeframe

## Dependency hygiene
- Keep dependencies up to date — unpatched dependencies are a security risk
- Remove unused dependencies promptly
- Prefer dependencies that are actively maintained and widely adopted