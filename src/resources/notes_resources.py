
from fastmcp import FastMCP
from src.database.db import get_connection


def register_notes_resources(mcp: FastMCP):

    @mcp.resource("lifeos://notes")
    def get_all_notes() -> list[dict]:
        """Retrieve all notes stored in LifeOS."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM notes
                ORDER BY created_at DESC
            """)

            return [dict(row) for row in cursor.fetchall()]

        finally:
            conn.close()

    @mcp.resource("lifeos://notes/recent")
    def get_recent_notes() -> list[dict]:
        """Retrieve recently updated notes."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM notes
                ORDER BY updated_at DESC
                LIMIT 10
            """)

            return [dict(row) for row in cursor.fetchall()]

        finally:
            conn.close()

    @mcp.resource("lifeos://notes/{category}")
    def get_notes_by_category(category: str) -> list[dict]:
        """Retrieve notes belonging to a specific category."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM notes
                WHERE category = ?
                ORDER BY created_at DESC
            """, (category,))

            return [dict(row) for row in cursor.fetchall()]

        finally:
            conn.close()
