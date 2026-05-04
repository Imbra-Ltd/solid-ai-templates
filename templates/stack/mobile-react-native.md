# Stack — React Native Mobile Application
[DEPENDS ON: templates/base/core/git.md, templates/base/core/docs.md, templates/base/core/quality.md, templates/base/language/typescript.md, templates/stack/spa-react.md, templates/backend/auth.md]

Extends the React SPA stack with React Native and Expo conventions. Covers
mobile-specific project structure, navigation, platform APIs, offline
behaviour, and testing.

---

## Stack
[ID: react-native-stack]

- Language: TypeScript (strict mode)
- Framework: React Native 0.73+
- Workflow: [Expo (managed) / Expo (bare) / React Native CLI]
- Navigation: Expo Router (file-based) / React Navigation 6+
- State: [Zustand / Jotai / React context]
- Server state: TanStack Query
- Styling: StyleSheet API / [NativeWind / Tamagui]
- HTTP client: fetch / axios
- Test runner: Jest + React Native Testing Library
- Package manager: [npm / pnpm]
- Distribution: [Expo EAS Build / Fastlane / manual]

---

## Project structure
[ID: react-native-structure]

```
app/                         # Expo Router: file-based routing
  (tabs)/
    index.tsx                # home tab
    [tab].tsx
  _layout.tsx                # root layout — navigation, providers
  +not-found.tsx
src/
  components/
    [Feature]/
      [Feature].tsx
      [Feature].test.tsx
  hooks/                     # custom hooks (use[Name].ts)
  services/                  # API calls — no business logic in components
  stores/                    # global state
  types/                     # shared TypeScript types
  utils/                     # pure utility functions
assets/
  fonts/
  images/
app.json                     # Expo config
tsconfig.json
package.json
README.md
CLAUDE.md
```

---

## TypeScript conventions
[EXTEND: react-spa-typescript]

- Strict mode enforced — same rules as `react-spa.md`
- Platform-specific files use `.ios.tsx` / `.android.tsx` suffixes —
  only when the difference cannot be handled with `Platform.select()`
- Prefer `Platform.select({ ios: ..., android: ..., default: ... })`
  over platform-specific files for small differences

---

## Component conventions
[EXTEND: react-spa-components]

- Use `StyleSheet.create()` for all styles — no inline style objects
  except for dynamic/computed values
- Never use web-only HTML elements — use `View`, `Text`, `Pressable`,
  `ScrollView`, `FlatList`, etc.
- `Pressable` over `TouchableOpacity` for new interactive elements
- `FlatList` or `FlashList` for long lists — never `ScrollView` with
  a `.map()` for more than ~20 items
- Test on both iOS and Android before marking a feature complete

---

## Navigation
[ID: react-native-navigation]

- File-based routing with Expo Router — directory structure mirrors URL/screen structure
- Deep link support configured in `app.json` under `expo.scheme`
- Type-safe navigation params — use Expo Router's typed routes or
  React Navigation's `RootStackParamList`
- Never navigate by manipulating state — always use the navigation API
- Handle back button on Android explicitly for modals and custom flows

---

## Platform APIs and permissions
[ID: react-native-platform]

- Request permissions at the moment they are needed — not at app launch
- Explain why a permission is needed before the system prompt appears
- Handle permission denial gracefully — never assume granted
- Use Expo SDK modules for device APIs (camera, location, notifications,
  file system) — avoid bare `react-native` platform modules unless the
  Expo equivalent does not exist
- Test permission flows on a real device — simulators do not always
  replicate permission behaviour accurately

---

## Offline and network
[ID: react-native-offline]

- Assume intermittent connectivity — never block the UI on a network call
  without a loading state and a retry option
- Cache read-heavy data with TanStack Query's `staleTime` and `gcTime`
- Use `NetInfo` to detect connectivity changes and surface a status
  indicator — do not silently fail
- Mutations that fail offline must be queued and retried when connectivity
  returns — use TanStack Query's `onlinePersister` or a manual queue

---

## State management
[EXTEND: react-spa-state]

- Local state: `useState` / `useReducer` for screen-scoped concerns
- Global state: Zustand for cross-screen shared state
- Server state: TanStack Query — same rules as `react-spa.md`
- Persist sensitive data (tokens, user ID) in `expo-secure-store` —
  never in `AsyncStorage`
- Non-sensitive persisted state (preferences, cached data) in `AsyncStorage`
  or via TanStack Query persistence

---

## Authentication
[EXTEND: backend-auth]

- Store access and refresh tokens in `expo-secure-store` — not `AsyncStorage`
- Intercept 401 responses to attempt token refresh before redirecting to login
- Biometric authentication via `expo-local-authentication` as an optional
  layer on top of token-based auth — not a replacement for it

---

## Testing
[EXTEND: base-testing]

- React Native Testing Library for component tests — same approach as `react-spa.md`
- Jest with `jest-expo` preset for the test runner
- Mock native modules that are not available in the Jest environment
- Component test naming: Given/When/Then
- E2E tests with Maestro or Detox — cover critical flows (onboarding, auth,
  key user journeys) on both iOS and Android simulators
- Run before every commit: `npm test && tsc --noEmit`

---

## Git conventions
[EXTEND: base-git]

- Do not commit `node_modules/`, `.expo/`, `ios/Pods/`, `android/build/`
- Lock file committed — do not delete it
- `ios/` and `android/` native directories committed for bare workflow;
  excluded for managed Expo workflow (generated on build)

---

## Commands
```
npx expo start           # develop — opens dev menu (iOS/Android/web)
npx expo start --ios     # develop — iOS simulator
npx expo start --android # develop — Android emulator
npm test                 # run Jest tests
tsc --noEmit             # type check
eas build --platform all # production build via Expo EAS
eas submit               # submit to App Store / Google Play
```