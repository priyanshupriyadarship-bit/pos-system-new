# 🚀 AI Personal Operating System (POS)

**🔴 LIVE DEMO:** https://web-production-fa032.up.railway.app/docs

## ✨ Features
- ✅ **Gmail API** - Send emails automatically
- ✅ **Google Calendar** - Read events & schedule
- ✅ **Telegram Bot** - AI-powered communication  
- ✅ **FastAPI** - Production-ready backend
- ✅ **Railway** - Live deployment & CI/CD

## 🛠️ Tech Stack
FastAPI - Python - Google APIs - Telegram Bot - Railway

text

## 🚀 Quickstart (Local)
```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
Visit: http://localhost:8000/docs

🌐 API Endpoints
text
GET    /docs                    → Interactive API docs
GET    /api/integrations/health  → Health check  
POST   /api/email/send          → Send Gmail
GET    /api/calendar/events     → Read Calendar
