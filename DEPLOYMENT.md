# Deployment Guide - FinTech Personal Finance Application

This guide walks you through deploying the FinTech application to production using:
- **Frontend**: Netlify (Free tier)
- **Backend**: Render (Free tier)
- **Database**: MongoDB Atlas (Free tier - M0)

---

## 📋 Prerequisites

- Git repository (GitHub, GitLab, or Bitbucket)
- MongoDB Atlas account
- Netlify account
- Render account

---

## 🗄️ Step 1: MongoDB Atlas Setup

### 1.1 Create MongoDB Atlas Account

1. Visit [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Click **"Try Free"** and create an account
3. Sign in to your Atlas dashboard

### 1.2 Create a Database Cluster

1. Click **"Build a Database"** or **"Create"**
2. Choose **FREE (M0)** tier
3. Select a cloud provider and region (choose closest to your users)
   - Recommended for India: **AWS - Mumbai (ap-south-1)**
4. Name your cluster (e.g., `fintech-cluster`)
5. Click **"Create Cluster"** (takes 3-5 minutes)

### 1.3 Create Database User

1. Go to **Database Access** in the left sidebar
2. Click **"Add New Database User"**
3. Choose **"Password"** authentication
4. Set username: `fintech_user`
5. Click **"Autogenerate Secure Password"** and **copy it** (save it securely!)
6. Set privileges: **"Read and write to any database"**
7. Click **"Add User"**

### 1.4 Configure Network Access

1. Go to **Network Access** in the left sidebar
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (0.0.0.0/0)
   - This allows Render to connect (Render uses dynamic IPs)
4. Click **"Confirm"**

### 1.5 Get Connection String

1. Go back to **Database** and click **"Connect"**
2. Choose **"Connect your application"**
3. Select **Driver: Python**, **Version: 3.12 or later**
4. Copy the connection string (looks like):
   ```
   mongodb+srv://fintech_user:<password>@fintech-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. Replace `<password>` with the password you copied earlier
6. **Save this connection string** - you'll need it for Render

---

## 🚀 Step 2: Deploy Backend to Render

### 2.1 Push Code to Git

If not already done:
```bash
cd c:\Users\LDNA40022\Lokesh\FinTech_App
git add .
git commit -m "Add deployment configurations"
git push origin main
```

### 2.2 Create Render Account

1. Visit [render.com](https://render.com)
2. Sign up with your GitHub/GitLab account

### 2.3 Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your Git repository
3. Select the **FinTech_App** repository
4. Configure the service:
   - **Name**: `fintech-backend` (or your choice)
   - **Region**: Choose closest to you (e.g., Singapore)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 2.4 Configure Environment Variables

Click **"Advanced"** and add these environment variables:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Generate one: run `python -c "import secrets; print(secrets.token_hex(32))"` |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `MONGODB_URL` | Your MongoDB Atlas connection string from Step 1.5 |
| `DATABASE_NAME` | `fintech_app` |
| `CORS_ORIGINS` | `["http://localhost:5173"]` (we'll update this after Netlify deployment) |
| `REMINDER_DAYS_BEFORE` | `3` |
| `DEBUG` | `False` |
| `APP_NAME` | `FinTech Personal Finance Manager` |
| `APP_VERSION` | `1.0.0` |

**Optional: Twilio (for WhatsApp reminders)**
| Key | Value |
|-----|-------|
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token |
| `TWILIO_WHATSAPP_FROM` | `whatsapp:+14155238886` |

### 2.5 Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Once deployed, copy your backend URL: `https://fintech-backend.onrender.com`
4. Test health check: Visit `https://fintech-backend.onrender.com/health`

> **Important**: Free tier on Render spins down after 15 minutes of inactivity. First request after inactivity may take 30-60 seconds.

---

## 🌐 Step 3: Deploy Frontend to Netlify

### 3.1 Create Netlify Account

1. Visit [netlify.com](https://netlify.com)
2. Sign up with your GitHub/GitLab account

### 3.2 Create New Site

1. Click **"Add new site"** → **"Import an existing project"**
2. Choose your Git provider (GitHub/GitLab)
3. Select the **FinTech_App** repository
4. Configure build settings:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`

### 3.3 Configure Environment Variables

1. Go to **Site settings** → **Build & deploy** → **Environment**
2. Click **"Add a variable"**
3. Add:
   - **Key**: `VITE_API_URL`
   - **Value**: Your Render backend URL (e.g., `https://fintech-backend.onrender.com`)

### 3.4 Deploy

1. Click **"Deploy site"**
2. Wait for build and deployment (3-5 minutes)
3. Once deployed, copy your Netlify URL: `https://your-app-name.netlify.app`

### 3.5 Optional: Custom Domain

1. Go to **Site settings** → **Domain management**
2. Click **"Add custom domain"**
3. Follow instructions to configure your domain

---

## 🔄 Step 4: Update CORS Configuration

Now that you have your Netlify URL, update the backend CORS settings:

1. Go back to **Render dashboard**
2. Open your backend service
3. Go to **Environment** variables
4. Update `CORS_ORIGINS` to:
   ```json
   ["https://your-app-name.netlify.app"]
   ```
5. Save changes (this will trigger a re-deployment)

---

## ✅ Step 5: Verify Deployment

### 5.1 Test Backend

1. Visit `https://fintech-backend.onrender.com/health`
2. Should return:
   ```json
   {
     "status": "healthy",
     "app": "FinTech Personal Finance Manager",
     "version": "1.0.0",
     "database": "connected"
   }
   ```

3. Test API docs: `https://fintech-backend.onrender.com/docs`

### 5.2 Test Frontend

1. Visit `https://your-app-name.netlify.app`
2. Register a new account
3. Login and test features:
   - Add expenses
   - Create EMI
   - Add bank accounts
   - View dashboard analytics

---

## 🔧 Troubleshooting

### Backend Issues

**Problem**: Health check shows `database: "disconnected"`
- **Solution**: Check MongoDB Atlas connection string in Render environment variables
- Ensure password has no special characters or is properly URL-encoded
- Verify Network Access allows 0.0.0.0/0 in MongoDB Atlas

**Problem**: CORS errors in browser console
- **Solution**: Update `CORS_ORIGINS` in Render to include your Netlify URL
- Format must be: `["https://your-app-name.netlify.app"]` (no trailing slash)

**Problem**: Service is slow or times out
- **Solution**: Free tier spins down after inactivity (cold start ~30-60 seconds)
- Consider upgrading to paid tier for always-on service

### Frontend Issues

**Problem**: "Network Error" or "Failed to fetch"
- **Solution**: Check `VITE_API_URL` in Netlify environment variables
- Ensure it matches your Render backend URL exactly
- Rebuild site after changing environment variables

**Problem**: 404 errors on page refresh
- **Solution**: Check that `netlify.toml` exists with redirect rules
- Netlify should automatically handle SPA routing

### Database Issues

**Problem**: Can't connect to MongoDB Atlas
- **Solution**: 
  - Verify username and password are correct
  - Check that IP whitelist includes 0.0.0.0/0
  - Ensure cluster is running (not paused)

---

## 📊 Monitoring & Maintenance

### Backend Logs (Render)

1. Go to your service in Render dashboard
2. Click **"Logs"** tab
3. View real-time logs and errors

### Frontend Logs (Netlify)

1. Go to your site in Netlify dashboard
2. Click **"Deploys"** → Select a deploy → **"Deploy log"**

### Database Monitoring (MongoDB Atlas)

1. Go to your cluster in Atlas dashboard
2. Click **"Metrics"** tab
3. View connection counts, operations, storage usage

---

## 🔒 Security Best Practices

1. **Never commit `.env` files** with real credentials to git
2. **Rotate SECRET_KEY** periodically
3. **Use strong passwords** for MongoDB users
4. **Enable 2FA** on all accounts (Netlify, Render, MongoDB Atlas)
5. **Review MongoDB Atlas audit logs** regularly
6. **Set up alerts** in MongoDB Atlas for unusual activity
7. **Use HTTPS only** (automatically handled by Netlify and Render)

---

## 💰 Cost Optimization

### Free Tier Limits

- **Netlify**: 100 GB bandwidth/month
- **Render**: 750 hours/month (enough for 1 service always-on)
- **MongoDB Atlas**: 512 MB storage (M0 tier)

### Upgrade Path

When you need more resources:
1. **Render**: Upgrade to Starter ($7/month) for always-on service
2. **MongoDB Atlas**: Upgrade to M2 ($9/month) for 2GB storage
3. **Netlify**: Pro plan ($19/month) for more bandwidth

---

## 🎯 Next Steps

1. **Set up monitoring**: Configure uptime monitoring (e.g., UptimeRobot)
2. **Configure backups**: Enable automated backups in MongoDB Atlas
3. **Add domain**: Purchase and configure custom domain
4. **SSL certificate**: Automatically provided by Netlify and Render
5. **CI/CD**: Automatic deployments are already configured via Git

---

## 📞 Support

- **MongoDB Atlas**: [docs.atlas.mongodb.com](https://docs.atlas.mongodb.com)
- **Render**: [render.com/docs](https://render.com/docs)
- **Netlify**: [docs.netlify.com](https://docs.netlify.com)

---

**Congratulations! 🎉** Your FinTech application is now live in production!
