# GitHub Pages Setup Guide

## What Is GitHub Pages?

GitHub Pages hosts **static websites** (HTML/CSS/JavaScript) directly from your GitHub repository for FREE!

## Important Note About GCM

⚠️ **GitHub Pages Limitation**: GitHub Pages can only host static content. It **cannot run Python code** or execute GCM simulations.

### Solution:
- **GitHub Pages**: Beautiful documentation and project showcase
- **Heroku** (or similar): Actual running application with simulations

Both can work together perfectly!

---

## Quick Setup (Enable GitHub Pages)

### Step 1: Push to GitHub

```bash
# Add GitHub remote (if not already added)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push all branches
git push -u origin --all
```

### Step 2: Enable GitHub Pages

1. Go to your repo on GitHub
2. Click **Settings**
3. Scroll to **Pages** (left sidebar)
4. Under **Source**, select:
   - Branch: `claude/build-gcm-physics-VaCFZ`
   - Folder: `/docs`
5. Click **Save**

### Step 3: Wait (2-3 minutes)

GitHub Pages will build your site automatically.

### Step 4: Visit Your Site!

Your site will be available at:
```
https://YOUR_USERNAME.github.io/YOUR_REPO/
```

---

## What You Get on GitHub Pages

✅ **Beautiful Landing Page** - Professional showcase
✅ **Project Documentation** - User guides and technical docs
✅ **Links to Live App** - Direct links to Heroku deployment
✅ **SEO Friendly** - Google can find and index it
✅ **Free Hosting** - No cost, unlimited bandwidth
✅ **Custom Domain** - Can use your own domain

---

## Customize Before Publishing

### Update Links

Edit `docs/index.html` and `docs/script.js`:

1. **Replace GitHub URL**:
   ```javascript
   // In script.js, line ~40
   link.href = 'https://github.com/YOUR_USERNAME/YOUR_REPO';
   ```

2. **Replace Heroku URL** (after deploying to Heroku):
   ```html
   <!-- In index.html -->
   href="https://your-actual-app.herokuapp.com"
   ```

### Add Custom Domain (Optional)

1. Edit `docs/CNAME`:
   ```
   gcm.yourdomain.com
   ```

2. Configure DNS:
   - Add CNAME record: `gcm` → `YOUR_USERNAME.github.io`

3. Enable in GitHub Settings → Pages → Custom domain

---

## Complete Deployment Strategy

### Best Practice: Use Both!

**GitHub Pages** (Documentation & Showcase):
```
https://username.github.io/repo/
├── Landing page
├── Documentation
├── User guides
├── Physics documentation
└── Links to live app
```

**Heroku** (Live Application):
```
https://your-app.herokuapp.com/
├── Interactive simulations
├── Real-time processing
├── Python backend
└── GCM execution
```

---

## Deployment Checklist

### GitHub Pages:
- [ ] Push code to GitHub
- [ ] Enable Pages in Settings
- [ ] Select `/docs` folder
- [ ] Update URLs in index.html
- [ ] Wait for build (2-3 min)
- [ ] Visit site and verify

### Heroku:
- [ ] Install Heroku CLI
- [ ] Run `heroku create`
- [ ] Push to Heroku
- [ ] Update GitHub Pages links
- [ ] Test simulation

---

## Folder Structure

```
your-repo/
├── docs/                    # GitHub Pages files
│   ├── index.html          # Main landing page
│   ├── style.css           # Styles
│   ├── script.js           # JavaScript
│   ├── _config.yml         # Jekyll config
│   └── CNAME               # Custom domain (optional)
│
├── gcm/                     # GCM package (not on GitHub Pages)
├── templates/               # Flask templates (not on GitHub Pages)
├── static/                  # Flask static files (not on GitHub Pages)
├── app.py                   # Flask app (not on GitHub Pages)
├── Procfile                 # Heroku config
└── requirements.txt         # Python dependencies
```

GitHub Pages only serves files from `docs/` folder.
Everything else is for Heroku deployment.

---

## Update GitHub Pages Content

To update your site:

```bash
# Edit files in docs/
# Then commit and push

git add docs/
git commit -m "Update GitHub Pages"
git push origin claude/build-gcm-physics-VaCFZ

# GitHub Pages auto-rebuilds (2-3 min)
```

---

## Add More Pages

Create additional HTML files in `docs/`:

```bash
docs/
├── index.html           # Home
├── user-guide.html      # User guide
├── physics.html         # Physics docs
├── deployment.html      # Deployment guide
├── architecture.html    # Architecture
└── api.html            # API reference
```

Link between pages:
```html
<a href="user-guide.html">User Guide</a>
```

---

## Troubleshooting

### Page Not Loading
- Wait 2-3 minutes after enabling
- Check Settings → Pages for errors
- Ensure `/docs` folder is selected
- Verify branch name is correct

### 404 Not Found
- Check file names (case sensitive)
- Ensure files are in `docs/` folder
- Verify GitHub Pages is enabled

### Links Broken
- Use relative paths: `user-guide.html` not `/user-guide.html`
- Update URLs after deployment
- Check console for errors

### Custom Domain Not Working
- Wait for DNS propagation (up to 24 hours)
- Verify CNAME record in DNS
- Check CNAME file in docs/
- Enable HTTPS in GitHub Pages settings

---

## Example Sites

See how others use GitHub Pages:

- https://pages.github.com/
- https://jekyllrb.com/
- https://getbootstrap.com/

---

## SEO & Analytics

### Add Google Analytics

In `docs/index.html`, before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR_GA_ID');
</script>
```

### Add Meta Tags

Already included in `index.html`:
- Description
- Title
- Viewport

---

## Monitoring

### GitHub Insights

Go to: Repository → Insights → Traffic

See:
- Page views
- Visitors
- Referring sites
- Popular content

---

## Advanced: Jekyll (Optional)

GitHub Pages supports Jekyll for enhanced features:

1. Add front matter to HTML:
   ```html
   ---
   layout: default
   title: Home
   ---
   ```

2. Use includes:
   ```
   {% include header.html %}
   ```

3. Use variables:
   ```
   {{ site.title }}
   ```

See: https://jekyllrb.com/docs/

---

## Cost

**GitHub Pages**: Completely FREE
- Unlimited sites
- Unlimited bandwidth
- Custom domains included
- HTTPS included

---

## Next Steps

1. **Push to GitHub** ✓
2. **Enable GitHub Pages** ✓
3. **Deploy Heroku App**
4. **Update links** in GitHub Pages
5. **Share** both URLs!

Your documentation site + live app = Professional project! 🌟

---

## Summary

✅ **GitHub Pages**: Documentation, showcase, landing page
✅ **Heroku**: Live application with simulations
✅ **Together**: Complete professional deployment

Both are FREE for basic use!
