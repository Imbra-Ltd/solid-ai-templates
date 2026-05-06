# Mobile — UX and Accessibility
[ID: mobile-ux]
[DEPENDS ON: templates/base/core/quality.md]

Mobile-specific UX principles and accessibility rules. Replaces
browser-centric guidance (WCAG viewports, axe, Lighthouse, CSS
media queries) with native platform equivalents.

---

## UX principles

- Design for one-handed use — primary actions within thumb reach
- Progressive disclosure — show only what the user needs at each step
- Performance is UX — 60 fps minimum; janky scrolling is a bug
- Respect platform conventions — iOS and Android have distinct
  interaction patterns (back gesture, navigation bar, pull-to-refresh);
  do not force one platform's idioms on the other
- Offline-first — assume intermittent connectivity; never block
  the UI without a loading state and a retry option

---

## Touch targets

- Minimum touch target: 48 × 48 dp (Android Material) /
  44 × 44 pt (Apple HIG) — smaller targets cause mis-taps
- Spacing between adjacent targets: ≥ 8 dp — prevent accidental
  activation of the wrong control
- Interactive elements at screen edges need extra padding —
  system gestures compete for the same space

---

## Accessibility — screen readers

- Target standard: WCAG 2.1 AA adapted for native platforms
- Every interactive element MUST have a screen-reader label:
  `accessibilityLabel` (React Native) or `Semantics(label:)`
  (Flutter)
- Images: provide `accessibilityLabel` for informative images;
  mark decorative images as `accessibilityElementsHidden` (RN)
  or `Semantics(excludeSemantics: true)` (Flutter)
- State changes (loading, error, success) MUST be announced:
  use `AccessibilityInfo.announceForAccessibility()` (RN) or
  `SemanticsService.announce()` (Flutter)
- Group related elements into a single accessible unit where
  appropriate — a card with title + subtitle + action should
  announce as one item, not three

---

## Accessibility — navigation

- Focus order follows the visual reading order (top-to-bottom,
  leading-to-trailing)
- Modals and bottom sheets MUST trap focus and restore it on
  dismiss
- Screen reader users MUST be able to reach all interactive
  elements — hidden overflow does not excuse inaccessible
  controls

---

## Accessibility testing

### Automated

- Lint for missing accessibility labels in CI — use
  `eslint-plugin-react-native-a11y` (React Native) or
  custom lint rules with `dart analyze` (Flutter)

### Manual (before shipping new screens)

- **VoiceOver** (iOS): enable in Settings → Accessibility;
  navigate every screen; verify all elements are announced
  with correct labels, roles, and state
- **TalkBack** (Android): enable in Settings → Accessibility;
  same verification as VoiceOver
- **Switch Control / Switch Access**: verify the app is usable
  with external switch devices (required for motor impairment)
- **Dynamic type / font scaling**: verify layout at the largest
  system font size — no text clipping or overlapping

### Criteria for done

A feature is not complete until:

- [ ] Every interactive element has an accessibility label
- [ ] VoiceOver walkthrough completed on iOS
- [ ] TalkBack walkthrough completed on Android
- [ ] Layout verified at maximum system font size
