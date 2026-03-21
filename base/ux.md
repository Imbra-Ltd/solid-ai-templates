# Base — UX Principles
[ID: base-ux]

## UX principles
- Mobile-first — design for small screens first, enhance for larger ones
- Progressive disclosure — show only what the user needs at each step
- No dark patterns — no misleading UI, no forced actions, no hidden costs
- Consistency — same interaction patterns throughout the product
- Performance is UX — slow interfaces are bad user experience

## Accessibility — WCAG 2.1 AA
- Target standard: WCAG 2.1 AA
- Minimum text contrast ratio: 4.5:1 (normal text), 3:1 (large text)
- All interactive elements reachable and operable by keyboard
- Focus indicators must be visible at all times
- No content that relies on colour alone to convey meaning
- Images must have descriptive `alt` text; decorative images use `alt=""`
- Semantic HTML: correct landmark elements and heading hierarchy
- `aria-label` on all interactive elements (buttons, icon links, social links)
- All `<a>` elements with icon-only or ambiguous text must have a descriptive
  `aria-label`
- Keyboard navigation: menus must close on Escape and restore focus

## Responsive breakpoints
- Tablet: max-width 1024px
- Mobile: max-width 768px
- Small mobile: max-width 480px

## Browser support
- Default target: last 2 versions of Chrome, Firefox, Safari, and Edge
- Progressive enhancement: graceful degradation for unsupported features
- [OVERRIDE: base-ux-browsers] to specify a different support matrix