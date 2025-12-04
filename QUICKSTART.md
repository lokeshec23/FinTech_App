# Quick Start Guide

This guide will help you get the FinTech Personal Finance Management Application up and running quickly.

## Prerequisites Check

```bash
# Check Python version (need 3.8+)
python --version

# Check Node.js version (need 16+)
node --version

# Check MongoDB (if using local)
mongo --version
```

## Quick Setup (Windows)

### 1. Backend Setup (5 minutes)

```bash
# Navigate to backend
cd c:\Users\LDNA40022\Lokesh\FinTech_App\backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy .env.example .env

# Generate secret key and update .env
python -c "import secrets; print(secrets.token_hex(32))"
# Copy the output and replace SECRET_KEY in .env
```

### 2. MongoDB Setup

**Quick option: MongoDB Atlas (Free Cloud)**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free account and cluster (takes 3-5 minutes)
3. Get connection string
4. Update `MONGODB_URL` in backend/.env

### 3. Frontend Setup (3 minutes)

```bash
# Navigate to frontend
cd ..\frontend

# Install dependencies
npm install

# Copy environment file
copy .env.example .env
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Access the Application

Open browser and go to: http://localhost:5173

## First Use

1. Click "Sign up" on the login page
2. Fill in your details (use +91XXXXXXXXXX format for phone)
3. After registration, you'll be redirected to the dashboard
4. Start adding expenses, EMIs, and financial data!

## Common Issues & Solutions

### MongoDB Connection Error
- **Local**: Make sure MongoDB service is running
- **Atlas**: Check connection string in .env includes username/password

### Backend Won't Start
```bash
# Make sure you're in the virtual environment
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Won't Start
```bash
# Clear node_modules and reinstall
rmdir /s /q node_modules
npm install
```

### CORS Error
- Backend must be running on port 8000
- Frontend must be running on port 5173
- Check CORS_ORIGINS in backend/.env

## Next Steps

1. **Add test data**: Create some expenses and EMIs to see the dashboard populate
2. **Configure WhatsApp**: (Optional) Set up Twilio for payment reminders
3. **Customize**: Modify categories, add more features

## Need Help?

- Check README.md for detailed documentation
- Review the API docs at http://localhost:8000/docs
- Check backend logs in the terminal
