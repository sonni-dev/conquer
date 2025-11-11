from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import (
    init_db, get_user_progress, get_tasks, add_task, 
    complete_task, get_todays_completions, get_weekly_stats,
    xp_for_next_level
)
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize db on startup
init_db()

@app.route('/')
def dashboard():
    """Main dashboard view"""

    progress = get_user_progress()
    xp_needed = xp_for_next_level(progress['total_xp'])
    xp_progress_percent = ((progress['total_xp'] % 100) / 100) * 100

    # Get task counts by type
    daily_tasks = get_tasks(task_type='daily')
    weekly_tasks = get_tasks(task_type='weekly')
    bonus_tasks = get_tasks(task_type='bonus')

    # Get today's completions
    todays_completions = get_todays_completions()

    # Get weekly stats
    weekly_stats = get_weekly_stats()

    return render_template('dashboard.html',
                           progress=progress,
                           xp_needed=xp_needed,
                           xp_progress_percent=xp_progress_percent,
                           daily_tasks=daily_tasks,
                           weekly_tasks=weekly_tasks,
                           bonus_tasks=bonus_tasks,
                           todays_completions=todays_completions,
                           weekly_stats=weekly_stats)