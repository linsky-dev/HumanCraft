---
name: skills-humancraft-references-accessibility
description: 'HumanCraft supporting resource: Accessibility and implementation. Read
  only when relevant to the current task.'
---

# Accessibility and implementation

For web products use WCAG 2.2 AA as a target where applicable; for native software also follow platform accessibility APIs and conventions. A quick audit is not conformance certification.

Use semantic elements, meaningful accessible names, programmatically associated labels, logical headings and keyboard order. Visible focus must not be obscured. Ensure modal focus behavior and escape where appropriate. Don't rely on color alone; use text or icons with accessible names. Normal text contrast target 4.5:1, large text 3:1; relevant non-text UI contrast 3:1 subject to WCAG exceptions. For WCAG 2.2 AA pointer target minimum see criterion 2.5.8 (24 by 24 CSS px or applicable exceptions); choose larger targets where context warrants. Support zoom/reflow, locale expansion, reduced motion, alternative to dragging and accessible authentication. Provide status announcements without flooding assistive technology. Avoid placeholders as the only labels.

Implementation checks: inspect DOM/accessibility tree or native equivalents, keyboard-only traversal, zoom, actual viewport, touch/keyboard alternatives, long content and relevant assistive technologies. Automated tools detect a subset; report manual checks separately. Do not declare compliance from automated tools alone. Respect native platform conventions, existing component library and contrast requirements.
