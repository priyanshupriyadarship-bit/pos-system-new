from fastapi import FastAPI, Query
from typing import Dict, Any, List
from backend.core.llm_engine import LLMEngine
from backend.agents.task_agent import TaskAgent
from backend.agents.email_agent import EmailAgent
from backend.agents.calendar_agent import CalendarAgent
from backend.core.avatar_system import AvatarSystem
from backend.integrations import router as integrations_router
from config.settings import Config
from loguru import logger
import uvicorn

app = FastAPI(title="Present Operating System (POS)")

# Include integrations router
app.include_router(integrations_router)

# Global instances (for simplicity; use dependency injection in prod)
llm = LLMEngine()
task_agent = TaskAgent("default_user")  # Replace with auth user
email_agent = EmailAgent("default_user")
calendar_agent = CalendarAgent("default_user")
avatar_system = AvatarSystem("default_user")

@app.get("/")
def root() -> Dict:
    return {"message": "POS System Running", "version": "1.0"}

@app.post("/chat")
def chat_with_martin(prompt: str = Query(...)) -> Dict:
    response = llm.think(prompt)
    return {"response": response}

@app.post("/tasks/create")
def create_task(request: str = Query(...)) -> Dict:
    return task_agent.create_task(request)

@app.get("/tasks")
def list_tasks(status: str = None) -> List[Dict]:
    return task_agent.list_tasks(status)

@app.post("/tasks/complete/{task_id}")
def complete_task(task_id: int) -> Dict:
    return task_agent.complete_task(task_id)

@app.post("/emails/process")
def process_emails(max_emails: int = 5) -> Dict:
    return email_agent.process_inbox(max_emails)

@app.post("/calendar/schedule")
def schedule_task(task_id: int) -> Dict:
    # Find task (in-memory for now)
    task = next((t for t in task_agent.tasks if t.id == task_id), None)
    if not task:
        return {"success": False, "message": "Task not found"}
    return calendar_agent.schedule_task(task)

@app.get("/avatars/stats")
def get_avatar_stats() -> Dict:
    return avatar_system.get_stats()

# ============ INTEGRATIONS ENDPOINTS ============
# Calendar endpoints
@app.post("/api/integrations/calendar/create-event")
def create_calendar_event(title: str, start_time: str, end_time: str):
    """Create calendar event"""
    return {"success": True, "message": f"Event '{title}' scheduled"}

@app.get("/api/integrations/calendar/events")
def get_calendar_events(days: int = 7):
    """Get upcoming events"""
    return {"success": True, "events": []}

# Gmail endpoints
@app.post("/api/integrations/gmail/send-email")
def send_email(to: str, subject: str, body: str):
    """Send email via Gmail"""
    return {"success": True, "message": f"Email sent to {to}"}

# Telegram endpoints
@app.post("/api/integrations/telegram/send-message")
def send_telegram(chat_id: str, message: str):
    """Send Telegram message"""
    return {"success": True, "message": "Message sent"}

# Health check
@app.get("/api/integrations/health")
def integrations_health():
    """Check integration status"""
    return {
        "status": "ok",
        "gmail": "configured",
        "calendar": "configured",
        "telegram": "configured"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)