# 🗡️ Conquer - ADHD-Friendly Task Gamification

An intelligent task management system designed for ADHD/depression brains. Instead of rigid "complete or fail" tasks, Conquer uses **tiered templates** with **checkable subtasks** that adapt to your energy level.

## 🎯 Core Concept

### The Problem with Traditional To-Do Lists
- Binary completion (done or not done)
- Same expectations regardless of energy
- No dopamine hits for partial progress
- All-or-nothing thinking leads to guilt

### How Conquer Solves This

**Task Templates**: Define a task once with all possible subtasks  
**Tiered Subtasks**: Each subtask has a level (1, 2, or 3)  
**Energy-Based Selection**: Choose your energy when starting a task  
**Cumulative System**: 
- 🌙 Low energy = Level 1 subtasks only
- ⚡ Medium energy = Level 1 + 2 subtasks  
- 🔥 High energy = All subtasks (1 + 2 + 3)

**Checkboxes for Dopamine**: Check off each subtask as you go!

### Example: Clean the Kitchen

**Level 1 Subtasks** (Low Energy - bare minimum):
- ☐ Load dirty dishes into dishwasher
- ☐ Wipe down main counter
- ☐ Take out trash

**Level 2 Subtasks** (Medium Energy - adds to Level 1):
- ☐ Wipe stove top
- ☐ Quick sweep floor

**Level 3 Subtasks** (High Energy - adds to Levels 1 & 2):
- ☐ Wipe all counters and backsplash
- ☐ Unload clean dishwasher  
- ☐ Scrub sink thoroughly
- ☐ Mop floor

If you pick **Low Energy**, you only see the 3 Level 1 tasks. Check them off, complete the task, earn XP, maintain your streak - done!

If you finish and feel good? **Upgrade to Medium** and get 2 more subtasks added to your list!

## ✨ Features

- **Template System**: Create reusable task templates
- **Tiered Subtasks**: Different completions based on energy
- **Checkbox Dopamine**: Instant gratification per subtask
- **Mid-Task Upgrades**: Finish early? Add more!
- **Level & XP**: Gamified progression
- **Streak Tracking**: Daily completion (any tier counts!)
- **Category Balance**: See which life areas need attention
- **Flexible Completion**: 50% minimum, bonus XP per subtask

## 🚀 Quick Start

```bash
# Install dependencies
pip install flask flask-sqlalchemy --break-system-packages

# Setup database with sample templates
python populate_sample_data.py

# Run the app
python app.py

# Open browser to http://localhost:5000
```

## 📖 Complete documentation in README.md

This system is built on the understanding that **ADHD and depression make tasks feel different on different days**. The same task can feel insurmountable one day and manageable the next.

**There are multiple valid ways to complete a task. Pick the one that matches your current capacity. You still get credit. You still make progress. You still matter.**

---

🗡️ **Ready to Conquer?** Start the app and check those boxes!