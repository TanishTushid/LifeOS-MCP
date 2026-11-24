
from fastmcp import FastMCP

# Database
from src.database.db import initialize_db

# MCP Tools
from src.tools.task_tools import register_task_tools
from src.tools.reminder_tools import register_reminder_tools
from src.tools.notes_tools import register_notes_tools
from src.tools.productivity_tools import register_productivity_tools
from src.resources.task_resources import register_task_resources
from src.resources.notes_resources import register_notes_resources
from src.prompts.assistant_prompts import register_assistant_prompts

# Initialize MCP server
mcp = FastMCP(
    name="LifeOS",
    instructions="""
    LifeOS is an AI-powered personal assistant.

    You can help users:
    - Manage daily tasks
    - Create and organize notes
    - Manage reminders
    - Track productivity

    Always confirm successful operations and report errors clearly.
    """
)
''' Register MCP Tools'''
# Initialize database
initialize_db()
# Register MCP tools
register_task_tools(mcp)
# Reminder.py 
register_reminder_tools(mcp)
# Notes 
register_notes_tools(mcp)
# Productivity Summary
register_productivity_tools(mcp)

''' Register MCP Resources'''
register_notes_resources(mcp)
register_task_resources(mcp)

# Register MCP Prompts
register_assistant_prompts(mcp)

# Start MCP server
if __name__ == "__main__":
    mcp.run()
