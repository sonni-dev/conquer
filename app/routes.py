from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, date, timedelta
from app import app, db
from app.models import (
    init_db, get_or_create_user, 
    TaskTemplate, SubTask, TaskInstance, SubTaskCompletion,
    UserProgress, CATEGORIES
)
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize db on startup
init_db(app)


@app.route('/')
def dashboard():
    """Main dashboard view"""
    user = get_or_create_user()

    # Get today's active task instances
    today_instances = TaskInstance.query.filter(
        db.func.date(TaskInstance.created_at) == date.today()
    ).all()

    # Separate by completion status
    active_tasks = [t for t in today_instances if not t.is_completed]
    completed_tasks = [t for t in today_instances if t.is_completed]

    # Get weekly stats
    week_start = date.today() - timedelta(days=date.today().weekday())
    weekly_completions = TaskInstance.query.filter(
        db.func.date(TaskInstance.completed_at) >= week_start
    ).all()

    # Category stats
    category_stats = {}
    for cat in CATEGORIES:
        count = sum(1 for t in weekly_completions if t.template.category == cat)
        category_stats[cat] = count

    return render_template('dashboard.html',
                         user=user,
                         active_tasks=active_tasks,
                         completed_tasks=completed_tasks,
                         weekly_completions=len(weekly_completions),
                         category_stats=category_stats,
                         categories=CATEGORIES)


@app.route('/templates')
def templates_list():
    category_filter = request.args.get('category')

    query = TaskTemplate.query.filter_by(is_active=True)
    if category_filter:
        query = query.filter_by(category=category_filter)
    
    templates = query.all()

    return render_template('templates.html',
                           templates=templates,
                           categories=CATEGORIES,
                           selected_category=category_filter)


@app.route('/template/create', methods=['GET', 'POST'])
def create_template():
    """Create a new task template"""
    if request.method == 'POST':
        # Create template
        template = TaskTemplate(
            title=request.form.get('title'),
            category=request.form.get('category'),
            task_type=request.form.get('task_type'),
            effort_type=request.form.get('effort_type'),
            location_type=request.form.get('location_type'),
            base_xp_low=int(request.form.get('base_xp_low', 10)),
            base_xp_medium=int(request.form.get('base_xp_medium', 20)),
            base_xp_high=int(request.form.get('base_xp_high', 30))
        )
        
        db.session.add(template)
        db.session.flush()  # Get template.id

        # Add subtasks
        subtask_descriptions = request.form.getlist('subtask_description[]')
        subtask_levels = request.form.getlist('subtask_level[]')

        for i, (desc, level) in enumerate(zip(subtask_descriptions, subtask_levels)):
            if desc.strip():  # Only add non-empty subtasks
                subtask = SubTask(
                    template_id=template.id,
                    description=desc.strip(),
                    level=int(level),
                    order=i
                )
                db.session.add(subtask)
        db.session.commit()
        return redirect(url_for('templates_list'))
    return render_template('create_template.html', categories=CATEGORIES)


@app.route('/tasks')
def tasks_view():
    """View and manage all tasks"""
    
    effort_filter = request.args.get('effort')
    location_filter = request.args.get('location')
    category_filter = request.args.get('category')

    filters = {}
    if effort_filter:
        filters['effort_type'] = effort_filter
    if location_filter:
        filters['location_type'] = location_filter
    # if energy_filter:
    #     filters['energy_level'] = energy_filter
    

    tasks = get_tasks(category=category_filter, filters=filters if filters else None)

    return render_template('tasks.html',
                           tasks=tasks,
                           current_filters=filters,
                           categories=CATEGORIES,
                           selected_category=category_filter)


@app.route('/add_task', methods=['GET', 'POST'])
def add_task_view():
    """Add a new task"""

    if request.method == 'POST':
        title = request.form.get('title')
        task_type = request.form.get('task_type')
        category = request.form.get('category')
        
        # High tier
        high_description = request.form.get('high_description')
        high_points = int(request.form.get('high_points'))
        
        # Medium tier
        medium_description = request.form.get('medium_description')
        medium_points = int(request.form.get('medium_points'))
        
        # Low tier
        low_description = request.form.get('low_description')
        low_points = int(request.form.get('low_points'))
        
        effort_type = request.form.get('effort_type')
        location_type = request.form.get('location_type')
        
        add_task(title, task_type, category,
                high_description, high_points,
                medium_description, medium_points,
                low_description, low_points,
                effort_type, location_type)
        
        return redirect(url_for('dashboard'))
    
    return render_template('add_task.html', categories=CATEGORIES)


@app.route('/task/<int:task_id>')
def task_detail(task_id):
    """Show task detail w tier selection for completion"""
    task = get_task_by_id(task_id)
    if not task:
        return "Task not found", 404
    
    return render_template('tasks_detail.html', task=task)


@app.route('/complete_task/<int:task_id>', methods=['POST'])
def complete_task_route(task_id):
    """Mark a task complete w selected tier"""

    data = request.get_json()
    tier = data.get('tier', 'low')  # Default to low if not specified

    task = get_task_by_id(task_id)

    if task:
        # Get points based on tier
        if tier == 'high':
            points = task['high_points']
        elif tier == 'medium':
            points = task['medium_points']
        else:
            points = task['low_points']
        
        complete_task(task_id, tier, points)
        
        tier_emoji = {'high': '🔥', 'medium': '⚡', 'low': '🌙'}
        return jsonify({
            'success': True, 
            'message': f'Quest completed! {tier_emoji.get(tier, "")} {tier.upper()} tier +{points} XP'
        })
    
    return jsonify({'success': False, 'message': 'Task not found'}), 404


@app.route('/quest_select')
def quest_select():
    """Quest selection interface based on mood/energy"""
    energy_filter = request.args.get('energy')
    category_filter = request.args.get('category')
    
    return render_template('quest_select.html', 
                         categories=CATEGORIES,
                         selected_energy=energy_filter,
                         selected_category=category_filter)


@app.route('/api/tasks/filter', methods=['POST'])
def filter_tasks():
    """API endpoint to filter tasks based on current state"""

    data = request.get_json()

    filters = {}
    if data.get('effort_type'):
        filters['effort_type'] = data['effort_type']
    if data.get('location_type'):
        filters['location_type'] = data['location_type']
    
    category = data.get('category')
    tasks = get_tasks(category=category, filters=filters if filters else None)
    
    return jsonify({'tasks': tasks})


if __name__ == '__main__':
    print("\n🎮 Conquer Started!")
    print("📍 Open your browser to: http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
