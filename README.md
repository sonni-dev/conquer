# 🎮 Conquer v2.0 - Tiered Task System

A gamified task management system designed for ADHD/depression brains. Track your daily tasks, weekly goals, and bonus quests with THREE energy levels per task - because some days everything feels hard, and that's okay.

## ✨ Core Philosophy

**This system is built on the principle that completion at ANY level is progress.** The same task can feel completely different depending on your energy, mental state, or what else is going on. Instead of all-or-nothing thinking, you choose which version you completed:

- 🔥 **High Energy**: The full, thorough version (maximum XP)
- ⚡ **Medium Energy**: The realistic, broken-down version (medium XP)
- 🌙 **Low Energy**: The absolute minimum that still counts (lower XP, but still counts!)

All three versions earn XP, maintain your streak, and count toward your weekly goals. No guilt. No failure states. Just honest tracking of what you could do with what you had.

## 🎯 Features

### Tiered Task Completion
Every task has three versions defined. When you complete a task:
1. You see all three tiers with their descriptions
2. You pick which one matches what you actually did
3. You earn the appropriate XP
4. Your choice is tracked so you can see patterns

### Life Balance Categories
Tasks are organized into 8 life categories:
- **Work**: Professional responsibilities
- **Coding / Personal Projects**: Side projects and learning
- **Cleaning**: Home maintenance
- **Adulting**: Paperwork, bills, appointments
- **Doby**: Pet care (customize to your pet's name!)
- **Social**: Connections with friends and family
- **Errands**: Shopping, picking up items
- **Self Care**: Exercise, hygiene, health

The dashboard shows your weekly completion counts per category so you can see if you're neglecting any life areas.

### Progressive Systems
- **Level & XP**: Gain experience and level up (100 XP per level)
- **Streak Tracking**: Complete at least one task daily (any tier!) to maintain streaks
- **Visual Dashboard**: Progress bars, category balance, completion history

### Smart Quest Selection
Filter available tasks by:
- Your current energy level (high/medium/low)
- Effort type (physical/mental/creative)
- Location (indoor/outdoor/anywhere)
- Category (to focus on neglected areas)

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

### Quick Start Scripts
- **Mac/Linux**: `./start.sh`
- **Windows**: `start.bat`

## 📖 How to Use

### Creating Tasks

When adding a task, you define three versions:

**Example: Clean the Kitchen**
- 🔥 High: Load & unload dishwasher, wipe all counters, clean stove, scrub sink, take out trash, sweep & mop floor
- ⚡ Medium: Load dishwasher, wipe main counter, clean stove, take out trash
- 🌙 Low: Load dirty dishes (sink clear), wipe main counter, take out trash

**Point Values:**
- Think about effort, not time
- High: Usually 40-60 XP for thorough completion
- Medium: Usually 20-30 XP for realistic completion  
- Low: Usually 10-15 XP for minimum completion

### Completing Tasks

1. Click the ✓ button on any task
2. You'll see all three tier options with descriptions
3. Click the version that matches what you did
4. Earn XP based on your completion level
5. Build your streak (any completion counts!)

### Using the Dashboard

**Progress Section:**
- Current level and XP bar
- Daily streak (complete any task to maintain)
- Longest streak
- Total completions

**Life Balance:**
- Visual breakdown of tasks by category this week
- Quickly see which life areas need attention
- No judgment - just data

**Today's Completions:**
- See what you've already done today
- Track which tiers you've been completing
- Notice patterns in your energy levels

### Quest Selection

Use the Quest Select page to filter tasks by:
1. **Energy Level**: Match tasks to how you're feeling
2. **Category**: Focus on a specific life area
3. **Location/Effort**: Find tasks that fit your situation

Remember: Filtering by "high energy" doesn't mean you HAVE to do the high energy version. It just shows tasks that have challenging high-energy options available.

## 🧠 Design for ADHD/Depression

### Key Principles

**No All-or-Nothing Thinking:**
Traditional todo lists are binary: done or not done. This system acknowledges that "clean kitchen" can mean different things on different days. Both count.

**Celebrate Low Energy Wins:**
Loading the dishwasher when you're exhausted is an achievement. The system treats it as such with XP and streak credit.

**Track Patterns Without Judgment:**
Seeing that you completed mostly "low energy" versions this week isn't a failure - it's information. Maybe you need rest. Maybe something's off. The data helps you notice.

**Prevent Life Imbalance:**
The category tracker helps you see if you're avoiding certain areas (like maybe you did 10 work tasks but zero self-care). Again, no judgment - just awareness.

**Choose at Completion Time:**
Even if you filtered for "high energy" tasks, you can still pick the low energy version when completing. Because sometimes a task feels harder than expected, and that's real.

## 💡 Sample Tasks Included

The system comes with 14 sample tasks across all categories to help you understand how to structure yours:

- Work: Email management
- Coding: Project work
- Cleaning: Kitchen, living space
- Adulting: Paperwork
- Doby: Pet care routine, walks
- Social: Connecting with people
- Errands: Grocery shopping
- Self Care: Morning routine, hydration, exercise

These are meant to be examples. Delete them and add your real tasks!

## 🎯 Tips for Success

1. **Be Honest**: The system only helps if you track reality. If you did the low energy version, click that one.

2. **Define Realistic Tiers**: When creating tasks, make sure the low energy version is something you can ACTUALLY do on a bad day.

3. **Use Categories Strategically**: If you notice you haven't done any "Social" tasks this week, maybe pick one today.

4. **Celebrate All Wins**: 15 XP is still XP. A low energy completion still maintains your streak. It counts.

5. **Adjust Point Values**: If a task consistently feels harder than its XP suggests, adjust the points. This is your system.

6. **Track Energy Patterns**: If you're doing mostly low energy completions for weeks, that's your brain telling you something. Maybe you need rest, support, or to talk to someone.

## 🔧 Customization

### Changing Categories
Edit the `CATEGORIES` list in `database.py` to match your life:
```python
CATEGORIES = [
    'Your',
    'Custom',
    'Categories',
    'Here'
]
```

### Adjusting Level Requirements
Modify the `calculate_level()` function in `database.py`:
```python
def calculate_level(xp):
    return max(1, (xp // 100) + 1)  # Currently 100 XP per level
```

### Styling
Edit CSS variables in `static/css/style.css`:
```css
:root {
    --primary-color: #6366f1;  /* Main theme color */
    --tier-high: #ef4444;      /* High energy color */
    --tier-medium: #f59e0b;    /* Medium energy color */
    --tier-low: #6366f1;       /* Low energy color */
}
```

## 📁 Project Structure

```
conquer/
├── app.py                      # Flask application
├── database.py                 # Database models and functions
├── populate_sample_data.py     # Sample data script
├── templates/
│   ├── base.html              # Base template
│   ├── dashboard.html         # Main dashboard with categories
│   ├── quest_select.html      # Quest selection by energy
│   ├── task_detail.html       # Tier selection page
│   ├── add_task.html          # Create tiered tasks
│   └── tasks.html             # All tasks view
├── static/
│   ├── css/
│   │   └── style.css          # Styles with tier colors
│   └── js/
│       └── main.js            # JavaScript functions
└── conquer.db                 # SQLite database
```

## 🤔 FAQ

**Q: What if I do something between two tiers?**
A: Pick whichever feels closer. Or pick the lower tier - it still counts!

**Q: Can I complete the same task multiple times per day?**
A: Yes! Each completion earns XP. Good for tracking recurring things like "drink water."

**Q: What happens if I miss a day?**
A: Your streak resets to 1 on your next completion. That's okay! Streaks are motivating but shouldn't cause stress.

**Q: Should I always aim for high energy completions?**
A: No! The goal is sustainable progress. Some days low energy is all you've got, and that's exactly what that tier is for.

**Q: What if a task doesn't have clear tiers?**
A: Some tasks are binary. For these, you can make the three tiers more about "how thoroughly" rather than "what steps." Like "Text friend back" could be: High=thoughtful reply, Medium=short reply, Low=emoji reaction.

## 🔮 Future Enhancement Ideas

- Character/pet that grows with your level
- Weekly/monthly reports showing tier patterns
- Suggested tasks based on neglected categories
- Dark mode
- Desktop widget
- Mobile-responsive improvements
- Export/backup functionality
- Task templates
- Recurring task auto-reset
- Collaborative household tasks

## 📝 Philosophy

This tool is built on the understanding that ADHD and depression don't just make tasks harder - they make them feel different on different days. The same task can feel insurmountable one day and manageable the next. Traditional productivity systems don't account for this variability, leading to shame spirals when you can't meet the standard.

This system says: **There are multiple valid ways to complete a task. Pick the one that matches your current capacity. You still get credit. You still make progress. You still matter.**

---

**Ready to start your quest?** Run the app and take it one task, one tier, one day at a time. 🗡️✨