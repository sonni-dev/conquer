import sqlite3
from datetime import datetime, timedelta
from contextlib import contextmanager


DATABASE = 'conquer.db'

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

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_db():
    """Initialize database w tables"""
    with get_db() as conn:
        cursor = conn.cursor()

        # User progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY,
                total_xp INTEGER DEFAULT 0,
                current_level INTEGER DEFAULT 1,
                tasks_completed INTEGER DEFAULT 0,
                current_streak INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                last_completion_date TEXT
            )
        ''')
        
        # Tasks table w tired completion
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                task_type TEXT NOT NULL,
                category TEXT,
                effort_type TEXT,
                location_type TEXT,
                
                high_description TEXT,
                high_points INTEGER NOT NULL,
                
                medium_description TEXT,
                medium_points INTEGER NOT NULL,
                
                low_description TEXT,
                low_points INTEGER NOT NULL,
                
                is_active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Task completions table - now tracks which tier was completed
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                completed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                tier_completed TEXT NOT NULL,
                points_earned INTEGER NOT NULL,
                FOREIGN KEY (task_id) REFERENCES tasks (id)
            )
        ''')
        
        # Weekly recurring tasks tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekly_completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                week_start TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                FOREIGN KEY (task_id) REFERENCES tasks (id)
            )
        ''')
        
        # Initialize user progress if not exists
        cursor.execute('SELECT COUNT(*) FROM user_progress')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO user_progress (total_xp, current_level, tasks_completed)
                VALUES (0, 1, 0)
            ''')


def get_user_progress():
    """Get current user progress"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_progress WHERE id = 1')
        return dict(cursor.fetchone())


def calculate_level(xp):
    """Calculate level based on XP (100 XP per level)"""
    return max(1, (xp // 100) + 1)


def xp_for_next_level(current_xp):
    """Calculate XP needed for next level"""
    current_level = calculate_level(current_xp)
    next_level_xp = current_level * 100
    return next_level_xp - current_xp


def complete_task(task_id, tier, points):
    """Mark task as complete with specified tier and update user progress"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Record completion w tier
        cursor.execute('''
            INSERT INTO task_completions (task_id, tier_completed, points_earned)
            VALUES (?, ?, ?)
        ''', (task_id, tier, points))
        
        # Update user progress
        cursor.execute('''
            UPDATE user_progress 
            SET total_xp = total_xp + ?,
                tasks_completed = tasks_completed + 1
            WHERE id = 1
        ''', (points,))
        
        # Update level if needed
        progress = get_user_progress()
        new_level = calculate_level(progress['total_xp'])
        if new_level > progress['current_level']:
            cursor.execute('''
                UPDATE user_progress 
                SET current_level = ?
                WHERE id = 1
            ''', (new_level,))
        
        # Update streak
        update_streak()


def update_streak():
    """Update completion streak"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Get last completion date
        cursor.execute('SELECT last_completion_date FROM user_progress WHERE id = 1')
        result = cursor.fetchone()
        last_date = result[0] if result[0] else None
        
        today = datetime.now().date()
        
        if last_date:
            last_date = datetime.fromisoformat(last_date).date()
            days_diff = (today - last_date).days
            
            if days_diff == 0:
                # Same day, don't update streak
                return
            elif days_diff == 1:
                # Consecutive day, increment streak
                cursor.execute('''
                    UPDATE user_progress 
                    SET current_streak = current_streak + 1,
                        last_completion_date = ?
                    WHERE id = 1
                ''', (today.isoformat(),))
                
                # Update longest streak if needed
                cursor.execute('''
                    UPDATE user_progress 
                    SET longest_streak = MAX(longest_streak, current_streak)
                    WHERE id = 1
                ''')
            else:
                # Streak broken, reset to 1
                cursor.execute('''
                    UPDATE user_progress 
                    SET current_streak = 1,
                        last_completion_date = ?
                    WHERE id = 1
                ''', (today.isoformat(),))
        else:
            # First completion ever
            cursor.execute('''
                UPDATE user_progress 
                SET current_streak = 1,
                    longest_streak = 1,
                    last_completion_date = ?
                WHERE id = 1
            ''', (today.isoformat(),))


def get_tasks(task_type=None, category=None, filters=None):
    """Get tasks, optionally filtered by type, category, and attributes"""
    with get_db() as conn:
        cursor = conn.cursor()

        query = 'SELECT * FROM tasks WHERE is_active = 1'
        params = []

        if task_type:
            query += ' AND task_type = ?'
            params.append(task_type)

        if category:
            query += ' AND category = ?'
            params.append(category)

        if filters:
            if filters.get('effort_type'):
                query += ' AND effort_type = ?'
                params.append(filters['effort_type'])
            if filters.get('location_type'):
                query += ' AND location_type = ?'
                params.append(filters['location_type'])
            # if filters.get('energy_level'):
            #     query += ' AND energy_level = ?'
            #     params.append(filters['energy_level'])
            
        query += ' ORDER BY high_points DESC'
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def get_task_by_id(task_id):
    """Get a single task by ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ? AND is_active = 1', (task_id,))
        result = cursor.fetchone()
        return dict(result) if result else None


def add_task(title, task_type, category, high_description, high_points,
             medium_description, medium_points, low_description, low_points,
             effort_type=None, location_type=None):
    """Add a new tiered task"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, task_type, category, 
                             high_description, high_points,
                             medium_description, medium_points,
                             low_description, low_points,
                             effort_type, location_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, task_type, category,
              high_description, high_points,
              medium_description, medium_points,
              low_description, low_points,
              effort_type, location_type))
        return cursor.lastrowid


def get_todays_completions():
    """Get tasks completed today with tier info"""
    with get_db() as conn:
        cursor = conn.cursor()
        today = datetime.now().date().isoformat()
        cursor.execute('''
            SELECT tc.*, t.title, t.category
            FROM task_completions tc
            JOIN tasks t ON tc.task_id = t.id
            WHERE DATE(tc.completed_at) = ?
            ORDER BY tc.completed_at DESC
        ''', (today,))
        return [dict(row) for row in cursor.fetchall()]


def get_weekly_stats():
    """Get stats for current week"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Get start of current week (Monday)
        today = datetime.now()
        week_start = (today - timedelta(days=today.weekday())).date()
        
        cursor.execute('''
            SELECT COUNT(*) as completions, SUM(points_earned) as points
            FROM task_completions
            WHERE DATE(completed_at) >= ?
        ''', (week_start.isoformat(),))
        
        return dict(cursor.fetchone())


def get_category_stats():
    """Get completion counts by category for current week"""
    with get_db() as conn:
        cursor = conn.cursor()

        # Get start of current week (Monday)
        today = datetime.now()
        week_start = (today - timedelta(days=today.weekday())).date()

        cursor.execute('''
            SELECT t.category, COUNT(*) as count
            FROM task_completions tc
            JOIN tasks t ON tc.task_id = t.id
            WHERE DATE(tc.completed_at) >= ? AND t.category IS NOT NULL
            GROUP BY t.category
        ''', (week_start.isoformat(),))
        
        results = {row['category']: row['count'] for row in cursor.fetchall()}

        # Ensure all categories are represented
        for category in CATEGORIES:
            if category not in results:
                results[category] = 0
        
        return results
