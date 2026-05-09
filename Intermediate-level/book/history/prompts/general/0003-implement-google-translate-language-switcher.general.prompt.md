---
id: 0003
title: Implement Google Translate Language Switcher
stage: general
date_iso: 2025-12-25
surface: agent
model: gemini-1.5-pro
feature: none
branch: main
user: 
  command: "This is the Gemini CLI. We are setting up the context for our chat...\nMy operating system is: win32\nThe project's temporary directory is: C:\Users\M.R COMPUTERS\.gemini\tmp\963284f2fc3a23ff5dd2e2fab3a0cdddb89884f70443d74a5d438f7976bfde55\nI'm currently working in the directory: D:\Agentic-Hackthon\Physical_AI_And_Humanoid_Robotics\book\nHere is the folder structure of the current working directories:\n\nShowing up to 200 items (files + folders). Folders or files indicated with ... contain more items not shown, were ignored, or the display limit (200 items) was reached.\n\nD:\Agentic-Hackthon\Physical_AI_And_Humanoid_Robotics\book\
├───.gitignore
├───build_output.log
├───build.log
├───docusaurus.config.ts
├───npm_start.log
├───package-lock.json
├───package.json
├───README.md
├───sidebars.ts
├───tsconfig.json
├───.docusaurus\...\n├───blog\
│   ├───2019-05-28-first-blog-post.md
│   ├───2019-05-29-long-blog-post.md
│   ├───2021-08-01-mdx-blog-post.mdx
│   ├───authors.yml
│   ├───tags.yml
│   └───2021-08-26-welcome\
│       ├───docusaurus-plushie-banner.jpeg
│       └───index.md
├───build\...\n├───docs\
│   ├───author.md
│   ├───intro.md
│   ├───appendices\
│   │   ├───_category_.json
│   │   ├───glossary.md
│   │   ├───projects.md
│   │   ├───references.md
│   │   ├───setup.md
│   │   ├───glossary\
│   │   │   └───_category_.json
│   │   ├───projects\
│   │   │   └───_category_.json
│   │   ├───references\
│   │   │   └───_category_.json
│   │   └───setup\
│   │       └───_category_.json
│   ├───brain\
│   │   ├───_category_.json
│   │   └───cognitive-architectures.md
│   ├───capstone\
│   │   ├───_category_.json
│   │   └───building-a-robot.md
│   ├───foundations\
│   │   ├───_category_.json
│   │   └───core-concepts.md
│   ├───preface\
│   │   ├───_category_.json
│   │   └───introduction.md
│   ├───ros2\
│   │   ├───_category_.json
│   │   └───getting-started.md
│   ├───simulation\
│   │   ├───_category_.json
│   │   └───virtual-environments.md
│   ├───tutorial-basics\
│   │   ├───_category_.json
│   │   ├───congratulations.md
│   │   ├───create-a-blog-post.md
│   │   ├───create-a-document.md
│   │   ├───create-a-page.md
│   │   ├───deploy-your-site.md
│   │   └───markdown-features.mdx
│   ├───tutorial-extras\
│   │   ├───_category_.json
│   │   ├───manage-docs-versions.md
│   │   ├───translate-your-site.md
│   │   └───img\
│   │       ├───docsVersionDropdown.png
│   │       └───localeDropdown.png
│   └───vla\
│       ├───_category_.json
│       └───multimodal-models.md
├───history\
│   └───prompts\
│       ├───general\
│       │   └───0001-start-docusaurus-application.general.prompt.md
│       └───red\
│           └───0002-fix-urdu-translation-page-not-found-errors.red.prompt.md
├───i18n\
│   ├───en\
│   │   ├───code.json
│   │   ├───docusaurus-plugin-content-blog\
│   │   │   └───options.json
│   │   ├───docusaurus-plugin-content-docs\
│   │   │   └───current.json
│   │   └───docusaurus-theme-classic\
│   │       ├───footer.json
│   │       └───navbar.json
│   └───ur\
│       ├───code.json
│       └───docusaurus-plugin-content-docs\
│           └───current\
│               ├───author.md
│               ├───intro.md
│               ├───appendices\
│               │   ├───_category_.json
│               │   ├───glossary.md
│               │   ├───projects.md
│               │   ├───references.md
│               │   └───setup.md
│               ├───brain\
│               │   ├───_category_.json
│               │   └───cognitive-architectures.md
│               ├───capstone\
│               │   ├───_category_.json
│               │   └───building-a-robot.md
│               ├───foundations\
│               │   ├───_category_.json
│               │   └───core-concepts.md
│               ├───preface\
│               │   ├───_category_.json
│               │   └───introduction.md
│               ├───ros2\
│               │   ├───_category_.json
│               │   └───getting-started.md
│               ├───simulation\
│               │   ├───_category_.json
│               │   └───virtual-environments.md
│               ├───tutorial-basics\
│               │   ├───_category_.json
│               │   ├───congratulations.md
│               │   ├───create-a-blog-post.md
│               │   ├───create-a-document.md
│               │   ├───create-a-page.md
│               │   ├───deploy-your-site.md
│               │   └───markdown-features.mdx
│               ├───tutorial-extras\
│               │   ├───_category_.json
│               │   ├───manage-docs-versions.md
│               │   ├───translate-your-site.md
│               │   └───img\
│               │       ├───docsVersionDropdown.png
│               │       └───localeDropdown.png
│               └───vla\
│                   ├───_category_.json
│                   └───multimodal-models.md
├───node_modules\...\n├───src\
│   ├───auth\
│   │   ├───AuthContext.js
│   │   └───AuthProvider.js
│   ├───components\
│   │   ├───AuthButton\
│   │   │   ├───index.js
│   │   │   └───styles.module.css
│   │   ├───CalloutBox\
│   │   │   ├───CalloutBox.module.css
│   │   │   └───index.js
│   │   ├───Chatbot\
│   │   │   ├───Chatbot.module.css
│   │   │   └───Chatbot.tsx
│   │   ├───HeroSection\
│   │   │   ├───HeroSection.module.css
│   │   │   └───index.js
│   │   ├───HomepageFeatures\
│   │   │   ├───index.tsx
│   │   │   └───styles.module.css
│   │   └───SectionBanner\
│   │       ├───index.js
│   │       └───SectionBanner.module.css
│   ├───css\
│   │   └───custom.css
│   ├───firebase\
│   │   ├───auth.js
│   │   ├───config.js
│   │   └───index.js
│   ├───pages\
│   │   ├───forgot-password.js
│   │   ├───index.module.css
│   │   ├───index.tsx
│   │   ├───login.js
│   │   ├───markdown-page.md
│   │   ├───profile.js
│   │   ├───signup.js
│   │   └───styles.module.css
│   └───theme\
│       ├───AuthButton.js
│       ├───AuthButton.module.css
│       ├───Root.js
│       ├───Footer\
│       │   ├───index.js
│       │   └───styles.module.css
│       ├───Layout\
│       │   ├───index.tsx
│       │   ├───styles.module.css
│       │   └───Provider\
│       │       └───index.tsx
│       └───NavbarItem\
│           └───index.js
└───static\
    ├───.nojekyll
    └───img\
        ├───chap1.jpg
        ├───chap10.jpg
        ├───chap12.jpg
        ├───chap13.jpg
        ├───chap14.jpg
        ├───chap15.jpg
        ├───chap2.jpg
        ├───chap3.jpg
        ├───chap4.jpg
        ├───chap5.jpg
        ├───chap6.jpg
        ├───chap7.jpg
        ├───chap8.jpg
        ├───chap9.jpg
        ├───favicon.png
        ├───flowdiagram1.jpg
        ├───flowdiagram2.jpg
        ├───flowdiagram3.jpg
        ├───flowdiagram4.jpg
        ├───home.jpg
        └───logo.png

Reminder: Do not return an empty response when a tool call is required.

My setup is complete. I will provide my first command in the next turn.You are a senior Docusaurus + React developer.

I already have a Docusaurus documentation/book website with Firebase authentication and a chatbot on the home page.

I want to add a language switcher dropdown (English / Urdu) in the Navbar.

Requirements:

Use Google Translate (JS widget, no iframe UI)

Default language: English

Languages: English (en) and Urdu (ur)

Switching should happen on dropdown change, without page reload

Must work on all pages (Markdown book pages, home page, sidebar, navbar)

Must be lightweight, client-side only

Must NOT break Firebase auth or chatbot

Hide the default Google Translate UI

Persist selected language using localStorage

Prevent translation of code blocks

Production-safe and compatible with Docusaurus routing

Output:

Step-by-step implementation

Code for:

Google Translate script injection

Navbar dropdown component

Language change handler

localStorage persistence

CSS to hide Google UI

Keep solution simple and error-free

Do NOT suggest backend APIs, AI translation APIs, or heavy i18n libraries." 
response_text: "The language switcher feature has been successfully implemented. This involved creating a custom React component for the dropdown, integrating it into the Docusaurus navbar, and applying CSS to hide the default Google Translate UI. The solution is client-side only, uses localStorage for persistence, and is compatible with Docusaurus routing. Instructions for preventing code block translation were also provided."
files_yaml: 
  - docusaurus.config.ts
  - src/theme/NavbarItem/custom-LanguageSwitcher/index.js
  - src/css/custom.css
tests_yaml: 
  - none
outcome: Language switcher feature implemented successfully.
---
