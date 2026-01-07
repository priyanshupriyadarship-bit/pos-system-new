cat > backend/models/user_model.py << 'USERMODEL'
"""
User Model - Database schema for user profiles
Stores user information, avatar stats, preferences, and analytics
"""

from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from backend.models.database import Base
from datetime import datetime

class User(Base):
    """
    User database model
    Represents a POS system user with profile and avatar data
    """
    __tablename__ = "users"
    
    # Primary key
    id = Column(String(36), primary_key=True, index=True)
    
    # User identity
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=True)
    full_name = Column(String(255), nullable=True)
    
    # Authentication (if implementing auth)
    hashed_password = Column(String(255), nullable=True)
    
    # Preferences
    timezone = Column(String(50), default="UTC")
    llm_provider = Column(String(20), default="openai")  # "openai" or "anthropic"
    
    # Avatar stats (stored as JSON)
    avatar_stats = Column(JSON, nullable=True)
    # Example structure:
    # {
    #     "Warrior": {"level": 5, "xp": 450, "tasks_completed": 23},
    #     "Businessman": {"level": 3, "xp": 280, "tasks_completed": 14},
    #     ...
    # }
    
    # Productivity analytics
    total_tasks_completed = Column(Integer, default=0)
    total_xp_earned = Column(Integer, default=0)
    current_streak_days = Column(Integer, default=0)
    longest_streak_days = Column(Integer, default=0)
    
    # Integration tokens (encrypted in production!)
    notion_token = Column(String(500), nullable=True)
    google_refresh_token = Column(String(500), nullable=True)
    telegram_chat_id = Column(String(100), nullable=True)
    
    # Settings (stored as JSON)
    settings = Column(JSON, nullable=True)
    # Example structure:
    # {
    #     "daily_goal_tasks": 5,
    #     "work_hours_start": "09:00",
    #     "work_hours_end": "17:00",
    #     "notification_enabled": true
    # }
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    last_active_at = Column(DateTime, nullable=True)
    
    # Status flags
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "timezone": self.timezone,
            "llm_provider": self.llm_provider,
            "avatar_stats": self.avatar_stats,
            "total_tasks_completed": self.total_tasks_completed,
            "total_xp_earned": self.total_xp_earned,
            "current_streak_days": self.current_streak_days,
            "longest_streak_days": self.longest_streak_days,
            "settings": self.settings,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_active_at": self.last_active_at.isoformat() if self.last_active_at else None,
            "is_active": self.is_active,
            "is_premium": self.is_premium
        }
    
    def update_avatar_stats(self, avatar_name: str, xp_gained: int):
        """Update avatar XP and level"""
        if not self.avatar_stats:
            self.avatar_stats = {}
        
        if avatar_name not in self.avatar_stats:
            self.avatar_stats[avatar_name] = {
                "level": 1,
                "xp": 0,
                "tasks_completed": 0
            }
        
        # Update stats
        self.avatar_stats[avatar_name]["xp"] += xp_gained
        self.avatar_stats[avatar_name]["tasks_completed"] += 1
        
        # Level up logic (100 XP per level)
        new_level = (self.avatar_stats[avatar_name]["xp"] // 100) + 1
        self.avatar_stats[avatar_name]["level"] = new_level
        
        # Update total XP
        self.total_xp_earned += xp_gained
USERMODEL

echo "  Created backend/models/user_model.py"
