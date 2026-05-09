---
id: "0004"
title: "Fix Navbar Crash and Duplicate Language Switcher"
stage: "red"
date_iso: "2025-12-25"
surface: "agent"
model: "Gemini"
feature: "language-switcher"
branch: "main"
user: "user"
command: "None"
labels:
  - "bug"
  - "docusaurus"
  - "react"
  - "navbar"
  - "translation"
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - src/theme/NavbarItem/index.js
  - docusaurus.config.ts
  - src/theme/NavbarItem/custom-LanguageSwitcher/index.js
tests_yaml: |
  - Manual verification by restarting the dev server and observing UI behavior.
---

### PROMPT

> my app is running on local host-- i got this error: This page crashed
> Try again
> A theme navbar item failed to render.
> Please double-check the following navbar item (themeConfig.navbar.items) of your Docusaurus config:
> {
>   "type": "custom-LanguageSwitcher",
>   "position": "right"
> }
> Cause:
> No NavbarItem component found for type "custom-LanguageSwitcher".

---

> my app is running on local host-- i got this error: This page crashed
> Try again
> A theme navbar item failed to render.
> Please double-check the following navbar item (themeConfig.navbar.items) of your Docusaurus config:
> {
>   "type": "custom-LanguageSwitcher",
>   "position": "right"
> }
>
> Cause:
> No NavbarItem component found for type "custom-LanguageSwitcher".-- You will behave as expert React and docusaurus Developer and will fix this issue; Uncaught runtime errors:
> ×
> ERROR
> Script error.
>     at handleError (webpack-internal:///./node_modules/webpack-dev-server/client/overlay.js:589:58)
>     at eval (webpack-internal:///./node_modules/webpack-dev-server/client/overlay.js:613:7) - my nabar is showing two translation buttons- keep only one working button and removed second one--

### RESPONSE

Fixed a multi-part issue related to a custom Docusaurus navbar component.

1.  **Resolved Initial Crash:** The primary error "No NavbarItem component found" was caused by an improper component override in `src/theme/NavbarItem/index.js`. This file was intercepting all navbar item rendering but only had logic for `custom-AuthButton`, causing all others to fail. I modified it to also recognize and render the `custom-LanguageSwitcher` component.

2.  **Removed Duplicate Button:** The navbar displayed two translation controls because the Docusaurus configuration (`docusaurus.config.ts`) included both the built-in `localeDropdown` and our `custom-LanguageSwitcher`. I removed the `localeDropdown` to keep only the desired Google Translate component.

3.  **Fixed "Script error." Crash:** The second crash was due to issues with how the Google Translate script was being loaded and unloaded during SPA page transitions. I refactored the `custom-LanguageSwitcher` component to ensure the third-party script is loaded idempotently (only once) and is not removed from the DOM on component unmount, making the component stable across page navigations.
