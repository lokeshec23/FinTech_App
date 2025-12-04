---
description: Deploy the FinTech application to Netlify and Render
---

# Deployment Workflow

This workflow guides you through deploying the FinTech application to production.

## Prerequisites

Before starting, ensure you have:
- [ ] MongoDB Atlas account and connection string ready
- [ ] Render account created
- [ ] Netlify account created
- [ ] Code pushed to a Git repository (GitHub/GitLab)

## Step 1: Setup MongoDB Atlas

// turbo
1. Open MongoDB Atlas in browser
   - Visit: https://www.mongodb.com/cloud/atlas

2. Create a free M0 cluster:
   - Click "Build a Database"
   - Select FREE (M0) tier
   - Choose region closest to you (e.g., AWS Mumbai for India)
   - Name: `fintech-cluster`

3. Create database user:
   - Go to "Database Access"
   - Add new user: `fintech_user`
   - Autogenerate secure password and SAVE IT
   - Privileges: Read and write to any database

4. Configure network access:
   - Go to "Network Access"
   - Add IP: 0.0.0.0/0 (Allow from anywhere)

5. Get connection string:
   - Go to "Database" → "Connect"
   - Choose "Connect your application"
   - Copy connection string
   - Replace `<password>` with your saved password
   - **Save this for Render deployment**

## Step 2: Deploy Backend to Render

// turbo
1. Generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
   - **Copy the output for Render environment variables**

2. Push code to Git (if not already):
```bash
git add .
git commit -m "Add deployment configurations"
git push origin main
```

3. Deploy to Render:
   - Visit: https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your repository
   - Configure:
     - **Name**: `fintech-backend`
     - **Region**: Singapore (or closest)
     - **Branch**: `main`
     - **Root Directory**: `backend`
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. Add environment variables in Render:
   ```
   SECRET_KEY = <paste the secret key from step 1>
   ALGORITHM = HS256
   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   MONGODB_URL = <paste MongoDB Atlas connection string>
   DATABASE_NAME = fintech_app
   CORS_ORIGINS = ["http://localhost:5173"]
   REMINDER_DAYS_BEFORE = 3
   DEBUG = False
   APP_NAME = FinTech Personal Finance Manager
   APP_VERSION = 1.0.0
   ```

5. Click "Create Web Service" and wait for deployment (5-10 minutes)

6. Copy your Render backend URL: `https://fintech-backend-xxxx.onrender.com`

7. Test the deployment:
   - Visit: `https://your-backend-url.onrender.com/health`
   - Should return: `{"status": "healthy", "database": "connected"}`

## Step 3: Deploy Frontend to Netlify

// turbo
1. Deploy to Netlify:
   - Visit: https://app.netlify.com
   - Click "Add new site" → "Import an existing project"
   - Connect your Git repository
   - Configure:
     - **Base directory**: `frontend`
     - **Build command**: `npm run build`
     - **Publish directory**: `frontend/dist`

2. Add environment variable:
   - Go to "Site settings" → "Build & deploy" → "Environment"
   - Add variable:
     - **Key**: `VITE_API_URL`
     - **Value**: `https://your-render-backend-url.onrender.com`

3. Click "Deploy site" and wait (3-5 minutes)

4. Copy your Netlify URL: `https://your-app-name.netlify.app`

## Step 4: Update CORS Configuration

1. Go back to Render dashboard
2. Open your backend service
3. Go to "Environment" tab
4. Update `CORS_ORIGINS` to:
   ```
   ["https://your-app-name.netlify.app"]
   ```
5. Save (will trigger re-deployment)

## Step 5: Verify Everything Works

// turbo
1. Test backend health:
```bash
curl https://your-backend-url.onrender.com/health
```

2. Visit your Netlify URL: `https://your-app-name.netlify.app`

3. Test the application:
   - Register a new account
   - Login
   - Add an expense
   - View dashboard

## Troubleshooting

### Backend shows "database: disconnected"
- Check MongoDB Atlas connection string
- Verify Network Access allows 0.0.0.0/0
- Check database user password is correct

### Frontend shows CORS errors
- Update CORS_ORIGINS in Render with exact Netlify URL
- No trailing slash in URL
- Wait for re-deployment

### Backend is very slow
- Free tier spins down after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- This is normal for free tier

## Next Steps

- [ ] Set up custom domain (optional)
- [ ] Configure Twilio for WhatsApp reminders (optional)
- [ ] Set up MongoDB Atlas backups
- [ ] Configure monitoring/alerts

## Important Notes

> **Cold Starts**: Render free tier spins down after inactivity. First load may be slow.

> **MongoDB Limits**: Free M0 tier has 512MB storage limit.

> **Netlify Limits**: 100GB bandwidth/month on free tier.

For detailed instructions, see [DEPLOYMENT.md](file:///c:/Users/LDNA40022/Lokesh/FinTech_App/DEPLOYMENT.md)
