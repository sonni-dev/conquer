from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime, date, timedelta
import datetime as dt
from app import app, db
from app.models import (
    get_or_create_user, 
    TaskTemplate, SubTask, TaskInstance, SubTaskCompletion,
    UserProgress, CATEGORIES
)
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize db on startup
# init_db(app)


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
        TaskInstance.completed_at.isnot(None),
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
    """View all task templates"""
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


@app.route('/template/<int:template_id>/edit', methods=['GET', 'POST'])
def edit_template(template_id):
    """Edit an existing template"""
    template = TaskTemplate.query.get_or_404(template_id)

    if request.method == 'POST':
        template.title = request.form.get('title')
        template.category = request.form.get('category')
        template.task_type = request.form.get('task_type')
        template.effort_type = request.form.get('effort_type')
        template.location_type = request.form.get('location_type')
        template.base_xp_low = int(request.form.get('base_xp_low', 10))
        template.base_xp_medium = int(request.form.get('base_xp_medium', 20))
        template.base_xp_high = int(request.form.get('base_xp_high', 30))

        # Delete existing subtasks and recreate
        SubTask.query.filter_by(template_id=template.id).delete()

        subtask_descriptions = request.form.getlist('subtask_descriptions[]')
        subtask_levels = request.form.getlist('subtask_level[]')

        for i, (desc, level) in enumerate(zip(subtask_descriptions, subtask_levels)):
            if desc.strip():
                subtask = SubTask(
                    template_id=template.id,
                    description=desc.strip(),
                    level=int(level),
                    order=i
                )
                db.session.add(subtask)
        
        db.session.commit()
        return redirect(url_for('templates_list'))
    
    return render_template('edit_template.html', template=template, categories=CATEGORIES)


@app.route('/template/<int:template_id>/add', methods=['POST'])
def add_task_from_template(template_id):
    """Create task instance from a template"""
    template = TaskTemplate.query.get_or_404(template_id)
    tier = int(request.form.get('tier', 1))

    # Create task instance
    instance = TaskInstance(
        template_id=template.id,
        selected_tier=tier
    )
    db.session.add(instance)
    db.session.flush()

    # Create subtask completions for available subtasks
    available_subtasks = template.get_subtasks_for_tier(tier)
    for subtask in available_subtasks:
        completion = SubTaskCompletion(
            task_instance=instance.id,
            subtask_id=subtask.id,
            completed=False
        )
        db.session.add(completion)
    
    db.session.commit()

    tier_names = {1: '🌙 Low', 2: '⚡ Medium', 3: '🔥 High'}
    flash(f'Added {template.title} to your tasks ({tier_names[tier]} Energy)!', 'success')
    
    return redirect(url_for('task_detail', instance_id=instance.id))


@app.route('/task/<int:instance_id>')
def task_detail(instance_id):
    """View task instance with subtasks"""
    instance = TaskInstance.query.get_or_404(instance_id)
    return render_template('tasks_detail.html', instance=instance)


@app.route('/task/<int:instance_id>/toggle-subtask/<int:completion_id>', methods=['POST'])
def toggle_subtask(instance_id, completion_id):
    """Toggle a subtask completion"""
    instance = TaskInstance.query.get_or_404(instance_id)
    completion = SubTaskCompletion.query.get_or_404(completion_id)

    if completion.task_instance_id != instance.id:
        flash('Invalid subtask', 'error')
        return redirect(url_for('task_detail', instance_id=instance_id))
    
    completion.toggle()
    db.session.commit()

    # No flash message for checkbox toggle - too noisy
    return redirect(url_for('task_detail', instance_id=instance_id))


@app.route('/task/<int:instance_id>/upgrade-tier', methods=['POST'])
def upgrade_tier(instance_id):
    """Upgrade task to next tier if all current subtasks complete"""
    instance = TaskInstance.query.get_or_404(instance_id)

    if not instance.can_upgrade_tier():
        flash('Complete all subtasks before upgrading!', 'error')
        return redirect(url_for('task_detail', instance_id=instance_id))
    
    if instance.selected_tier >=3:
        flash('Already at maximum tier!', 'error')
        return redirect(url_for('task_detail', instance_id=instance_id))
    
    # Upgrade tier
    old_tier = instance.selected_tier
    instance.selected_tier += 1

    # Add new subtasks for this tier
    available_subtasks = instance.template.get_subtasks_for_tier(instance.selected_tier)
    existing_subtask_ids = [sc.subtask.id for sc in instance.subtask_completions]

    for subtask in available_subtasks:
        if subtask.id not in existing_subtask_ids:
            completion = SubTaskCompletion(
                task_instance_id=instance.id,
                subtask_id=subtask.id,
                completed=False
            )
            db.session.add(completion)
    
    db.session.commit()

    tier_names = {1: '🌙 Low', 2: '⚡ Medium', 3: '🔥 High'}
    flash(f'Upgraded to {tier_names[instance.selected_tier]} Energy! Keep going!', 'success')
    
    return redirect(url_for('task_detail', instance_id=instance_id))


@app.route('/task/<int:instance_id>/complete', methods=['POST'])
def complete_task(instance_id):
    """Mark task as complete and award XP"""
    instance = TaskInstance.query.get_or_404(instance_id)

    if instance.is_completed:
        flash('Task already completed!', 'error')
        return redirect(url_for('dashboard'))
    
    # Check if at least 50% of subtasks are done
    status = instance.get_completion_status()
    if status['percentage'] < 50:
        flash(f'Complete at least 50% of subtasks ({status["completed"]}/{status["total"]})', 'error')
        return redirect(url_for('task_detail', instance_id=instance_id))
    
    # Calculate XP
    xp_earned = instance.template.calculate_xp(
        instance.selected_tier,
        status['completed']
    )

    instance.completed_at = dt.datetime.now(dt.timezone.utc)
    instance.xp_earned = xp_earned

    # Update user progress
    user = get_or_create_user()
    user.total_xp += xp_earned
    user.tasks_completed += 1

    # Update level
    new_level = user.calculate_level()
    leveled_up = new_level > user.current_level
    user.current_level = new_level

    # Update streak
    today = date.today()
    if user.last_completion_date:
        days_diff = (today - user.last_completion_date).days
        if days_diff == 0:
            pass  # Same day, no streak change
        elif days_diff == 1:
            user.current_streak += 1
            if user.current_streak > user.longest_streak:
                user.longest_streak = user.current_streak
        else:
            user.current_streak = 1
    else:
        user.current_streak = 1
        user.longest_streak = 1

    user.last_completion_date = today

    db.session.commit()

    tier_emoji = {1: '🌙', 2: '⚡', 3: '🔥'}
    message = f'Quest completed! {tier_emoji[instance.selected_tier]} +{xp_earned} XP'
    
    if leveled_up:
        message += f' 🎉 LEVEL UP! Now level {user.current_level}!'
    
    flash('message', 'success')

    return redirect(url_for('dashboard'))


@app.route('/task/<int:instance_id>/delete', methods=['POST'])
def delete_task_instance(instance_id):
    """Delete a task instance"""
    instance = TaskInstance.query.get_or_404(instance_id)

    if instance.is_completed:
        flash('Cannot delete completed task!', 'error')
        return redirect(url_for('dashboard'))
    
    task_title = instance.template.title
    
    db.session.delete(instance)
    db.session.commit()

    flash(f'Removed {task_title} from your tasks', 'success')
    
    return redirect(url_for('dashboard'))


@app.route('/api/templates/filter', methods=['POST'])
def filter_templates():
    """API endpoint to filter templates"""
    data = request.get_json()
    
    query = TaskTemplate.query.filter_by(is_active=True)
    
    if data.get('category'):
        query = query.filter_by(category=data['category'])
    if data.get('effort_type'):
        query = query.filter_by(effort_type=data['effort_type'])
    if data.get('location_type'):
        query = query.filter_by(location_type=data['location_type'])
    
    templates = query.all()
    
    return jsonify({
        'templates': [{
            'id': t.id,
            'title': t.title,
            'category': t.category,
            'task_type': t.task_type,
            'effort_type': t.effort_type,
            'location_type': t.location_type,
            'subtask_count': len(t.subtasks)
        } for t in templates]
    })

