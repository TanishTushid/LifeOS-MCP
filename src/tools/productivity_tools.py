

from fastmcp import FastMCP
from datetime import date

from src.database.db import get_connection


def register_productivity_tools(mcp: FastMCP):

    @mcp.tool()
    def get_productivity_summary() -> dict:
        """Get an overview of task productivity."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    COUNT(*) AS total_tasks,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END)
                        AS completed_tasks,
                    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END)
                        AS pending_tasks
                FROM tasks
            """)

            result = cursor.fetchone()

            total = result["total_tasks"] or 0
            completed = result["completed_tasks"] or 0
            pending = result["pending_tasks"] or 0

            completion_rate = (
                round((completed / total) * 100, 2)
                if total > 0 else 0
            )

            return {
                "success": True,
                "total_tasks": total,
                "completed_tasks": completed,
                "pending_tasks": pending,
                "completion_rate": completion_rate
            }

        finally:
            conn.close()

    @mcp.tool()
    def get_completed_tasks() -> dict:
        """Retrieve all completed tasks."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM tasks
                WHERE status = 'completed'
                ORDER BY id DESC
            """)

            tasks = [dict(row) for row in cursor.fetchall()]

            return {
                "success": True,
                "count": len(tasks),
                "tasks": tasks
            }

        finally:
            conn.close()

    @mcp.tool()
    def get_pending_tasks() -> dict:
        """Retrieve all pending tasks."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM tasks
                WHERE status = 'pending'
                ORDER BY id DESC
            """)

            tasks = [dict(row) for row in cursor.fetchall()]

            return {
                "success": True,
                "count": len(tasks),
                "tasks": tasks
            }

        finally:
            conn.close()

    @mcp.tool()
    def get_overdue_tasks() -> dict:
        """Retrieve pending tasks whose due dates have passed."""

        today = date.today().isoformat()

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM tasks
                WHERE status = 'pending'
                AND due_date != ''
                AND date(due_date) < date(?)
                ORDER BY due_date ASC
            """, (today,))

            tasks = [dict(row) for row in cursor.fetchall()]

            return {
                "success": True,
                "count": len(tasks),
                "tasks": tasks
            }

        finally:
            conn.close()

    @mcp.tool()
    def get_completion_rate() -> dict:
        """Calculate the percentage of completed tasks."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    COUNT(*) AS total,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END)
                        AS completed
                FROM tasks
            """)

            result = cursor.fetchone()

            total = result["total"] or 0
            completed = result["completed"] or 0

            rate = (
                round((completed / total) * 100, 2)
                if total > 0 else 0
            )

            return {
                "success": True,
                "total_tasks": total,
                "completed_tasks": completed,
                "completion_rate": rate
            }

        finally:
            conn.close()
