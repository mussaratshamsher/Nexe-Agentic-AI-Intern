---
ID: 0002
TITLE: Fix Urdu Translation Page Not Found Errors
STAGE: red
DATE_ISO: 2025-12-25
SURFACE: agent
MODEL: gemini-experimental
FEATURE: i18n
BRANCH: main
USER: User
COMMAND: mv and Remove-Item commands
LABELS: ["i18n", "bugfix", "docusaurus", "file-structure"]
LINKS: null
FILES_YAML:
 - i18n/ur/docusaurus-plugin-content-docs/current/appendices/references/references.md (moved)
 - i18n/ur/docusaurus-plugin-content-docs/current/appendices/glossary/glossary.md (moved)
 - i18n/ur/docusaurus-plugin-content-docs/current/appendices/projects/projects.md (moved)
 - i18n/ur/docusaurus-plugin-content-docs/current/appendices/setup/setup.md (moved)
 - i18n/ur/docusaurus-plugin-content-docs/current/appendices/references/ (removed)
 - i18n/ur/docusaurus-plugin-content-docs/current/appendices/glossary/ (removed)
 - i18n/ur/docusaurus-plugin-content-docs/current/appendices/projects/ (removed)
 - i18n/ur/docusaurus-plugin-content-docs/current/appendices/setup/ (removed)
TESTS_YAML:
---

## PROMPT_TEXT

```
still all urdu translation is not visible and showing error of page not found: Page Not Found              │
│   We could not find what you were looking for.                                                               │
│                                                                                                              │
│   Please contact the owner of the site that linked you to the original URL and let them know their link is   │
│   broken.  what the issue is?? why are you not adding each page translation properly -- i got fadup now again and again error
```

## RESPONSE_TEXT

```
Investigated the "Page Not Found" errors for Urdu translations. Identified that some markdown files were incorrectly nested within subdirectories (e.g., glossary.md was in appendices/glossary/ instead of appendices/). Moved these files to their correct locations and removed the now empty (or _category_.json-only) directories. This should resolve the page not found errors for the affected translated pages.
```