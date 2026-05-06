# Mobile — Authentication
[ID: mobile-auth]
[DEPENDS ON: templates/base/security/security.md]

Authentication rules for native mobile applications. Overrides
web-specific token transport (httpOnly cookies) with platform
secure storage.

---

## Token storage
[ID: mobile-auth-token-storage]

- Store access and refresh tokens in the platform's secure enclave:
  `expo-secure-store` (React Native) or `flutter_secure_storage`
  (Flutter) — never in `AsyncStorage`, `SharedPreferences`,
  `localStorage`, or plain files
- Tokens are encrypted at rest by the OS keychain (iOS Keychain /
  Android Keystore) — do not add a custom encryption layer on top
- Access tokens sent in the `Authorization: Bearer <token>` header
  — same as backend clients
- Clear all tokens on logout — wipe both access and refresh tokens
  from secure storage in a single operation

---

## Token refresh

- Implement a transparent refresh interceptor in the HTTP client
  (Axios interceptor / Dio interceptor) — the rest of the app
  must not know about token expiry
- On 401 response: attempt a single refresh; if refresh fails,
  redirect to the login screen
- Queue concurrent requests during a refresh — do not fire
  multiple refresh calls in parallel
- Rotate refresh tokens on every use — the server issues a new
  refresh token with each refresh response

---

## Biometric authentication

- Biometric unlock (Face ID, Touch ID, fingerprint) is an
  optional convenience layer — not a replacement for server-side
  token-based authentication
- Gate biometric enrolment behind an opt-in setting — never
  enable silently
- Fall back to PIN / password if biometric authentication fails
  or is unavailable
- Use platform APIs: `expo-local-authentication` (React Native)
  or `local_auth` (Flutter)

---

## Session lifecycle

- Persist the refresh token across app restarts — the user
  should not re-authenticate on every cold start
- Invalidate all local tokens when the server signals revocation
  (e.g. password change, account lock)
- On app backgrounding, do not clear tokens — mobile users
  switch apps frequently; clearing forces unnecessary re-login
- Set a maximum offline session duration — if the app has not
  contacted the server within a configurable window, force
  re-authentication on next foreground
