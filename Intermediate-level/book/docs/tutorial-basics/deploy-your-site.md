---
sidebar_position: 5
---

# Deploying Your Robotics Documentation Site

Deploying your robotics documentation site ensures that research findings, technical specifications, and implementation guides are accessible to your team, collaborators, and the broader robotics community.

Docusaurus is a **static-site-generator** (also called **[Jamstack](https://jamstack.org/)**).

It builds your site as simple **static HTML, JavaScript and CSS files** that can be served efficiently.

## Build your site for Robotics Documentation

Build your site **for production** with your robotics documentation:

```bash
npm run build
```

The static files are generated in the `build` folder, containing all your robotics documentation, code examples, and technical illustrations.

### Optimizing for Robotics Content

For robotics documentation sites with mathematical equations and heavy code examples, consider additional build optimizations:

```bash
# Build with extra optimizations
npm run build -- --bundle-analyzer

# Or build with a specific base URL for deployment
BASEROUTER=/robotics-book npm run build
```

## Deploy your Robotics Documentation Site

Test your production build locally to ensure all robotics content renders correctly:

```bash
npm run serve
```

The `build` folder is now served at [http://localhost:3000/](http://localhost:3000/).

### Deployment Platforms for Robotics Projects

You can deploy your robotics documentation to these platforms:

#### GitHub Pages (Recommended for Open Source)

For open robotics research projects, GitHub Pages provides free hosting:

```bash
# Install the GitHub deployment package
npm install --save-dev gh-pages

# Add to your package.json:
# "scripts": {
#   "deploy": "docusaurus deploy"
# }

# Create a GitHub personal access token and set:
# GIT_USER=<your-github-username> npm run deploy
```

#### Cloud Platforms

For private robotics projects, consider these options:

```bash
# AWS S3 deployment
aws s3 sync build/ s3://your-robotics-docs-bucket --delete

# Google Cloud Storage
gsutil rsync -r build gs://your-robotics-docs-bucket

# Azure Static Web Apps
az storage blob upload-batch -d '$web' -s build --account-name myroboticsdocs
```

### Continuous Integration for Robotics Documentation

Set up CI/CD to automatically deploy updates to your robotics documentation:

```yaml title=".github/workflows/deploy.yml"
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    name: Deploy to GitHub Pages
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: npm

      - name: Install dependencies
        run: npm ci
      - name: Build website
        run: npm run build

      # Popular action to deploy to GitHub Pages:
      # Docs: https://github.com/peaceiris/actions-gh-pages#%EF%B8%8F-docusaurus
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
```

### Special Considerations for Robotics Content

#### MathJax and LaTeX Rendering

Ensure mathematical equations render correctly in your deployed site by verifying the build process includes proper KaTeX or MathJax configuration:

```js title="docusaurus.config.js"
module.exports = {
  // ... other config
  markdown: {
    mermaid: true,
  },
  themes: [
    '@docusaurus/theme-classic',
    '@docusaurus/theme-mermaid',
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'robotics-math',
        path: 'docs',
        routeBasePath: 'docs',
        showLastUpdateAuthor: true,
        showLastUpdateTime: true,
        // Enable LaTeX math in docs
        remarkPlugins: [require('remark-math')],
        rehypePlugins: [require('rehype-katex')],
      },
    ],
  ],
  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.13.24/dist/katex.min.css',
      type: 'text/css',
      integrity:
        'sha384-odtC+0UGzzFL/6PNoE8rX/SPcQDXBJ+uRepguP4QkPCm2LBxH3FAj542USm++tO',
      crossorigin: 'anonymous',
    },
  ],
};
```

#### Large Media Files

If your robotics documentation includes large simulation videos, 3D models, or datasets:

- Consider hosting large files separately (GitHub LFS, AWS S3)
- Use efficient image formats (WebP for photos, SVG for diagrams)
- Compress files before adding to the repository

### Testing Robotics-Specific Features

Before deployment, verify all robotics-specific features work:

```bash
# Test locally with production build
npm run serve

# Verify that:
# - All mathematical equations render correctly
# - Code syntax highlighting works for robotics languages (Python, C++, etc.)
# - Diagrams and images display properly
# - Navigation works across all robotics documentation sections
# - Search functionality finds robotics terminology
```

### Deployment Verification Checklist

For robotics documentation sites, ensure:

- [ ] All mathematical formulas render correctly
- [ ] Code examples are properly syntax-highlighted
- [ ] Technical diagrams and images are accessible
- [ ] Cross-references between robotics concepts work
- [ ] Search functionality finds domain-specific terminology
- [ ] MathJax/LaTeX equations display properly
- [ ] Interactive elements (if any) function correctly
- [ ] Mobile viewing works for field robotics teams

## Version Control for Robotics Documentation

Consider setting up versioning for your robotics research and development:

```bash
# Tag the current version of your documentation
git tag docs-v1.0.0

# Push tags to track documentation versions
git push origin docs-v1.0.0
```

You can now deploy the `build` folder containing your robotics documentation **almost anywhere** easily, **for free** or very small cost (read the **[Deployment Guide](https://docusaurus.io/docs/deployment)**).