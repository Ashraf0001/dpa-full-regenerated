# Deployment Guide

This guide explains how to set up automatic deployment of the DPA documentation site using GitHub Actions.

## Overview

The project includes several CI/CD workflows that automatically:

1. **Test** the codebase on multiple Python versions
2. **Build** release binaries and Python packages
3. **Deploy** documentation to GitHub Pages
4. **Notify** about deployment status

## Workflows

### 1. Main CI/CD Pipeline (`ci.yml`)

**Triggers:**
- Push to `feature-testing`, `main`, or `develop` branches
- Pull requests to these branches

**Jobs:**
- **Test**: Runs tests on Python 3.9, 3.10, 3.11
- **Build**: Creates release binaries and packages
- **Docs**: Builds and deploys documentation
- **Notify**: Reports deployment status

### 2. Documentation Only (`docs-simple.yml`)

**Purpose:** Lightweight documentation deployment
**Triggers:** Same as main pipeline
**Features:** GitHub Pages deployment only

## Setup Instructions

### 1. Enable GitHub Pages

1. Go to your repository settings
2. Navigate to **Pages** section
3. Set **Source** to "GitHub Actions"
4. Save the settings

### 2. Configure Repository Secrets (Optional)

For advanced features, add these secrets:

```bash
# For Netlify deployment (alternative)
NETLIFY_AUTH_TOKEN=your_netlify_token
NETLIFY_SITE_ID=your_site_id

# For notifications (if using Slack/Discord)
SLACK_WEBHOOK_URL=your_slack_webhook
DISCORD_WEBHOOK_URL=your_discord_webhook
```

### 3. Branch Protection (Recommended)

Set up branch protection for `main` and `feature-testing`:

1. Go to **Settings** → **Branches**
2. Add rule for `main` and `feature-testing`
3. Enable:
   - Require status checks to pass
   - Require branches to be up to date
   - Include administrators

## Deployment Process

### Automatic Deployment

When you push to `feature-testing` or `main`:

1. **GitHub Actions** automatically triggers
2. **Tests** run on multiple Python versions
3. **Documentation** builds with MkDocs
4. **Site** deploys to GitHub Pages
5. **URL** becomes available at: `https://ashraf0001.github.io/dpa-full-regenerated/`

### Manual Deployment

To deploy manually:

```bash
# Build documentation locally
mkdocs build

# Deploy to GitHub Pages (if you have gh-pages branch)
mkdocs gh-deploy
```

## URLs and Access

### GitHub Pages
- **Production**: `https://ashraf0001.github.io/dpa-full-regenerated/`
- **Branch-specific**: `https://ashraf0001.github.io/dpa-full-regenerated/feature-testing/`

### Netlify (Alternative)
- **Production**: `https://your-site-name.netlify.app`
- **Preview**: `https://deploy-preview-123--your-site-name.netlify.app`

## Monitoring

### GitHub Actions Dashboard
- View workflow runs: `https://github.com/Ashraf0001/dpa-full-regenerated/actions`
- Check deployment status
- Download build artifacts

### Deployment Status
- **Green**: All tests passed, deployment successful
- **Yellow**: Tests passed, deployment in progress
- **Red**: Tests failed, deployment blocked

## Troubleshooting

### Common Issues

1. **Build Fails**
   ```bash
   # Check local build
   mkdocs build --strict
   ```

2. **Dependencies Missing**
   ```bash
   # Install locally
   pip install -r requirements-docs.txt
   ```

3. **Permission Errors**
   - Ensure GitHub Pages is enabled
   - Check repository permissions
   - Verify workflow permissions

### Debug Commands

```bash
# Test documentation build locally
mkdocs build --verbose

# Check MkDocs configuration
mkdocs config

# Validate site structure
mkdocs build --strict --clean
```

## Customization

### Adding New Dependencies

1. Update `requirements-docs.txt`
2. Update workflow files
3. Test locally before pushing

### Modifying Deployment

1. Edit `.github/workflows/ci.yml`
2. Test with feature branch
3. Merge to main when ready

### Environment Variables

Add to repository secrets:
```bash
MKDOCS_ENABLE_INSIDER=true
MKDOCS_EXTRA_CSS=custom.css
MKDOCS_EXTRA_JS=custom.js
```

## Best Practices

1. **Always test locally** before pushing
2. **Use feature branches** for development
3. **Monitor deployment logs** for issues
4. **Keep dependencies updated**
5. **Document changes** in commit messages

## Support

For issues with deployment:

1. Check GitHub Actions logs
2. Verify repository settings
3. Test locally with same environment
4. Create issue with detailed error logs

---

**Happy Deploying!** 🚀
