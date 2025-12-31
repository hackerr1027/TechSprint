# 🚀 Free Deployment Checklist

## ✅ Pre-Deployment (Already Done)

- [x] Created `vercel.json` configuration
- [x] Created `.env.production` with Render placeholder
- [x] Updated CORS in `backend/main.py` for Vercel
- [x] Tested production build (✅ Success - 30.97s)

---

## 📋 Deployment Steps

### Step 1: Push to GitHub

```bash
cd c:\Users\admin\Desktop\DAIICT-25dec\TechSprint-main

# Initialize git (if needed)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment - Render + Vercel"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
git branch -M main
git push -u origin main
```

**Status**: ⏳ TODO

---

### Step 2: Deploy Backend to Render

1. Go to [render.com](https://render.com) → Sign up with GitHub
2. **New +** → **Web Service**
3. Connect your repository
4. **Configure**:
   - **Name**: `infragen-backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: **FREE** ⚠️
5. Click **Create Web Service**
6. **Wait 2-5 minutes** for deployment
7. **Copy your URL**: `https://infragen-backend.onrender.com`

**Status**: ⏳ TODO

---

### Step 3: Update Frontend Environment

**Edit `.env.production`** and replace:

```env
VITE_API_URL=https://your-render-backend.onrender.com
```

With your actual Render URL from Step 2.

**Then commit and push:**

```bash
git add .env.production
git commit -m "Update API URL for production"
git push
```

**Status**: ⏳ TODO

---

### Step 4: Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com) → Sign up with GitHub
2. **Add New...** → **Project**
3. **Import** your repository
4. **Configure**:
   - Framework: Vite (auto-detected)
   - Root Directory: `./`
   - Build Command: `npm run build` (auto-filled)
   - Output Directory: `dist` (auto-filled)
5. **Environment Variables**:
   - Name: `VITE_API_URL`
   - Value: `https://your-render-backend.onrender.com`
6. Click **Deploy**
7. **Wait 1-3 minutes**
8. **Copy your URL**: `https://your-app.vercel.app`

**Status**: ⏳ TODO

---

### Step 5: Test Your Deployment

1. Visit your Vercel URL
2. Wait 30 seconds (Render wakes up)
3. Check "Backend Connected" status (should be green)
4. Test infrastructure generation:
   - Input: "Create a VPC with EC2 and RDS"
   - Click "Generate Infrastructure"
   - Verify diagram and code appear

**Status**: ⏳ TODO

---

## 🎯 Quick Reference

### Your URLs (fill in after deployment)

- **Backend (Render)**: `https://________________.onrender.com`
- **Frontend (Vercel)**: `https://________________.vercel.app`
- **Backend API Docs**: `https://________________.onrender.com/docs`

### Important Files

- `backend/main.py` - CORS configuration (✅ Updated)
- `.env.production` - API URL (⏳ Update after Render deployment)
- `vercel.json` - Vercel config (✅ Created)

### Commands

```bash
# Test build locally
npm run build

# Preview production build
npm run preview

# Deploy via Vercel CLI (alternative)
npm install -g vercel
vercel --prod
```

---

## 💡 Tips

1. **First Request Slow?** Render free tier sleeps after 15min - first request takes ~30s
2. **Keep Alive**: Use [UptimeRobot](https://uptimerobot.com) (free) to ping your backend every 5 minutes
3. **Custom Domain**: Both platforms support free custom domains
4. **Auto-Deploy**: Both platforms auto-deploy when you push to GitHub

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Backend not connected" | Wait 30s for Render to wake up |
| CORS errors | Verify `backend/main.py` has `https://*.vercel.app` |
| Build fails on Vercel | Check environment variable `VITE_API_URL` is set |
| 404 on page refresh | Already fixed in `vercel.json` |

---

## 📊 Cost

- **Render Free Tier**: 750 hours/month (enough for 1 app)
- **Vercel Free Tier**: Unlimited deployments
- **Total**: $0/month 🎉

---

## Next Action

**Start with Step 1**: Push your code to GitHub!

```bash
# Quick start
cd c:\Users\admin\Desktop\DAIICT-25dec\TechSprint-main
git init
git add .
git commit -m "Initial deployment"
```

Then create a new repository on GitHub and follow the instructions.
