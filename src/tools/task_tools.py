
from fastmcp import FastMCP
from typing import Literal
from src.database.db import get_connection


def register_task_tools(mcp: FastMCP):

    @mcp.tool()
    def add_task(
        title: str,
        description: str = "",
        due_date: str = "",
        priority: Literal["low", "medium", "high"] = "medium"
    ) -> dict:
        """Create a new task in LifeOS."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO tasks
                (title, description, due_date, priority, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (title, description, due_date, priority, "pending")
            )

            task_id = cursor.lastrowid
            conn.commit()

            return {
                "success": True,
                "message": "Task created successfully",
                "task_id": task_id,
                "title": title
            }

        finally:
            conn.close()

    @mcp.tool()
    def get_tasks(
        status: Literal["all", "pending", "completed"] = "all"
    ) -> dict:
        """Retrieve tasks filtered by their status."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            if status == "all":
                cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
            else:
                cursor.execute(
                    "SELECT * FROM tasks WHERE status = ? ORDER BY id DESC",
                    (status,)
                )

            tasks = [dict(row) for row in cursor.fetchall()]

            return {
                "success": True,
                "count": len(tasks),
                "tasks": tasks
            }

        finally:
            conn.close()

    @mcp.tool()
    def update_task(
        task_id: int,
        title: str,
        description: str = "",
        due_date: str = "",
        priority: Literal["low", "medium", "high"] = "medium"
    ) -> dict:
        """Update an existing task."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE tasks
                SET title = ?,
                    description = ?,
                    due_date = ?,
                    priority = ?
                WHERE id = ?
                """,
                (title, description, due_date, priority, task_id)
            )

            conn.commit()

            if cursor.rowcount == 0:
                return {
                    "success": False,
                    "message": "Task not found"
                }

            return {
                "success": True,
                "message": "Task updated successfully",
                "task_id": task_id
            }

        finally:
            conn.close()

    @mcp.tool()
    def delete_task(task_id: int) -> dict:
        """Delete a task using its ID."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM tasks WHERE id = ?",
                (task_id,)
            )

            conn.commit()

            if cursor.rowcount == 0:
                return {
                    "success": False,
                    "message": "Task not found"
                }

            return {
                "success": True,
                "message": "Task deleted successfully",
                "task_id": task_id
            }

        finally:
            conn.close()

    @mcp.tool()
    def complete_task(task_id: int) -> dict:
        """Mark a task as completed."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE tasks
                SET status = 'completed'
                WHERE id = ?
                """,
                (task_id,)
            )

            conn.commit()

            if cursor.rowcount == 0:
                return {
                    "success": False,
                    "message": "Task not found"
                }

            return {
                "success": True,
                "message": "Task completed successfully",
                "task_id": task_id
            }

        finally:
            conn.close()
