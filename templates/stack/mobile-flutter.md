# Stack — Flutter Mobile Application
[DEPENDS ON: templates/base/core/git.md, templates/base/core/docs.md, templates/base/core/quality.md, templates/backend/auth.md]

A cross-platform mobile (iOS + Android) application built with Flutter and
Dart. Covers project structure, widget conventions, state management, routing,
platform integration, and testing.

---

## Stack
[ID: flutter-stack]

- Language: Dart 3+
- Framework: Flutter (stable channel, latest stable)
- State management: [Riverpod / Bloc / Provider]
- Routing: [go_router / auto_route]
- HTTP client: Dio / http
- Serialisation: json_serializable + freezed
- Dependency injection: [Riverpod / get_it]
- Test runner: flutter_test (unit + widget) + integration_test
- Distribution: [Fastlane / Codemagic / manual]

---

## Project structure
[ID: flutter-structure]

```
lib/
  main.dart                  # entry point — wires providers, runs app
  app.dart                   # MaterialApp / CupertinoApp, routing, theme
  [feature]/
    data/
      [feature]_repository.dart   # data access — remote + local
      [feature]_api.dart          # HTTP calls
      [feature]_dto.dart          # JSON serialisable DTOs
    domain/
      [feature]_model.dart        # pure domain models (freezed)
      [feature]_repository.dart   # abstract repository interface
    presentation/
      [feature]_screen.dart       # screen widget — thin
      [feature]_controller.dart   # Riverpod notifier / Bloc
      widgets/
        [widget].dart
  core/
    network/
      api_client.dart        # Dio instance, interceptors
    storage/
      secure_storage.dart    # flutter_secure_storage wrapper
    theme/
      app_theme.dart
    router/
      app_router.dart
test/
  [feature]/
    [feature]_test.dart
integration_test/
  app_test.dart
pubspec.yaml
analysis_options.yaml
README.md
CLAUDE.md
```

---

## Dart conventions
[ID: flutter-dart]

- Follow the official **Dart style guide** — enforced by `dart format` and
  `flutter analyze`; do not suppress analysis warnings without a documented reason
- `analysis_options.yaml` with `flutter` lints enabled — commit it
- Prefer `final` for all local variables and fields that are not reassigned
- Use `const` constructors wherever possible — reduces widget rebuilds
- No dynamic typing — avoid `dynamic`; use explicit types or generics
- Null safety enforced — no `!` force-unwrap without a comment explaining
  why null is impossible at that point

---

## Widget conventions
[ID: flutter-widgets]

- One widget per file — filename in `snake_case`, class name in `PascalCase`
- Prefer `StatelessWidget` — only use `StatefulWidget` when local ephemeral
  state (animations, focus, scroll position) cannot be lifted to a controller
- Keep `build()` methods short — extract sub-widgets into separate classes,
  not private methods, so Flutter can optimise rebuilds
- Use `const` widget constructors wherever all arguments are compile-time constants
- Never put business logic or data fetching inside a widget — delegate to
  a controller/notifier

---

## State management (Riverpod)
[ID: flutter-state]

- Define providers at the top level of a file — never inside a widget class
- Use `AsyncNotifierProvider` for async data; `NotifierProvider` for sync state
- Expose immutable state — use `freezed` data classes for state objects
- Do not read providers inside `build()` before their data is available without
  handling the loading and error states via `when()` / `AsyncValue`
- Keep providers small and composable — one concern per provider

---

## Routing
[ID: flutter-routing]

- All routes defined in `app_router.dart` — no `Navigator.push()` with
  hardcoded widget constructors scattered through the codebase
- Type-safe route parameters — use `go_router`'s typed routes or `auto_route`
- Deep links and push notification navigation handled in the router —
  not in individual screens
- Handle the back stack explicitly for authentication flows —
  replace, not push, after login/logout

---

## Data layer
[ID: flutter-data]

- Abstract repository interfaces in `domain/` — concrete implementations in `data/`
- DTOs in `data/` are JSON-serialisable (via `json_serializable`) —
  never pass DTOs to the presentation layer; map to domain models
- Use `freezed` for immutable domain models and union types
- All HTTP calls in `*_api.dart` files — never inline `Dio.get()` in a widget
  or controller
- Run `dart run build_runner build` after modifying `freezed` or
  `json_serializable` annotated classes

---

## Authentication
[EXTEND: backend-auth]

- Store tokens in `flutter_secure_storage` — never in `SharedPreferences`
- Refresh tokens via a Dio interceptor — transparent to the rest of the app
- Biometric auth via `local_auth` as an optional unlock layer —
  not a replacement for server-side authentication

---

## Platform and permissions
[ID: flutter-platform]

- Declare all required permissions in `AndroidManifest.xml` and
  `Info.plist` — document why each permission is needed in a comment
- Request permissions at the point of use with `permission_handler` —
  not at app launch
- Handle permission denial gracefully — show an explanation and a
  settings deep link if the user has permanently denied
- Test on real devices for camera, location, Bluetooth, and biometrics —
  simulators do not replicate all platform behaviours

---

## Testing
[EXTEND: base-testing]

- Unit tests (`flutter_test`): test controllers/notifiers, repositories,
  and pure functions — no Flutter widgets
- Widget tests: test individual widgets and screens with `WidgetTester` —
  mock providers with `ProviderScope` overrides
- Integration tests (`integration_test`): end-to-end flows on a real device
  or emulator — cover onboarding, authentication, and key user journeys
- Mock HTTP with `mockito` or `http_mock_adapter` — never hit real endpoints
  in tests
- Test naming: `<unit>_<state>_<expected>`
  e.g. `loginController_invalidCredentials_returnsAuthError`
- Run before every commit: `flutter test && flutter analyze`

---

## Git conventions
[EXTEND: base-git]

- Do not commit `build/`, `.dart_tool/`, `*.g.dart`, `*.freezed.dart` if
  generated files are excluded — document the regeneration step in README
- Commit generated files if the CI does not run `build_runner` — keep the
  choice consistent and document it
- `pubspec.lock` is committed — do not delete it

---

## Commands
```
flutter run                  # develop — hot reload on connected device/emulator
flutter run --release        # test release build locally
flutter test                 # run unit and widget tests
flutter test integration_test/  # run integration tests (device required)
flutter analyze              # static analysis
dart format .                # format all Dart files
dart run build_runner build  # regenerate freezed / json_serializable code
flutter build apk            # Android release build
flutter build ios            # iOS release build (macOS required)
```