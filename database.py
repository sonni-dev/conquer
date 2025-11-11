import sqlite3
from datetime import datetime, timedelta
from contextlib import contextmanager


DATABASE = 'conquer.db'

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
        
        # Tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                task_type TEXT NOT NULL,
                points INTEGER NOT NULL,
                effort_type TEXT,
                location_type TEXT,
                energy_level TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Task completions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                completed_at TEXT DEFAULT CURRENT_TIMESTAMP,
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


def complete_task(task_id, points):
    """Mark task as complete and update user progress"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Record completion
        cursor.execute('''
            INSERT INTO task_completions (task_id, points_earned)
            VALUES (?, ?)
        ''', (task_id, points))
        
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