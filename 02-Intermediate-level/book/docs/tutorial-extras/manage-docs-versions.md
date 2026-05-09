---
sidebar_position: 1
---

# Managing Documentation Versions for Robotics Projects

Versioning your robotics documentation is crucial for tracking development progress, supporting multiple robot firmware versions, and maintaining historical research records. This system enables teams to reference the correct documentation for each iteration of their humanoid robotics platform.

## Creating a Documentation Version

When releasing a new version of your robot platform (e.g., firmware 2.1, control system update), create a corresponding documentation version:

```bash
npm run docusaurus docs:version 2.1-robot-platform
```

The `docs` folder is copied into `versioned_docs/version-2.1-robot-platform` and `versions.json` is created.

Your robotics documentation now has 2 versions:

- `2.1-robot-platform` at `http://localhost:3000/docs/` for the stable 2.1 platform docs
- `current` at `http://localhost:3000/docs/next/` for the **upcoming, unreleased features and improvements**

### Versioning Strategy for Robotics Projects

Consider using semantic versioning that reflects both software and hardware changes:

```bash
# Major platform updates (new robot generation)
npm run docusaurus docs:version 3.0-humanoid-gen2

# Minor improvements (new algorithms, sensor updates)
npm run docusaurus docs:version 2.2-object-manipulation

# Patches (bug fixes, calibration updates)
npm run docusaurus docs:version 2.1.1-stability-fixes
```

## Robot Hardware and Software Version Matrix

For complex robotics projects, consider versioning that accounts for both hardware and software:

```text
v2.1.0-actuator-upgrade
├── Hardware: New servo motors with 20% more torque
├── Firmware: Updated control algorithms for new actuators
├── Software: Enhanced trajectory planning for increased payload
└── Documentation: Updated calibration procedures and safety limits
```

## Add a Robotics Version Dropdown

To navigate seamlessly across different robot platform versions, add a version dropdown to your navbar.

Modify the `docusaurus.config.js` file:

```js title="docusaurus.config.js"
export default {
  themeConfig: {
    navbar: {
      items: [
        // highlight-start
        {
          type: 'docsVersionDropdown',
          position: 'left',
          // Custom styling for robotics documentation
          dropdownItemsAfter: [
            {
              to: '/versions',
              label: 'All versions',
            },
          ],
        },
        // highlight-end
        {
          to: '/blog',
          label: 'Research Blog',
          position: 'right',
        },
      ],
    },
  },
};
```

Your version dropdown will help robotics teams quickly find documentation for their specific robot version.

## Managing Multiple Robot Platform Generations

Organize your versioned documentation for different robot generations:

```
versioned_docs/
├── version-humanoid-gen1/     # Documentation for first generation humanoid
│   ├── hardware/
│   ├── software/
│   └── tutorials/
├── version-humanoid-gen2/     # Documentation for second generation
│   ├── advanced-perception/
│   ├── vla-systems/
│   └── cognitive-architectures/
└── version-legacy-platform/   # Older platform documentation
```

## Update Existing Robot Platform Documentation

You can update versioned docs for each robot platform in their respective folders:

- `versioned_docs/version-2.1-robot-platform/locomotion.md` updates the locomotion algorithms for 2.1 platform
- `docs/locomotion.md` updates the upcoming version with the latest improvements
- `versioned_docs/version-humanoid-gen2/perception.md` updates perception systems for second generation robots

### Example: Updating Control System Documentation

When you implement a new control algorithm:

```bash
# First, update the current (upcoming) documentation
# Edit docs/control-systems/new-adaptive-controller.md

# After releasing the feature in a new robot firmware version:
npm run docusaurus docs:version 2.3-adaptive-control

# Later, if you need to fix documentation for the older version:
# Edit versioned_docs/version-2.2-previous-control/perception.md
```

## Versioning Best Practices for Robotics Teams

### 1. Synchronize with Hardware Releases
```bash
# When releasing new hardware
git tag robot-hardware-v2.0
npm run docusaurus docs:version v2.0-hardware-release

# When releasing new software for existing hardware
npm run docusaurus docs:version v2.1-software-update
```

### 2. Feature Documentation Timeline
```
Documentation Timeline:
v1.0 (Initial platform) ──→ v1.1 (Improved perception) ──→ v2.0 (New hardware)
         ↓                           ↓                              ↓
   Core capabilities        Enhanced sensing              Physical redesign
```

### 3. Deprecation Strategy
When retiring features in robot platforms, mark them clearly in documentation:

```md
:::caution Deprecated in v2.0 Platform

The `legacy_gait_controller` has been replaced by `adaptive_locomotion_system` in v2.0+ platforms.
Older robots running v1.x firmware can still use this controller.

For new implementations, use the [Adaptive Locomotion System](/docs/next/adaptive-locomotion).
:::
```

## Continuous Integration for Versioned Robotics Docs

Set up your CI/CD pipeline to handle versioned documentation:

```yaml title=".github/workflows/deploy-versions.yml"
name: Deploy Documentation Versions

on:
  push:
    tags:
      - 'v*'  # Trigger on version tags
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # All history for versioning

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install dependencies
        run: npm ci

      - name: Create version if tagged
        run: |
          if [[ $GITHUB_REF == refs/tags/* ]]; then
            VERSION=${GITHUB_REF#refs/tags/}
            npm run docusaurus docs:version $VERSION
          fi

      - name: Build and deploy
        run: npm run build
```

The documentation versioning system ensures that your robotics teams always have access to the correct information for their specific robot platform version, preventing costly errors from using outdated specifications or procedures.

:::tip

For robotics projects, align documentation versions with robot firmware releases and maintain at least 2-3 versions to support different robot units operating in the field.

:::
