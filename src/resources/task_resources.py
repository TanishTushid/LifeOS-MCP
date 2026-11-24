

from fastmcp import FastMCP
from src.database.db import get_connection


def register_task_resources(mcp: FastMCP):

    @mcp.resource("lifeos://tasks")
    def get_all_tasks() -> list[dict]:
        """Retrieve all tasks stored in LifeOS."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM tasks
                ORDER BY id DESC
            """)

            return [dict(row) for row in cursor.fetchall()]

        finally:
            conn.close()

    @mcp.resource("lifeos://tasks/pending")
    def get_pending_tasks() -> list[dict]:
        """Retrieve all pending tasks."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM tasks
                WHERE status = 'pending'
                ORDER BY id DESC
            """)

            return [dict(row) for row in cursor.fetchall()]

        finally:
            conn.close()

    @mcp.resource("lifeos://tasks/completed")
    def get_completed_tasks() -> list[dict]:
        """Retrieve all completed tasks."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM tasks
                WHERE status = 'completed'
                ORDER BY id DESC
            """)

            return [dict(row) for row in cursor.fetchall()]

        finally:
            conn.close()
