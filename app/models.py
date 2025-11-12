from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, Boolean, Date, DateTime

from flask_sqlalchemy import SQLAlchemy
import datetime as dt
from datetime import datetime
from app import app, db
from typing import List

db = SQLAlchemy()

# Task Categories
CATEGORIES = [
    'Work',
    'Coding / Personal Projects',
    'Cleaning',
    'Adulting',
    'Doby',
    'Social',
    'Errands',
    'Self Care'
]


class UserProgress(db.Model):
    """Track user's overall progress and stats"""
    __tablename__ = 'user_progress'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_xp: Mapped[int] = mapped_column(Integer, default=0)
    current_level: Mapped[int] = mapped_column(Integer, default=1)
    tasks_completed: Mapped[int] = mapped_column(Integer, default=0)
    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0)
    last_completion_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)

    def calculate_level(self):
        """Calculate level based on XP (100 XP per level)"""
        return max(1, (self.total_xp // 100) + 1)
    
    def xp_for_next_level(self):
        """Calculate XP needed for next level"""
        current_level = self.calculate_level()
        next_level_xp = current_level * 100
        return next_level_xp - self.total_xp
    
    def xp_progress_percent(self):
        """Calculate progress percentage within current level"""
        return ((self.total_xp % 100) / 100) * 100


class TaskTemplate(db.Model):
    """Template for tasks that can be instantiated multiple times"""
    __tablename__ = 'task_templates'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(100))
    task_type: Mapped[str] = mapped_column(String(50), nullable=False) # daily, weekly, bonus
    effort_type: Mapped[str] = mapped_column(String(50)) # physical, mental, creative
    location_type: Mapped[str] = mapped_column(String(50)) # indoor, outdoor, any

    # Base XP for each tier
    base_xp_low: Mapped[int] = mapped_column(Integer, default=10)
    base_xp_medium: Mapped[int] = mapped_column(Integer, default=20)
    base_xp_high: Mapped[int] = mapped_column(Integer, default=30)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=datetime.now(dt.timezone.utc))

    # Relationships
    subtasks: Mapped[List['SubTask']] = relationship(back_populates='template', lazy=True, cascade='all, delete-orphan', order_by='SubTask.order')
    instances: Mapped[List['TaskInstance']] = relationship(back_populates='template', lazy=True, cascade='all, delete-orphan')

    def get_subtasks_for_tier(self, tier):
        """Get all subtasks for a given tier (cumulative)"""
        return [st for st in self.subtasks if st.level <= tier]
    
    def calculate_xp(self, tier, completed_subtask_count):
        """Calculate total XP based on tier and completed subtasks"""
        base_xp = {
            1: self.base_xp_low,
            2: self.base_xp_medium,
            3: self.base_xp_high
        }.get(tier, self.base_xp_low)

        # Add conus XP per completed subtask
        subtask_bonus = completed_subtask_count * 2
        return base_xp + subtask_bonus


class SubTask(db.Model):
    """Individual sub-task belonging to a template"""
    __tablename__ = 'sub_tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    template_id: Mapped[int] = mapped_column(Integer, ForeignKey('task_templates.id'), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)  # 1, 2, or 3
    order: Mapped[int] = mapped_column(Integer, default=0)  # For display ordering

    def __repr__(self) -> str:
        return f'<SubTask {self.description} (L{self.level})>'


class TaskInstance(db.Model):
    """An instance of a template added to a specific day"""
    __tablename__ = 'task_instances'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    template_id: Mapped[int] = mapped_column(Integer, ForeignKey('task_templates.id'), nullable=False)
    selected_tier: Mapped[int] = mapped_column(Integer, nullable=False)  # 1, 2, or 3

    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=datetime.now(dt.timezone.utc))
    completed_at: Mapped[dt.datetime] = mapped_column(DateTime, nullable=True)
    xp_earned: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    subtask_completions: Mapped[List['SubTaskCompletion']] = relationship(back_populates='task_instance', lazy=True, cascade='all, delete-orphan')


    @property
    def is_completed(self):
        """Check if task is marked as complete"""
        return self.completed_at is not None
    
    def get_available_subtasks(self):
        """Get all subtasks available for this instance's tier"""
        return self.template.get_subtasks_for_tier(self.selected_tier)
    
    def get_completion_status(self):
        """Get completion stats for this instance"""
        available = self.get_available_subtasks()
        completed = [sc for sc in self.subtask_completions if sc.completed]

        return {
            'total': len(available),
            'completed': len(completed),
            'percentage': (len(completed) / len(available) * 100) if available else 0
        }
    
    def can_upgrade_tier(self):
        """Check if user can upgrade to next tier (all current subtasks done)"""
        if self.selected_tier >= 3:
            return False
        
        status = self.get_completion_status()
        return status['percentage'] == 100