---
sidebar_position: 2
---

# Internationalizing Robotics Documentation

Internationalization (i18n) is essential for robotics projects that span global research teams, manufacturing sites, and end-user locations. This guide shows how to translate your Physical AI and Humanoid Robotics documentation for international collaboration.

## Configure i18n for Robotics Teams

Modify `docusaurus.config.js` to add support for multiple locales relevant to your robotics project:

```js title="docusaurus.config.js"
export default {
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ja', 'de', 'zh', 'fr'],  // English, Japanese, German, Chinese, French
    localeConfigs: {
      en: {
        label: 'English',
        direction: 'ltr',
      },
      ja: {
        label: '日本語',
        direction: 'ltr',
      },
      de: {
        label: 'Deutsch',
        direction: 'ltr',
      },
      zh: {
        label: '中文',
        direction: 'ltr',
      },
      fr: {
        label: 'Français',
        direction: 'ltr',
      },
    },
  },
};
```

## Translate Robotics Documentation

The technical nature of robotics documentation requires special attention during translation:

### Technical Terminology
Copy and translate `docs/intro.md` to the French locale:

```bash
mkdir -p i18n/fr/docusaurus-plugin-content-docs/current/

cp docs/intro.md i18n/fr/docusaurus-plugin-content-docs/current/intro.md
```

When translating robotics content, maintain consistency in technical terms:

```md title="i18n/fr/docusaurus-plugin-content-docs/current/intro.md" (example excerpt)
---
sidebar_position: 1
---

# Guide Complet sur l'IA Physique et la Robotique Humanoides

Bienvenue dans le guide définitif sur l'IA Physique et la Robotique Humanoides - un domaine multidisciplinaire combinant l'intelligence artificielle, l'ingénierie mécanique, la vision par ordinateur et les sciences cognitives pour créer des systèmes intelligents incarnés.

## À propos de ce livre

Cette ressource complète explore l'intersection de pointe entre l'intelligence artificielle et la robotique physique, en se concentrant spécifiquement sur les robots humanoïdes et leurs applications...
```

### Maintaining Code Examples
Keep code examples in English as they are language-neutral:

```md
# Exemple de code de contrôle PID - garder en anglais
```python
class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp  # Toujours en anglais car ce sont des variables de code
        self.ki = ki
        self.kd = kd
```
```

## Translate Specialized Robotics Content

### Mathematical Equations
Mathematical notations remain the same across languages:

```md
## Équation de Cinématique Directe

La position de l'organe terminal est calculée en utilisant:

$$ \mathbf{T} = \prod_{i=1}^{n} \mathbf{A}_i(\theta_i) $$

Où:
- $\mathbf{T}$ est la matrice de transformation
- $\mathbf{A}_i(\theta_i)$ est la matrice de transformation du lien pour la jointure $i$
- $\theta_i$ est l'angle de la jointure $i$
```

### Diagrams and Images
Images and diagrams typically remain the same, with translation applied to captions:

```md
![Configuration du bras robotique](/img/chap3.jpg)

*Figure: Configuration typique d'un bras manipulateur à 6 degrés de liberté avec étiquetage des jointures*
```

## Start Your Localized Robotics Site

Start your site on the Japanese locale for testing:

```bash
npm run start -- --locale ja
```

Your localized robotics documentation is accessible at [http://localhost:3000/ja/](http://localhost:3000/ja/) and the technical content is now available in Japanese.

### Robotics-Specific Translation Considerations

:::caution

Robotics terminology should be consistent across languages. Maintain a glossary of terms to ensure uniformity across all translations.

:::

**Example Glossary for Robotics Terms:**
- English: manipulator, controller, actuator, sensor fusion
- Japanese: マニピュレータ (manipyureta), コントローラ (kontorōra), アクチュエータ (akuchueeta), センサーフュージョン (senā fyūjon)
- German: Manipulator, Regler, Stellantrieb, Sensorfusion

## Add a Locale Dropdown for Robotics Teams

To facilitate seamless navigation across languages for international robotics teams, add a locale dropdown.

Modify the `docusaurus.config.js` file:

```js title="docusaurus.config.js"
export default {
  themeConfig: {
    navbar: {
      items: [
        // highlight-start
        {
          type: 'localeDropdown',
          position: 'right',
          dropdownItemsAfter: [
            {
              to: '/languages',
              label: 'All languages',
            },
          ],
        },
        // highlight-end
        {
          type: 'docsVersionDropdown',
          position: 'left',
        },
      ],
    },
  },
};
```

The locale dropdown now appears in your navbar, enabling international robotics teams to access documentation in their preferred language.

## Translation Workflow for Large Robotics Projects

### Collaborative Translation
For large robotics documentation projects with multiple contributors:

```bash
# Set up translation teams
mkdir -p i18n/ja/docusaurus-plugin-content-docs/current/
mkdir -p i18n/de/docusaurus-plugin-content-docs/current/
mkdir -p i18n/zh/docusaurus-plugin-content-docs/current/

# Create translation templates
cp docs/intro.md i18n/ja/docusaurus-plugin-content-docs/current/intro.md
cp docs/intro.md i18n/de/docusaurus-plugin-content-docs/current/intro.md
cp docs/intro.md i18n/zh/docusaurus-plugin-content-docs/current/intro.md
```

### Translation Review Process
Implement a review process for technical accuracy:

```
Translation Workflow:
Original English → Translation → Technical Review → Proofreading → Publication
```

## Build Your Localized Robotics Documentation

Build your site for a specific locale:

```bash
npm run build -- --locale de
```

Or build your site to include all the locales at once:

```bash
npm run build
```

## Additional i18n Configuration for Technical Documentation

### Search Localization
Configure search to work across languages:

```js title="docusaurus.config.js"
module.exports = {
  themes: [
    [
      '@docusaurus/theme-classic',
      {
        customCss: require.resolve('./src/css/custom.css'),
      },
    ],
    [
      '@docusaurus/theme-search-algolia',
      {
        // Support for multiple languages in search
        contextualSearch: true,
        searchParameters: {
          // Configure search to understand technical terminology
        },
      },
    ],
  ],
};
```

### Sitemap for International Documentation
Generate sitemaps for each locale:

```js title="docusaurus.config.js"
module.exports = {
  plugins: [
    [
      '@docusaurus/plugin-sitemap',
      {
        filename: 'sitemap.xml',
        lastmod: 'date',
        changefreq: 'weekly',
        priority: 0.5,
        onRouteMeta(route) {
          // Customize sitemap for each locale
          return {
            alternateRefs: route.anchors
              .filter((anchor) => anchor.id.startsWith('lang-'))
              .map((anchor) => ({
                href: anchor.id.replace('lang-', ''),
                hreflang: anchor.id.split('-')[1],
              })),
          };
        },
      },
    ],
  ],
};
```

Internationalizing your robotics documentation enables global collaboration, supports international manufacturing and deployment teams, and facilitates worldwide research partnerships in the field of Physical AI and Humanoid Robotics.
