{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 cat > backend/models/task_model.py << 'TASKMODEL'\
"""\
Task Model - Database schema for tasks\
Stores all tasks with metadata, priority, status, and avatar links\
"""\
\
from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean, Enum\
from sqlalchemy.sql import func\
from backend.models.database import Base\
import enum\
from datetime import datetime\
\
class TaskPriority(enum.Enum):\
    """Task priority levels"""\
    LOW = "low"\
    MEDIUM = "medium"\
    HIGH = "high"\
    URGENT = "urgent"\
\
class TaskStatus(enum.Enum):\
    """Task lifecycle states"""\
    PENDING = "pending"\
    IN_PROGRESS = "in_progress"\
    COMPLETED = "completed"\
    CANCELLED = "cancelled"\
\
class Task(Base):\
    """\
    Task database model\
    Represents a single task in the POS system\
    """\
    __tablename__ = "tasks"\
    \
    # Primary key\
    id = Column(String(36), primary_key=True, index=True)\
    \
    # User association\
    user_id = Column(String(255), nullable=False, index=True)\
    \
    # Task content\
    title = Column(String(500), nullable=False)\
    description = Column(Text, nullable=True)\
    \
    # Classification\
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)\
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)\
    \
    # Avatar assignment (which life role does this task belong to)\
    avatar_name = Column(String(100), nullable=True)  # e.g., "Warrior", "Businessman"\
    \
    # XP reward\
    xp_reward = Column(Integer, default=10)\
    \
    # Time tracking\
    estimated_minutes = Column(Integer, nullable=True)\
    actual_minutes = Column(Integer, nullable=True)\
    \
    # Scheduling\
    due_date = Column(DateTime, nullable=True)\
    scheduled_time = Column(DateTime, nullable=True)\
    \
    # Metadata\
    created_at = Column(DateTime, server_default=func.now(), nullable=False)\
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)\
    completed_at = Column(DateTime, nullable=True)\
    \
    # Flags\
    is_recurring = Column(Boolean, default=False)\
    is_quest = Column(Boolean, default=False)  # Long-term goals\
    \
    # Source tracking\
    source = Column(String(50), nullable=True)  # e.g., "email", "telegram", "manual", "notion"\
    source_id = Column(String(255), nullable=True)  # External ID from source system\
    \
    # PAEI Framework tags\
    paei_tag = Column(String(10), nullable=True)  # P, A, E, or I\
    \
    # RPM Goal connection\
    goal_id = Column(String(36), nullable=True)  # Links to long-term goal\
    \
    def __repr__(self):\
        return f"<Task(id=\{self.id\}, title='\{self.title\}', status=\{self.status.value\})>"\
    \
    def to_dict(self):\
        """Convert to dictionary for API responses"""\
        return \{\
            "id": self.id,\
            "user_id": self.user_id,\
            "title": self.title,\
            "description": self.description,\
            "priority": self.priority.value,\
            "status": self.status.value,\
            "avatar_name": self.avatar_name,\
            "xp_reward": self.xp_reward,\
            "estimated_minutes": self.estimated_minutes,\
            "actual_minutes": self.actual_minutes,\
            "due_date": self.due_date.isoformat() if self.due_date else None,\
            "scheduled_time": self.scheduled_time.isoformat() if self.scheduled_time else None,\
            "created_at": self.created_at.isoformat(),\
            "updated_at": self.updated_at.isoformat(),\
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,\
            "is_recurring": self.is_recurring,\
            "is_quest": self.is_quest,\
            "source": self.source,\
            "paei_tag": self.paei_tag,\
            "goal_id": self.goal_id\
        \}\
TASKMODEL\
\
echo " Created backend/models/task_model.py"\
}