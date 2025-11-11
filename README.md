# 🎮 Conquer

A gamified task management system that turns your to-do list into an adventure! Track your daily tasks, weekly goals, and bonus quests while leveling up and maintaining streaks.

## ✨ Features

- **Quest-based Tasks**: Three types of tasks - Daily, Weekly, and Bonus
- **Smart Quest Selection**: Filter tasks by your current state:
  - Energy level (High/Medium/Low)
  - Effort type (Physical/Mental/Creative)
  - Location (Indoor/Outdoor/Anywhere)
- **Level & XP System**: Gain experience points and level up
- **Streak Tracking**: Build and maintain daily completion streaks
- **Visual Progress**: Clean dashboard with progress bars and stats
- **Flexible**: Add custom tasks with your own point values

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- pip

### Installation

1. **Install Flask**:
   ```bash
   pip install flask --break-system-packages
   ```

2. **Initialize the database with sample data**:
   ```bash
   python populate_sample_data.py
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** to: `http://localhost:5000`

## 📖 How to Use

### Dashboard
- View your current level, XP progress, and streaks
- See today's completed tasks
- Quick access to different quest types
- Quick quest selection based on your mood

### Quest Select
- Filter quests based on how you're feeling
- Choose tasks that match your energy level
- Select indoor or outdoor activities
- Pick physical or mental challenges

### Add Tasks
- Create custom quests with:
  - Title and description
  - Task type (Daily/Weekly/Bonus)
  - Point value (XP reward)
  - Tags for filtering (effort, location, energy)

### Complete Tasks
- Click the ✓ button to mark tasks complete
- Earn XP and level up
- Build your daily streak

## 🎯 Task Types

- **📆 Daily**: Tasks you want to do every day
- **🔄 Weekly**: Tasks that need to be done once per week
- **⭐ Bonus**: Optional tasks for extra XP (low priority)

## 💡 Tips

- **Point Values**:
  - Easy tasks: 10-20 XP
  - Medium tasks: 25-35 XP
  - Hard tasks: 40-50+ XP
  
- **Maintaining Streaks**: Complete at least one task each day to keep your streak alive

- **Quest Selection**: Use the Quest Select page when you're not sure what to do - filter by your current mood and energy!

## 🔮 Future Enhancements (Optional)

- Character/pet that grows with your level
- Weekly/monthly reports and statistics
- Task templates and categories
- Dark mode
- Desktop widget or system tray integration
- Export progress data

## 📁 Project Structure

```
conquer/
├── app.py                      # Flask application
├── database.py                 # Database models and functions
├── populate_sample_data.py     # Sample data script
├── templates/
│   ├── base.html              # Base template
│   ├── dashboard.html         # Main dashboard
│   ├── quest_select.html      # Quest selection interface
│   ├── add_task.html          # Add new task form
│   └── tasks.html             # All tasks view
├── static/
│   ├── css/
│   │   └── style.css          # Styles
│   └── js/
│       └── main.js            # JavaScript functions
└── quest_tracker.db           # SQLite database (created on first run)
```

## 🛠️ Customization

- **Colors**: Edit CSS variables in `static/css/style.css`
- **XP per Level**: Modify the `calculate_level()` function in `database.py`
- **Task Categories**: Add new tags or categories in the database schema
- **Streak Rules**: Adjust streak calculation in `update_streak()` function

## 📝 Notes

- The database is stored locally in `conquer.db`
- All data persists between sessions
- To reset everything, simply delete `conquer.db` and run `populate_sample_data.py` again

---

**Ready to start your quest?** Run the app and turn your tasks into an adventure! 🗡️✨