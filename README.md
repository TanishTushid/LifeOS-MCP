# LifeOS

LifeOS is a personal assistant server built with FastMCP. It provides tools and
resources for managing tasks, notes, reminders, and productivity.

## Requirements

- Python 3.14+
- FastMCP

## Run

Create a virtual environment and install dependencies:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

The SQLite database is stored at `data/lifeos.db` and is initialized
automatically when the server starts.

## Features

- Task creation, updates, completion, deletion, and status filtering
- Note creation, updates, search, category resources, and deletion
- Reminder creation, completion, filtering, and deletion
- Productivity summaries, overdue task reports, and completion rates
- MCP prompts for planning, weekly reviews, prioritization, and learning