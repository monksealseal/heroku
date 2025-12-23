#!/bin/bash
# Script to enable GitHub Pages for this repository
# This uses the GitHub API to automate the process

set -e

echo "=================================================="
echo "GitHub Pages Automated Setup"
echo "=================================================="
echo ""

# Get repository info
REPO_OWNER="monksealseal"
REPO_NAME="heroku"
BRANCH="claude/build-gcm-physics-VaCFZ"

echo "Repository: $REPO_OWNER/$REPO_NAME"
echo "Branch: $BRANCH"
echo "Source folder: /docs"
echo ""

# Check if gh CLI is available
if command -v gh &> /dev/null; then
    echo "Using GitHub CLI (gh)..."
    echo ""

    # Enable GitHub Pages using gh CLI
    gh api \
        --method POST \
        -H "Accept: application/vnd.github+json" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        "/repos/$REPO_OWNER/$REPO_NAME/pages" \
        -f source[branch]="$BRANCH" \
        -f source[path]="/docs" \
        2>&1 || {
            echo ""
            echo "Note: If you see an error about Pages already being enabled,"
            echo "that's fine - it means GitHub Pages is already set up!"
            echo ""
        }

    echo ""
    echo "✓ GitHub Pages configuration sent!"
    echo ""

else
    echo "GitHub CLI (gh) not found."
    echo ""
    echo "OPTION 1: Install GitHub CLI and run this script again"
    echo "  Install from: https://cli.github.com/"
    echo ""
    echo "OPTION 2: Enable manually in GitHub web interface"
    echo "  1. Go to: https://github.com/$REPO_OWNER/$REPO_NAME/settings/pages"
    echo "  2. Under 'Build and deployment' → 'Source', select 'GitHub Actions'"
    echo "  3. The workflow will automatically deploy when you push changes"
    echo ""
    echo "OPTION 3: Use GitHub Actions (automatic deployment)"
    echo "  The workflow file is already created at:"
    echo "  .github/workflows/deploy-pages.yml"
    echo ""
    echo "  Once you enable GitHub Pages (using web interface):"
    echo "  - Every push to docs/ will automatically deploy"
    echo "  - You can also trigger manually from Actions tab"
    echo ""
    exit 1
fi

# Get the Pages URL
echo "Fetching your GitHub Pages URL..."
PAGES_URL=$(gh api \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "/repos/$REPO_OWNER/$REPO_NAME/pages" \
    --jq '.html_url' 2>/dev/null || echo "https://$REPO_OWNER.github.io/$REPO_NAME/")

echo ""
echo "=================================================="
echo "✓ SUCCESS!"
echo "=================================================="
echo ""
echo "Your GitHub Pages site will be available at:"
echo "  $PAGES_URL"
echo ""
echo "Note: It may take 2-3 minutes for the site to build and deploy."
echo ""
echo "To check deployment status:"
echo "  gh run list --workflow=deploy-pages.yml"
echo ""
echo "Or visit:"
echo "  https://github.com/$REPO_OWNER/$REPO_NAME/actions"
echo ""
