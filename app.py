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


@app.route('/tasks')
def tasks_view():
    """View and manage all tasks"""
    
    effort_filter = request.args.get('effort')
    location_filter = request.args.get('location')
    energy_filter = request.args.get('energy')

    filters = {}
    if effort_filter:
        filters['effort_type'] = effort_filter
    if location_filter:
        filters['location_type'] = location_filter
    if energy_filter:
        filters['energy_level'] = energy_filter
    

    tasks = get_tasks(filters=filters if filters else None)

    return render_template('tasks.html',
                           tasks=tasks,
                           current_filters=filters)


@app.route('/add_task', methods=['GET', 'POST'])
def add_task_view():
    """Add a new task"""

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description', '')
        task_type = request.form.get('task_type')
        points = int(request.form.get('points'))
        effort_type = request.form.get('effort_type')
        location_type = request.form.get('location_type')
        energy_level = request.form.get('energy_level')

        add_task(title, description, task_type, points, effort_type, location_type, energy_level)

        return redirect(url_for('dashboard'))
    
    return render_template('add_task.html')


@app.route('/complete_task/<int:task_id>', methods=['POST'])
def complete_task_route(task_id):
    """Mark a task complete"""

    tasks = get_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)

    if task:
        complete_task(task_id, task['points'])
        return jsonify({'success': True, 'message': f'Quest completed! +{task["points"]} XP'})
    
    return jsonify({'success': False, 'message': 'Task not found'}), 404


@app.route('/quest_select')
def quest_select():
    """Quest selection interface based on mood/energy"""
    return render_template('quest_select.html')


@app.route('/api/tasks/filter', methods=['POST'])
def filter_tasks():
    """API endpoint to filter tasks based on current state"""

    data = request.get_json()

    filters = {}
    if data.get('effort_type'):
        filters['effort_type'] = data['effort_type']
    if data.get('location_type'):
        filters['location_type'] = data['location_type']
    if data.get('energy_level'):
        filters['energy_level'] = data['energy_level']
    
    tasks = get_tasks(filters=filters if filters else None)
    return jsonify({'tasks': tasks})


if __name__ == '__main__':
    print("\n🎮 Conquer Started!")
    print("📍 Open your browser to: http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
