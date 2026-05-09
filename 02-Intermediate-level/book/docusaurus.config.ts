import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline:
    'A comprehensive guide to the principles, technologies, and practices of building intelligent humanoid robots.',
  favicon: 'img/favicon.png',

  // ✅ Vercel-safe (no deployment required yet)
  url: 'https://example.com',
  baseUrl: '/',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      en: {
        label: 'English',
        htmlLang: 'en-US',
      },
      ur: {
        label: 'اردو',
        direction: 'rtl',
        htmlLang: 'ur-PK',
      },
    },
  },

  scripts: [
    {
      src: 'https://www.gstatic.com/firebasejs/10.15.0/firebase-app-compat.js',
      async: true,
    },
    {
      src: 'https://www.gstatic.com/firebasejs/10.15.0/firebase-auth-compat.js',
      async: true,
    },
    // Additional script to handle potential DOM issues
    {
      src: '/js/global-script.js',
      async: true,
    }
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',

    colorMode: {
      respectPrefersColorScheme: true,
    },

    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Physical AI Book Logo',
        src: 'img/logo.png',
      },
      items: [
        { to: '/', label: 'Home', position: 'left' },
        { to: '/docs/intro', label: 'Chapters', position: 'left' },
        {
          to: '/docs/appendices/glossary',
          label: 'Glossary',
          position: 'left',
        },
        {
          to: '/docs/appendices/references',
          label: 'Resources',
          position: 'left',
        },
                  {
                    type: 'custom-LanguageSwitcher',
                    position: 'right',
                  },
                  {
                    type: 'custom-AuthButton',
                    position: 'right',
                  },      ],
    },

    footer: {
      style: 'dark',
      links: [
        {
          title: 'Social',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/mussaratshamsher',
            },
            {
              label: 'Twitter',
              href: 'https://twitter.com/Physical_AI',
            },
            {
              label: 'LinkedIn',
              href: 'https://www.linkedin.com/in/mussarat-shamsher-7618a6380/',
            },
          ],
        },
      ],
      copyright:
        'Copyright © 2025 Physical AI Press. All rights reserved.',
    },

    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/mussaratshamsher/Physical_AI_And_Humanoid_Robotics/tree/main/book/',
          remarkPlugins: [require('remark-math')],
          rehypePlugins: [require('rehype-katex')],
        },

        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          editUrl:
            'https://github.com/mussaratshamsher/Physical_AI_And_Humanoid_Robotics/tree/main/book/',
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },

        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.css',
      type: 'text/css',
      crossorigin: 'anonymous',
    },
  ],
};

export default config;
