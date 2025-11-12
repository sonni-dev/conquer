from app import app
from app.models import db, TaskTemplate, SubTask

def populate_sample_templates():
    """Add sample task templates with tiered subtasks"""
    
    templates_data = [
        # Cleaning - Kitchen
        {
            'title': 'Clean the Kitchen',
            'category': 'Cleaning',
            'task_type': 'daily',
            'effort_type': 'physical',
            'location_type': 'indoor',
            'base_xp_low': 15,
            'base_xp_medium': 30,
            'base_xp_high': 50,
            'subtasks': [
                ('Load dirty dishes into dishwasher', 1),
                ('Wipe down main counter', 1),
                ('Take out trash', 1),
                ('Wipe stove top', 2),
                ('Quick sweep floor', 2),
                ('Wipe all counters and backsplash', 3),
                ('Unload clean dishwasher', 3),
                ('Scrub sink thoroughly', 3),
                ('Mop floor', 3),
            ]
        },
        
        # Self Care - Morning Routine
        {
            'title': 'Morning Self-Care Routine',
            'category': 'Self Care',
            'task_type': 'daily',
            'effort_type': 'physical',
            'location_type': 'indoor',
            'base_xp_low': 10,
            'base_xp_medium': 20,
            'base_xp_high': 30,
            'subtasks': [
                ('Brush teeth', 1),
                ('Take medications', 1),
                ('Splash water on face', 1),
                ('Wash face properly', 2),
                ('Change into clean clothes', 2),
                ('Moisturize face', 2),
                ('Take a full shower', 3),
                ('Style hair', 3),
                ('Put on outfit (not just any clothes)', 3),
            ]
        },
        
        # Doby Care
        {
            'title': 'Doby Care Routine',
            'category': 'Doby',
            'task_type': 'weekly',
            'effort_type': 'physical',
            'location_type': 'indoor',
            'base_xp_low': 12,
            'base_xp_medium': 25,
            'base_xp_high': 45,
            'subtasks': [
                ('Quick brush', 1),
                ('Fill water bowl', 1),
                ('Thorough brushing', 2),
                ('Check and trim nails if needed', 2),
                ('Give bath with proper shampoo', 3),
                ('Clean ears', 3),
                ('Brush teeth', 3),
                ('Check for fleas/ticks', 3),
            ]
        },
        
        # Work - Email Management
        {
            'title': 'Process Work Emails',
            'category': 'Work',
            'task_type': 'daily',
            'effort_type': 'mental',
            'location_type': 'any',
            'base_xp_low': 10,
            'base_xp_medium': 20,
            'base_xp_high': 35,
            'subtasks': [
                ('Check for urgent emails', 1),
                ('Reply to 1-2 most urgent', 1),
                ('Scan through inbox', 2),
                ('Reply to priority emails', 2),
                ('Flag emails for later', 2),
                ('Reply to all emails needing response', 3),
                ('Organize inbox with filters/folders', 3),
                ('Clear out old emails', 3),
            ]
        },
        
        # Cleaning - Bedroom
        {
            'title': 'Tidy Bedroom',
            'category': 'Cleaning',
            'task_type': 'weekly',
            'effort_type': 'physical',
            'location_type': 'indoor',
            'base_xp_low': 12,
            'base_xp_medium': 25,
            'base_xp_high': 40,
            'subtasks': [
                ('Make the bed', 1),
                ('Pick up clothes from floor', 1),
                ('Put away items on nightstand', 2),
                ('Vacuum or sweep floor', 2),
                ('Dust surfaces', 2),
                ('Change bedsheets', 3),
                ('Organize closet', 3),
                ('Clean under bed', 3),
            ]
        },
        
        # Errands - Grocery Shopping
        {
            'title': 'Grocery Shopping',
            'category': 'Errands',
            'task_type': 'weekly',
            'effort_type': 'physical',
            'location_type': 'outdoor',
            'base_xp_low': 15,
            'base_xp_medium': 30,
            'base_xp_high': 45,
            'subtasks': [
                ('Grab milk, bread, and essentials', 1),
                ('Quick checkout', 1),
                ('Check what you need at home first', 2),
                ('Make a basic list', 2),
                ('Shop for items on list', 2),
                ('Plan meals for the week', 3),
                ('Make detailed list organized by store sections', 3),
                ('Shop deliberately with list', 3),
                ('Put everything away properly at home', 3),
            ]
        },
        
        # Social
        {
            'title': 'Connect with Friends/Family',
            'category': 'Social',
            'task_type': 'weekly',
            'effort_type': 'mental',
            'location_type': 'any',
            'base_xp_low': 12,
            'base_xp_medium': 25,
            'base_xp_high': 40,
            'subtasks': [
                ('Send a text to check in', 1),
                ('Reply to messages', 1),
                ('Have a phone call or voice chat', 2),
                ('Have a real conversation (15+ min)', 2),
                ('Make plans to meet up', 3),
                ('Video call or meet in person', 3),
                ('Do an activity together', 3),
            ]
        },
        
        # Coding Project
        {
            'title': 'Work on Coding Project',
            'category': 'Coding / Personal Projects',
            'task_type': 'weekly',
            'effort_type': 'mental',
            'location_type': 'indoor',
            'base_xp_low': 15,
            'base_xp_medium': 30,
            'base_xp_high': 55,
            'subtasks': [
                ('Open project and review code', 1),
                ('Fix one small bug', 1),
                ('Plan next feature or improvement', 2),
                ('Write some code (30+ min)', 2),
                ('Test changes', 2),
                ('Complete a full feature', 3),
                ('Write tests for new code', 3),
                ('Update documentation', 3),
                ('Commit and push changes', 3),
            ]
        },
        
        # Self Care - Exercise
        {
            'title': 'Exercise/Movement',
            'category': 'Self Care',
            'task_type': 'daily',
            'effort_type': 'physical',
            'location_type': 'any',
            'base_xp_low': 10,
            'base_xp_medium': 25,
            'base_xp_high': 40,
            'subtasks': [
                ('Do some stretches (5 min)', 1),
                ('Take a short walk (10 min)', 1),
                ('Do a quick workout (15-20 min)', 2),
                ('Go for a longer walk (20-30 min)', 2),
                ('Full workout at gym or home (30+ min)', 3),
                ('Include warmup and cooldown', 3),
                ('Try a new exercise or class', 3),
            ]
        },
        
        # Adulting
        {
            'title': 'Handle Important Paperwork/Admin',
            'category': 'Adulting',
            'task_type': 'weekly',
            'effort_type': 'mental',
            'location_type': 'any',
            'base_xp_low': 10,
            'base_xp_medium': 25,
            'base_xp_high': 45,
            'subtasks': [
                ('Open the mail/emails', 1),
                ('Read through what needs attention', 1),
                ('Make one important phone call', 2),
                ('Fill out one form or document', 2),
                ('Complete all pending forms', 3),
                ('Make all necessary calls', 3),
                ('Scan and file documents properly', 3),
                ('Update tracking spreadsheet', 3),
            ]
        },
    ]
    
    print("Creating sample templates...")
    
    for template_data in templates_data:
        # Create template
        template = TaskTemplate(
            title=template_data['title'],
            category=template_data['category'],
            task_type=template_data['task_type'],
            effort_type=template_data.get('effort_type'),
            location_type=template_data.get('location_type'),
            base_xp_low=template_data['base_xp_low'],
            base_xp_medium=template_data['base_xp_medium'],
            base_xp_high=template_data['base_xp_high']
        )
        
        db.session.add(template)
        db.session.flush()  # Get template ID
        
        # Add subtasks
        for order, (description, level) in enumerate(template_data['subtasks']):
            subtask = SubTask(
                template_id=template.id,
                description=description,
                level=level,
                order=order
            )
            db.session.add(subtask)
        
        print(f"  ✓ Created: {template.title} ({len(template_data['subtasks'])} subtasks)")
    
    db.session.commit()
    
    print(f"\n✅ Successfully created {len(templates_data)} templates!")
    print("\nTemplates by category:")
    categories = {}
    for t in templates_data:
        cat = t['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in sorted(categories.items()):
        print(f"   {cat}: {count} templates")


if __name__ == '__main__':
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Populate templates
        populate_sample_templates()
        
        print("\n🗡️ Conquer is ready! Run 'python app.py' to start.")