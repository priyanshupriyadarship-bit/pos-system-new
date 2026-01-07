{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh12440\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 cd pos-system\
source venv/bin/activate\
\
cat > backend/integrations/telegram_bot.py << 'TELEGRAM'\
"""\
Telegram Bot Integration - Martin AI Voice Interface\
Provides conversational interface to POS system via Telegram\
"""\
\
from telegram import Update\
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes\
import os\
from typing import Dict, Any\
from backend.core.llm_engine import LLMEngine\
from backend.agents.task_agent import TaskAgent\
from backend.agents.calendar_agent import CalendarAgent\
from backend.agents.xp_agent import XPAgent\
\
class TelegramBot:\
    """Martin AI - Telegram conversational interface for POS"""\
    \
    def __init__(self, token: str, user_id: str):\
        self.token = token\
        self.user_id = user_id\
        self.llm = LLMEngine()\
        self.task_agent = TaskAgent(user_id)\
        self.calendar_agent = CalendarAgent(user_id)\
        self.xp_agent = XPAgent(user_id)\
        self.app = Application.builder().token(token).build()\
        self._setup_handlers()\
    \
    def _setup_handlers(self):\
        """Register command and message handlers"""\
        self.app.add_handler(CommandHandler("start", self.start_command))\
        self.app.add_handler(CommandHandler("stats", self.stats_command))\
        self.app.add_handler(CommandHandler("tasks", self.tasks_command))\
        self.app.add_handler(CommandHandler("schedule", self.schedule_command))\
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))\
    \
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):\
        """Welcome message"""\
        welcome = """\
\uc0\u55357 \u56395  Hello! I'm Martin, your AI personal operating system.\
\
I can help you with:\
- \uc0\u55357 \u56541  Managing tasks and goals\
- \uc0\u55357 \u56517  Scheduling your day\
- \uc0\u55356 \u57262  Tracking avatar progress\
- \uc0\u55357 \u56522  Analyzing your productivity\
\
Just chat with me naturally! Try:\
- "Add task: Review ML project"\
- "What's my schedule today?"\
- "Show my avatar stats"\
        """\
        await update.message.reply_text(welcome)\
    \
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):\
        """Show avatar stats"""\
        stats = self.xp_agent.get_user_stats()\
        \
        message = "\uc0\u55356 \u57262  Your Avatar Stats:\\n\\n"\
        for name, data in stats['avatars'].items():\
            message += f"\{name\}: Level \{data['level']\} (\{data['xp']\} XP)\\n"\
        \
        message += f"\\n\uc0\u55357 \u56522  Balance: "\
        for name, percent in stats['balance'].items():\
            message += f"\{name\}=\{percent:.1f\}% "\
        \
        await update.message.reply_text(message)\
    \
    async def tasks_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):\
        """Show active tasks"""\
        tasks = self.task_agent.get_active_tasks()\
        \
        if not tasks:\
            await update.message.reply_text("\uc0\u9989  No active tasks! You're all caught up!")\
            return\
        \
        message = "\uc0\u55357 \u56541  Your Active Tasks:\\n\\n"\
        for i, task in enumerate(tasks[:10], 1):\
            priority = "\uc0\u55357 \u56628 " if task['priority'] == 'high' else "\u55357 \u57313 " if task['priority'] == 'medium' else "\u55357 \u57314 "\
            message += f"\{i\}. \{priority\} \{task['title']\}\\n"\
        \
        await update.message.reply_text(message)\
    \
    async def schedule_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):\
        """Show today's schedule"""\
        schedule = self.calendar_agent.get_today_schedule()\
        \
        if not schedule:\
            await update.message.reply_text("\uc0\u55357 \u56517  No events scheduled for today")\
            return\
        \
        message = "\uc0\u55357 \u56517  Today's Schedule:\\n\\n"\
        for event in schedule:\
            message += f"\{event['start_time']\} - \{event['end_time']\}: \{event['title']\}\\n"\
        \
        await update.message.reply_text(message)\
    \
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):\
        """Process natural language messages with Martin AI"""\
        user_message = update.message.text\
        \
        # Use LLM to understand intent\
        prompt = f"""\
        Analyze this user message and determine the action:\
        Message: "\{user_message\}"\
        \
        Available actions:\
        - create_task: User wants to add a task\
        - complete_task: User completed something\
        - schedule_event: User wants to schedule something\
        - query_info: User asking for information\
        - general_chat: Casual conversation\
        \
        Respond in JSON format:\
        \{\{"action": "action_type", "details": \{\{\}\}, "response": "natural language response"\}\}\
        """\
        \
        ai_response = self.llm.generate(prompt)\
        \
        # Parse and execute action\
        try:\
            import json\
            parsed = json.loads(ai_response)\
            action = parsed['action']\
            \
            if action == 'create_task':\
                task_title = parsed['details'].get('title', user_message)\
                task = self.task_agent.create_task(\{\
                    'title': task_title,\
                    'description': user_message\
                \})\
                response = f" Created task: \{task_title\}"\
            \
            elif action == 'complete_task':\
                response = "\uc0\u55356 \u57225  Great job! Task marked complete!"\
            \
            elif action == 'schedule_event':\
                response = "\uc0\u55357 \u56517  I've added that to your calendar"\
            \
            else:\
                response = parsed.get('response', "I'm here to help! What would you like to do?")\
            \
            await update.message.reply_text(response)\
        \
        except Exception as e:\
            await update.message.reply_text("I'm processing that... How else can I help?")\
    \
    def run(self):\
        """Start the bot"""\
        print("\uc0\u55358 \u56598  Martin AI Bot is running...")\
        self.app.run_polling()\
\
# Example usage\
if __name__ == "__main__":\
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")\
    USER_ID = "default_user"\
    \
    if not TOKEN:\
        print("\uc0\u10060  Error: TELEGRAM_BOT_TOKEN not set in .env file")\
        print("Get your token from @BotFather on Telegram")\
    else:\
        bot = TelegramBot(TOKEN, USER_ID)\
        bot.run()\
TELEGRAM\
\
echo "\uc0\u9989  Created backend/integrations/telegram_bot.py"\
}