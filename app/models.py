from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, Boolean, DateTime

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app, db

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

    id = db.Column(db.Integer, primary_key=True)
    total_xp = db.Column(db.Integer, default=0)
    current_levvel = 