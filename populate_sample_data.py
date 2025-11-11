from database import init_db, add_task

def populate_sample_tasks():
    """Add tiered sample tasks across all categories"""
    
    sample_tasks = [
        # Work
        {
            'title': 'Check and respond to emails',
            'task_type': 'daily',
            'category': 'Work',
            'high_description': 'Check all emails, respond to everything, organize inbox, file away completed threads, set up filters',
            'high_points': 30,
            'medium_description': 'Check emails, respond to urgent ones, flag others for later',
            'medium_points': 20,
            'low_description': 'Check for urgent emails only, send quick replies',
            'low_points': 10,
            'effort_type': 'mental',
            'location_type': 'any'
        },
        
        # Coding / Personal Projects
        {
            'title': 'Work on coding project',
            'task_type': 'weekly',
            'category': 'Coding / Personal Projects',
            'high_description': 'Complete a full feature or significant refactor, write tests, update documentation',
            'high_points': 50,
            'medium_description': 'Make progress on current feature, commit changes',
            'medium_points': 30,
            'low_description': 'Review code, fix one small bug, or plan next steps',
            'low_points': 15,
            'effort_type': 'mental',
            'location_type': 'indoor'
        },
        
        # Cleaning - Kitchen
        {
            'title': 'Clean the kitchen',
            'task_type': 'daily',
            'category': 'Cleaning',
            'high_description': 'Load & unload dishwasher, wipe all counters & backsplash, clean stove top & knobs, scrub sink, take out trash & recycling, sweep & mop floor',
            'high_points': 50,
            'medium_description': 'Load dishwasher, wipe main counters, clean stove, take out trash, quick sweep',
            'medium_points': 30,
            'low_description': 'Load dirty dishes into dishwasher (sink clear), wipe main counter, take out trash',
            'low_points': 15,
            'effort_type': 'physical',
            'location_type': 'indoor'
        },
        
        # Cleaning - General
        {
            'title': 'Tidy living space',
            'task_type': 'weekly',
            'category': 'Cleaning',
            'high_description': 'Pick up everything, vacuum all rooms, dust all surfaces, clean mirrors, organize clutter into proper places',
            'high_points': 45,
            'medium_description': 'Pick up main areas, vacuum high-traffic areas, quick dust',
            'medium_points': 25,
            'low_description': 'Pick up visible clutter, quick vacuum one room',
            'low_points': 12,
            'effort_type': 'physical',
            'location_type': 'indoor'
        },
        
        # Adulting
        {
            'title': 'Handle important paperwork',
            'task_type': 'weekly',
            'category': 'Adulting',
            'high_description': 'Complete forms, make necessary calls, scan & file documents, follow up on pending items, update tracking spreadsheet',
            'high_points': 40,
            'medium_description': 'Complete the most urgent task, make one important call',
            'medium_points': 25,
            'low_description': 'Open the paperwork, read through what needs to be done, gather necessary info',
            'low_points': 10,
            'effort_type': 'mental',
            'location_type': 'any'
        },
        
        # Doby (Pet Care)
        {
            'title': 'Doby care routine',
            'task_type': 'daily',
            'category': 'Doby',
            'high_description': 'Bath with proper shampoo, brush thoroughly, trim nails, clean teeth, check ears, treat for fleas if needed',
            'high_points': 45,
            'medium_description': 'Quick brush, check nails, clean teeth',
            'medium_points': 25,
            'low_description': 'Quick brush or pets and belly rubs',
            'low_points': 10,
            'effort_type': 'physical',
            'location_type': 'indoor'
        },
        
        {
            'title': 'Walk Doby',
            'task_type': 'daily',
            'category': 'Doby',
            'high_description': '30+ minute walk, explore new areas, practice training commands, play fetch',
            'high_points': 35,
            'medium_description': '20 minute walk around neighborhood',
            'medium_points': 20,
            'low_description': 'Quick 10 minute potty break outside',
            'low_points': 10,
            'effort_type': 'physical',
            'location_type': 'outdoor'
        },
        
        # Social
        {
            'title': 'Connect with friends/family',
            'task_type': 'weekly',
            'category': 'Social',
            'high_description': 'Have a video call or in-person meetup, have real conversation for 30+ minutes',
            'high_points': 40,
            'medium_description': 'Have a phone call, text conversation, or voice message exchange',
            'medium_points': 25,
            'low_description': 'Send a text to check in or reply to messages',
            'low_points': 12,
            'effort_type': 'mental',
            'location_type': 'any'
        },
        
        # Errands
        {
            'title': 'Grocery shopping',
            'task_type': 'weekly',
            'category': 'Errands',
            'high_description': 'Make meal plan, create detailed list, shop for full week, put everything away properly',
            'high_points': 40,
            'medium_description': 'Shop from existing list, get essentials, put most things away',
            'medium_points': 25,
            'low_description': 'Grab the absolute essentials (milk, bread, etc), quick trip',
            'low_points': 15,
            'effort_type': 'physical',
            'location_type': 'outdoor'
        },
        
        # Self Care
        {
            'title': 'Morning self-care routine',
            'task_type': 'daily',
            'category': 'Self Care',
            'high_description': 'Shower, wash face, brush teeth, take meds, moisturize, get dressed in real clothes',
            'high_points': 30,
            'medium_description': 'Wash face, brush teeth, take meds, change into clean clothes',
            'medium_points': 20,
            'low_description': 'Brush teeth, take meds',
            'low_points': 10,
            'effort_type': 'physical',
            'location_type': 'indoor'
        },
        
        {
            'title': 'Drink water throughout day',
            'task_type': 'daily',
            'category': 'Self Care',
            'high_description': 'Drink 8+ glasses of water, track intake, drink consistently throughout the day',
            'high_points': 20,
            'medium_description': 'Drink 5-6 glasses of water',
            'medium_points': 15,
            'low_description': 'Drink at least 3 glasses of water',
            'low_points': 10,
            'effort_type': 'physical',
            'location_type': 'any'
        },
        
        {
            'title': 'Exercise/Movement',
            'task_type': 'daily',
            'category': 'Self Care',
            'high_description': '30+ minute workout at gym or full home routine with warmup and cooldown',
            'high_points': 40,
            'medium_description': '15-20 minute workout, walk, or yoga session',
            'medium_points': 25,
            'low_description': '10 minute walk or simple stretching',
            'low_points': 12,
            'effort_type': 'physical',
            'location_type': 'any'
        },
        
        # Bonus tasks
        {
            'title': 'Meal prep for the week',
            'task_type': 'bonus',
            'category': 'Self Care',
            'high_description': 'Plan full week of meals, shop for ingredients, prep and portion all meals, clean up kitchen',
            'high_points': 60,
            'medium_description': 'Prep 3-4 meals, simple recipes, some portioning',
            'medium_points': 35,
            'low_description': 'Prep 1-2 simple meals or snacks',
            'low_points': 20,
            'effort_type': 'physical',
            'location_type': 'indoor'
        },
        
        {
            'title': 'Practice hobby or learning',
            'task_type': 'bonus',
            'category': 'Coding / Personal Projects',
            'high_description': 'Dedicate 2+ hours to learning something new, complete tutorials, practice deliberately',
            'high_points': 50,
            'medium_description': 'Spend 30-60 minutes on hobby or skill development',
            'medium_points': 30,
            'low_description': 'Watch a tutorial or read about something interesting for 15 minutes',
            'low_points': 15,
            'effort_type': 'mental',
            'location_type': 'any'
        }
    ]
    
    # Add all tasks
    for task in sample_tasks:
        add_task(
            title=task['title'],
            task_type=task['task_type'],
            category=task['category'],
            high_description=task['high_description'],
            high_points=task['high_points'],
            medium_description=task['medium_description'],
            medium_points=task['medium_points'],
            low_description=task['low_description'],
            low_points=task['low_points'],
            effort_type=task.get('effort_type'),
            location_type=task.get('location_type')
        )
    
    print(f"✅ Added {len(sample_tasks)} tiered sample tasks!")
    print("\nTasks by category:")
    categories = {}
    for task in sample_tasks:
        cat = task['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in sorted(categories.items()):
        print(f"   {cat}: {count} tasks")

if __name__ == '__main__':
    init_db()
    populate_sample_tasks()