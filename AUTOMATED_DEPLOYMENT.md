# Automated GitHub Pages Deployment

This repository now has **automated GitHub Pages deployment** configured!

## How It Works

A GitHub Actions workflow (`.github/workflows/deploy-pages.yml`) automatically deploys the `docs/` folder to GitHub Pages whenever you push changes.

---

## Quick Start (3 Methods)

### Method 1: Automated Script ⚡ (Recommended)

Run the automated setup script:

```bash
./enable_github_pages.sh
```

This will use the GitHub CLI to enable Pages automatically.

**Prerequisites:**
- GitHub CLI installed: `brew install gh` (Mac) or see https://cli.github.com/
- Logged in: `gh auth login`

---

### Method 2: GitHub Web Interface 🌐 (Easiest)

1. Go to your repository on GitHub.com
2. Click **Settings** → **Pages** (in left sidebar)
3. Under **Build and deployment**:
   - **Source**: Select **GitHub Actions**
4. Click **Save**

**That's it!** The workflow will automatically deploy when you push changes to `docs/`.

---

### Method 3: GitHub CLI Commands 💻

If you prefer command-line:

```bash
# Enable GitHub Pages with GitHub Actions source
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  "/repos/monksealseal/heroku/pages" \
  -f source[branch]="claude/build-gcm-physics-VaCFZ" \
  -f source[path]="/docs"

# Check status
gh api /repos/monksealseal/heroku/pages
```

---

## After Enabling Pages

### Your Site URL

Your GitHub Pages site will be available at:
```
https://monksealseal.github.io/heroku/
```

### Automatic Deployment

Every time you push changes to the `docs/` folder:

1. GitHub Actions automatically triggers
2. Builds and deploys your site
3. Site updates in 2-3 minutes

### Manual Deployment

You can also trigger deployment manually:

1. Go to **Actions** tab on GitHub
2. Select **Deploy to GitHub Pages** workflow
3. Click **Run workflow**

---

## Monitoring Deployments

### View Deployment Status

**Via GitHub CLI:**
```bash
# List recent workflow runs
gh run list --workflow=deploy-pages.yml

# Watch specific run
gh run watch

# View logs
gh run view --log
```

**Via Web Interface:**
```
https://github.com/monksealseal/heroku/actions
```

### Deployment Takes ~2-3 Minutes

Typical timeline:
- **0:00** - Push to repository
- **0:05** - GitHub Actions starts
- **0:30** - Build completes
- **2:00** - Site deployed and live

---

## Workflow Features

✅ **Automatic Triggers:**
- Pushes to `claude/build-gcm-physics-VaCFZ` branch
- Changes to `docs/**` files only

✅ **Manual Triggers:**
- Run from GitHub Actions tab
- `workflow_dispatch` enabled

✅ **Security:**
- Minimal permissions (read content, write pages)
- Concurrent deployment protection
- ID token for authentication

✅ **Optimized:**
- Only deploys when docs/ changes
- Cancels duplicate deployments
- Artifact caching

---

## Updating Your Site

### Edit Documentation

1. Edit files in `docs/` folder:
   ```bash
   # Example: Update landing page
   nano docs/index.html
   ```

2. Commit and push:
   ```bash
   git add docs/
   git commit -m "Update documentation"
   git push origin claude/build-gcm-physics-VaCFZ
   ```

3. GitHub Actions automatically deploys!

### Check Deployment

```bash
# See latest run status
gh run list --workflow=deploy-pages.yml --limit 1

# Or visit
https://github.com/monksealseal/heroku/actions
```

---

## Troubleshooting

### Pages Not Enabled Yet?

If you see "404 Not Found" when visiting your site:

1. **Enable Pages first** (see Method 2 above)
2. Wait 2-3 minutes for initial deployment
3. Check Actions tab for workflow status

### Workflow Not Running?

Check these:

1. **Pages source is set to "GitHub Actions"** (not "Deploy from branch")
2. **Workflow file exists**: `.github/workflows/deploy-pages.yml`
3. **Branch name is correct** in workflow file
4. **Permissions are enabled**: Settings → Actions → General → Workflow permissions

### Deployment Failed?

View error logs:

```bash
# CLI
gh run view --log

# Web
https://github.com/monksealseal/heroku/actions
```

Common fixes:
- Check Pages is enabled in repository settings
- Verify docs/ folder exists and has index.html
- Ensure workflow has proper permissions

---

## Advanced Configuration

### Change Deployment Branch

Edit `.github/workflows/deploy-pages.yml`:

```yaml
on:
  push:
    branches:
      - main  # Change to your preferred branch
```

### Add Custom Domain

1. Add `CNAME` file to `docs/`:
   ```bash
   echo "gcm.yourdomain.com" > docs/CNAME
   git add docs/CNAME
   git commit -m "Add custom domain"
   git push
   ```

2. Configure DNS:
   - Add CNAME record: `gcm` → `monksealseal.github.io`

3. Enable in GitHub Settings → Pages → Custom domain

### Deploy from Different Folder

Edit workflow file, change `path`:

```yaml
- name: Upload artifact
  uses: actions/upload-pages-artifact@v3
  with:
    path: './public'  # Change from './docs'
```

---

## Benefits of This Setup

✅ **Fully Automated** - Push and forget
✅ **Fast** - Deploys in ~2 minutes
✅ **Free** - No hosting costs
✅ **Reliable** - GitHub's infrastructure
✅ **Versioned** - Git tracks all changes
✅ **Secure** - Minimal permissions, audited
✅ **Scalable** - Handles high traffic
✅ **Professional** - Custom domains, HTTPS

---

## What's Deployed?

The `docs/` folder contains:

```
docs/
├── index.html          # Landing page
├── style.css           # Styling
├── script.js           # JavaScript
├── _config.yml         # Jekyll config
├── CNAME               # Custom domain (optional)
└── screenshot-placeholder.svg
```

All these files are automatically deployed to:
```
https://monksealseal.github.io/heroku/
```

---

## Next Steps

1. **Enable Pages** using Method 1 or 2 above
2. **Visit your site** at https://monksealseal.github.io/heroku/
3. **Update content** by editing files in docs/
4. **Push changes** - deployment happens automatically!

---

## Support

- **GitHub Pages Docs**: https://docs.github.com/pages
- **GitHub Actions Docs**: https://docs.github.com/actions
- **Workflow File**: `.github/workflows/deploy-pages.yml`
- **Setup Script**: `enable_github_pages.sh`

---

## Summary

You now have professional, automated deployment:

1. **Edit** files in `docs/`
2. **Commit and push** to repository
3. **Automatic deployment** via GitHub Actions
4. **Live site** updates in 2-3 minutes

No manual steps needed after initial setup! 🎉
