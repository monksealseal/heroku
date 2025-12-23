# 🚀 Deploy Your GCM to Heroku NOW!

## Ready-to-Deploy Package ✅

Everything is configured and ready. Just follow these steps:

---

## Option 1: One Command Deploy (Fastest!)

```bash
# Copy these commands to your terminal:

# 1. Install Heroku CLI (if not installed)
curl https://cli-assets.heroku.com/install.sh | sh

# 2. Login to Heroku
heroku login

# 3. Create and deploy
heroku create
git push heroku claude/build-gcm-physics-VaCFZ:main
heroku open
```

**That's it!** Your app will be live in ~3 minutes.

---

## Option 2: Use the Automated Script

```bash
./deploy.sh
```

This script does everything automatically.

---

## Option 3: Manual Step-by-Step

### Step 1: Install Heroku CLI

**macOS:**
```bash
brew tap heroku/brew && brew install heroku
```

**Ubuntu/Linux:**
```bash
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
```

**Windows:**
Download from: https://devcenter.heroku.com/articles/heroku-cli

### Step 2: Login

```bash
heroku login
# Press any key to open browser
# Login with your Heroku account
```

### Step 3: Create App

```bash
# Create with random name
heroku create

# OR create with your own name
heroku create my-gcm-simulator
```

You'll see:
```
Creating app... done, ⬢ your-app-name
https://your-app-name.herokuapp.com/ | https://git.heroku.com/your-app-name.git
```

### Step 4: Deploy

```bash
git push heroku claude/build-gcm-physics-VaCFZ:main
```

You'll see the build process:
```
remote: -----> Building on the Heroku-22 stack
remote: -----> Using buildpack: heroku/python
remote: -----> Python app detected
remote: -----> Installing python-3.11.7
remote: -----> Installing pip dependencies
remote:        Collecting numpy>=1.24.0
remote:        Collecting scipy>=1.10.0
remote:        Collecting flask>=3.0.0
remote:        Collecting gunicorn>=21.2.0
remote:        Collecting matplotlib>=3.7.0
...
remote: -----> Compressing...
remote: -----> Launching...
remote: https://your-app-name.herokuapp.com/ deployed to Heroku
```

### Step 5: Open Your App

```bash
heroku open
```

---

## ⚡ Ultra-Quick Deploy (Copy-Paste)

**If you already have Heroku CLI:**

```bash
heroku login && \
heroku create && \
git push heroku claude/build-gcm-physics-VaCFZ:main && \
heroku open
```

Just paste this one line and press Enter!

---

## 🎯 What Happens After Deploy

Your app will be live at:
```
https://[your-app-name].herokuapp.com
```

### Test It:

1. **Open the URL** in your browser
2. **Configure a test simulation:**
   - Resolution: 32×16×10 (Fast)
   - Profile: Tropical
   - CO₂: 400 ppmv
   - Duration: 5 days
3. **Click "Run Simulation"**
4. **Watch the progress bar** (takes ~2-3 minutes)
5. **View beautiful results!**

---

## 📊 What You'll See

### On First Visit:
- Beautiful gradient background (purple/blue)
- Configuration panel on the left
- Results panel on the right
- "Run Simulation" button

### During Simulation:
- Progress bar (0% → 100%)
- Status updates
- Real-time percentage

### After Completion:
- 4 statistics cards:
  - Global Mean Temp
  - Surface Temp
  - Max Wind Speed
  - Mean Humidity
- Interactive plot tabs:
  - Surface Temperature
  - Zonal Wind
  - Humidity
  - Diagnostics

---

## 🔍 Verify Deployment

```bash
# Check app status
heroku ps

# View logs
heroku logs --tail

# Get app info
heroku apps:info
```

---

## 🎨 Customize Your App

### Change App Name

```bash
heroku apps:rename new-name
```

### Add Custom Domain

```bash
heroku domains:add www.myapp.com
```

### Enable SSL (Free)

```bash
heroku certs:auto:enable
```

---

## 💰 Cost

**Free Tier** (Perfect for testing):
- 550 dyno hours/month
- Sleeps after 30 min inactivity
- Perfect for demos
- **Cost: $0**

**Hobby Tier** (Recommended):
- Always on (no sleeping)
- Custom domains
- SSL included
- **Cost: $7/month**

Upgrade anytime:
```bash
heroku ps:type hobby
```

---

## 🆘 Troubleshooting

### "App not found"
```bash
# Check your apps
heroku apps

# If none exist, create one
heroku create
```

### "No Heroku remote"
```bash
# Add Heroku remote
heroku git:remote -a your-app-name
```

### "Build failed"
```bash
# Check logs
heroku logs --tail

# Usually fixes itself on retry
git push heroku claude/build-gcm-physics-VaCFZ:main
```

### "App crashed"
```bash
# View errors
heroku logs --tail

# Restart
heroku restart
```

---

## 📱 Access Your App

After deployment, you can access it:

### On Desktop:
```
https://your-app-name.herokuapp.com
```

### On Mobile:
Same URL works perfectly - the UI is responsive!

### API Access:
```bash
curl https://your-app-name.herokuapp.com/api/simulations
```

---

## 🎓 Next Steps After Deploy

1. **Share the URL** with colleagues
2. **Run different scenarios:**
   - Try polar vs tropical profiles
   - Compare 280 ppmv vs 560 ppmv CO₂
   - Test different resolutions
3. **Monitor performance:**
   ```bash
   heroku logs --tail
   ```
4. **Scale up if needed:**
   ```bash
   heroku ps:type hobby
   ```
5. **Add your own features**
6. **Enjoy!** 🎉

---

## 🌟 You're Deploying:

✅ Complete GCM with sophisticated physics
✅ Modern web interface
✅ Real-time visualizations
✅ Production-ready code
✅ Professional documentation
✅ Optimized for cloud

**Your climate model is ready for the world!** 🌍

---

## Need Help?

- Deployment issues? Check DEPLOYMENT.md
- Heroku questions? Visit https://devcenter.heroku.com
- GCM usage? See docs/USER_GUIDE.md

---

**Ready? Run this now:**

```bash
heroku login && heroku create && git push heroku claude/build-gcm-physics-VaCFZ:main && heroku open
```

🚀 **Let's deploy!**
