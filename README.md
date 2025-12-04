# FinTech Personal Finance Management Application

A comprehensive personal finance management application built with React and FastAPI that helps you track expenses, manage EMIs, monitor assets/liabilities, and get financial insights.

## 🌟 Features

- **📊 Dashboard Analytics**: Real-time financial overview with spending trends and category breakdowns
- **💰 Expense Tracking**: Categorized expense management with monthly views
- **📅 EMI Management**: Track loans with amortization schedules and payment tracking
- **🏦 Bank Account Integration**: Manage multiple bank accounts with balance aggregation
- **💳 UPI Transaction Logging**: Record and track digital payments
- **📈 Financial Insights**: Asset/liability ratio, EMI burden percentage, cash flow forecasts
- **📱 WhatsApp Reminders**: Automated payment reminders via WhatsApp (Twilio)
- **🎯 Financial Goals**: Set and track savings/investment goals
- **🔐 Secure Authentication**: JWT-based authentication
- **🌙 Premium Dark Theme**: Glassmorphism UI with smooth animations

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast Python web framework
- **MongoDB**: NoSQL database with Motor async driver
- **JWT**: Secure authentication
- **Twilio**: WhatsApp integration for reminders
- **APScheduler**: Automated reminder scheduling

### Frontend
- **React 18**: Modern UI library
- **Vite**: Lightning-fast build tool
- **React Router**: Client-side routing
- **Chart.js**: Beautiful data visualizations
- **Axios**: HTTP client
- **React Toastify**: Toast notifications

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB (local or Atlas)
- Twilio account (optional, for WhatsApp reminders)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
cd c:\Users\LDNA40022\Lokesh\FinTech_App
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Edit .env and configure:
# - SECRET_KEY (generate with: openssl rand -hex 32)
# - MONGODB_URL (if using MongoDB Atlas)
# - Twilio credentials (optional)
```

### 3. MongoDB Setup

**Option A: Local MongoDB**
- Install MongoDB Community Edition
- Start MongoDB service
- Use default connection: `mongodb://localhost:27017`

**Option B: MongoDB Atlas (Cloud)**
- Create free account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
- Create cluster and get connection string
- Update `MONGODB_URL` in `.env`

### 4. Frontend Setup

```bash
# Navigate to frontend
cd ../frontend

# Install dependencies
npm install

# Copy environment file
copy .env.example .env

# Edit .env if needed (default works for local development)
```

### 5. Twilio WhatsApp Setup (Optional)

1. Create Twilio account: [twilio.com](https://www.twilio.com/)
2. Get WhatsApp-enabled phone number
3. Configure in backend `.env`:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
   ```

## ▶️ Running the Application

### Start Backend

```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run at: http://localhost:8000

### Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will run at: http://localhost:5173

## 🌐 Production Deployment

Deploy this application to production for free using:
- **Frontend**: Netlify (free tier)
- **Backend**: Render (free tier)  
- **Database**: MongoDB Atlas (free tier)

### Quick Deployment

1. **MongoDB Atlas**: Create free cluster and get connection string
2. **Render**: Deploy backend with MongoDB URL
3. **Netlify**: Deploy frontend with Render backend URL

### Detailed Guides

- **📖 Full Guide**: [DEPLOYMENT.md](./DEPLOYMENT.md) - Complete step-by-step instructions
- **⚡ Quick Reference**: [DEPLOYMENT_QUICK_REFERENCE.md](./DEPLOYMENT_QUICK_REFERENCE.md) - Essential info at a glance
- **🤖 Automated Workflow**: Run `/deploy` command for guided deployment

### Live URLs (after deployment)
- Frontend: `https://your-app-name.netlify.app`
- Backend API: `https://your-backend.onrender.com`
- API Docs: `https://your-backend.onrender.com/docs`

## 📱 Usage

1. **Register**: Create new account at `/register`
2. **Login**: Sign in at `/login`
3. **Dashboard**: View financial overview
4. **Add Expenses**: Track daily spending
5. **Manage EMIs**: Add loans and view payment schedules
6. **Set Goals**: Create financial goals
7. **View Analytics**: Monitor spending patterns

## 🔑 API Documentation

Once the backend is running, access interactive API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📊 Indian Currency Format

All amounts are displayed in Indian Rupees (₹) with proper formatting:
- Example: ₹12,34,567.89 (12 lakhs, 34 thousand, 567 rupees)

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🌐 Environment Variables

### Backend (.env)
```
SECRET_KEY=your-secret-key
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=fintech_app
TWILIO_ACCOUNT_SID=optional
TWILIO_AUTH_TOKEN=optional
TWILIO_WHATSAPP_FROM=optional
REMINDER_DAYS_BEFORE=3
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

## 📂 Project Structure

```
FinTech_App/
├── backend/
│   ├── app/
│   │   ├── models/          # Pydantic models
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── utils/           # Utilities
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # MongoDB connection
│   │   └── main.py          # FastAPI app
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── context/         # React contexts
│   │   ├── services/        # API services
│   │   ├── utils/           # Utilities
│   │   ├── App.jsx          # Main app
│   │   └── main.jsx         # Entry point
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues or questions, please open an issue on GitHub.

## 🎯 Future Enhancements

- Real bank account integration via API
- AI-powered financial advice chat
- Mobile app (React Native)
- Bill reminder system
- Investment portfolio tracking
- Tax calculation features
- Multi-currency support
- Export to Excel/PDF

---

**Made with ❤️ for better financial management**
