# 🚀 Quick Deployment Reference

## URLs & Access

### Production URLs (Update after deployment)
- **Frontend (Netlify)**: `https://your-app-name.netlify.app`
- **Backend (Render)**: `https://fintech-backend-xxxx.onrender.com`
- **Backend API Docs**: `https://fintech-backend-xxxx.onrender.com/docs`
- **Backend Health**: `https://fintech-backend-xxxx.onrender.com/health`

### Development URLs
- **Frontend**: `http://localhost:5173`
- **Backend**: `http://localhost:8000`
- **Backend API Docs**: `http://localhost:8000/docs`

---

## 🔑 Required Credentials

### MongoDB Atlas
```
Connection String: mongodb+srv://username:password@cluster.mongodb.net/...
Database Name: fintech_app
```

### Backend Secret Key
```bash
# Generate with:
python -c "import secrets; print(secrets.token_hex(32))"
```

### Optional: Twilio (WhatsApp Reminders)
```
TWILIO_ACCOUNT_SID: ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN: your_auth_token
TWILIO_WHATSAPP_FROM: whatsapp:+14155238886
```

---

## 📝 Environment Variables Checklist

### Render (Backend)
- [ ] `SECRET_KEY` - Generated secure key
- [ ] `MONGODB_URL` - MongoDB Atlas connection string
- [ ] `DATABASE_NAME` - `fintech_app`
- [ ] `CORS_ORIGINS` - `["https://your-netlify-url.netlify.app"]`
- [ ] `ALGORITHM` - `HS256`
- [ ] `ACCESS_TOKEN_EXPIRE_MINUTES` - `30`
- [ ] `DEBUG` - `False`
- [ ] `APP_NAME` - `FinTech Personal Finance Manager`
- [ ] `APP_VERSION` - `1.0.0`
- [ ] `REMINDER_DAYS_BEFORE` - `3`

### Netlify (Frontend)
- [ ] `VITE_API_URL` - `https://your-render-backend.onrender.com`

---

## 🎯 Deployment Sequence

1. **MongoDB Atlas** → Create cluster & get connection string
2. **Render Backend** → Deploy with MongoDB URL
3. **Netlify Frontend** → Deploy with Render backend URL
4. **Update CORS** → Add Netlify URL to Render backend

---

## ✅ Verification Commands

```bash
# Test backend health
curl https://your-backend.onrender.com/health

# Expected response:
{
  "status": "healthy",
  "app": "FinTech Personal Finance Manager",
  "version": "1.0.0",
  "database": "connected"
}
```

---

## ⚠️ Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| Database disconnected | Check MongoDB connection string & Network Access (0.0.0.0/0) |
| CORS error | Update `CORS_ORIGINS` in Render with exact Netlify URL |
| Backend slow/timeout | Free tier cold start (~30-60s after inactivity) |
| Build fails | Check build logs in Render/Netlify dashboard |
| Frontend can't reach API | Verify `VITE_API_URL` matches Render backend URL |

---

## 📞 Dashboard Links

- **MongoDB Atlas**: https://cloud.mongodb.com
- **Render**: https://dashboard.render.com
- **Netlify**: https://app.netlify.com
- **Twilio**: https://console.twilio.com (optional)

---

## 🔄 Update & Redeploy

### Backend Changes
```bash
git add .
git commit -m "Update backend"
git push origin main
# Render auto-deploys from Git
```

### Frontend Changes
```bash
git add .
git commit -m "Update frontend"
git push origin main
# Netlify auto-deploys from Git
```

---

## 💡 Pro Tips

- **Monitor logs**: Check Render/Netlify dashboards for errors
- **Cold starts**: First request after 15min inactivity is slow on free tier
- **CORS**: Always update after changing frontend URL
- **Backups**: Enable automated backups in MongoDB Atlas
- **Custom domain**: Free on Netlify, configure in Site Settings

---

For detailed instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)
