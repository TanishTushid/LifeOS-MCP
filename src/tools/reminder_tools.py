
from fastmcp import FastMCP
from typing import Literal
from datetime import datetime

from src.database.db import get_connection


def register_reminder_tools(mcp: FastMCP):

    @mcp.tool()
    def create_reminder(
        title: str,
        remind_at: str,
        description: str = ""
    ) -> dict:
        """Create a reminder with a specific date and time.

        remind_at must use ISO 8601 format:
        YYYY-MM-DDTHH:MM:SS
        """

        if not title.strip():
            return {
                "success": False,
                "message": "Reminder title cannot be empty"
            }

        try:
            reminder_time = datetime.fromisoformat(remind_at)
        except ValueError:
            return {
                "success": False,
                "message": "Invalid date format. Use YYYY-MM-DDTHH:MM:SS"
            }

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO reminders
                (title, description, remind_at, status)
                VALUES (?, ?, ?, ?)
                """,
                (
                    title.strip(),
                    description,
                    reminder_time.isoformat(),
                    "pending"
                )
            )

            reminder_id = cursor.lastrowid
            conn.commit()

            return {
                "success": True,
                "message": "Reminder created successfully",
                "reminder_id": reminder_id,
                "title": title,
                "remind_at": reminder_time.isoformat()
            }

        finally:
            conn.close()

    @mcp.tool()
    def get_reminders(
        status: Literal["all", "pending", "completed"] = "all"
    ) -> dict:
        """Retrieve reminders filtered by status."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            if status == "all":
                cursor.execute(
                    "SELECT * FROM reminders ORDER BY remind_at ASC"
                )
            else:
                cursor.execute(
                    """
                    SELECT * FROM reminders
                    WHERE status = ?
                    ORDER BY remind_at ASC
                    """,
                    (status,)
                )

            reminders = [
                dict(row) for row in cursor.fetchall()
            ]

            return {
                "success": True,
                "count": len(reminders),
                "reminders": reminders
            }

        finally:
            conn.close()

    @mcp.tool()
    def complete_reminder(reminder_id: int) -> dict:
        """Mark a reminder as completed."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE reminders
                SET status = 'completed'
                WHERE id = ?
                """,
                (reminder_id,)
            )

            conn.commit()

            if cursor.rowcount == 0:
                return {
                    "success": False,
                    "message": "Reminder not found"
                }

            return {
                "success": True,
                "message": "Reminder completed successfully",
                "reminder_id": reminder_id
            }

        finally:
            conn.close()

    @mcp.tool()
    def delete_reminder(reminder_id: int) -> dict:
        """Delete a reminder using its ID."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM reminders WHERE id = ?",
                (reminder_id,)
            )

            conn.commit()

            if cursor.rowcount == 0:
                return {
                    "success": False,
                    "message": "Reminder not found"
                }

            return {
                "success": True,
                "message": "Reminder deleted successfully",
                "reminder_id": reminder_id
            }

        finally:
            conn.close()
