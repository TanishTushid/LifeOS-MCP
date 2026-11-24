
from fastmcp import FastMCP

from src.database.db import get_connection


def register_notes_tools(mcp: FastMCP):

    @mcp.tool()
    def create_note(
        title: str,
        content: str,
        category: str = "general"
    ) -> dict:
        """Create and save a new personal note."""

        if not title.strip():
            return {
                "success": False,
                "message": "Note title cannot be empty"
            }

        if not content.strip():
            return {
                "success": False,
                "message": "Note content cannot be empty"
            }

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO notes (title, content, category)
                VALUES (?, ?, ?)
                """,
                (title.strip(), content.strip(), category.strip() or "general")
            )

            note_id = cursor.lastrowid
            conn.commit()

            return {
                "success": True,
                "message": "Note created successfully",
                "note_id": note_id,
                "title": title
            }

        finally:
            conn.close()

    @mcp.tool()
    def get_notes() -> dict:
        """Retrieve all saved notes."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM notes ORDER BY created_at DESC"
            )

            notes = [dict(row) for row in cursor.fetchall()]

            return {
                "success": True,
                "count": len(notes),
                "notes": notes
            }

        finally:
            conn.close()

    @mcp.tool()
    def search_notes(query: str) -> dict:
        """Search notes by title, content or category."""

        if not query.strip():
            return {
                "success": False,
                "message": "Search query cannot be empty"
            }

        conn = get_connection()

        try:
            cursor = conn.cursor()

            search_term = f"%{query.strip()}%"

            cursor.execute(
                """
                SELECT * FROM notes
                WHERE title LIKE ?
                   OR content LIKE ?
                   OR category LIKE ?
                ORDER BY created_at DESC
                """,
                (search_term, search_term, search_term)
            )

            notes = [dict(row) for row in cursor.fetchall()]

            return {
                "success": True,
                "count": len(notes),
                "notes": notes
            }

        finally:
            conn.close()

    @mcp.tool()
    def update_note(
        note_id: int,
        title: str,
        content: str,
        category: str = "general"
    ) -> dict:
        """Update an existing note using its ID."""

        if not title.strip() or not content.strip():
            return {
                "success": False,
                "message": "Title and content cannot be empty"
            }

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE notes
                SET title = ?,
                    content = ?,
                    category = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    title.strip(),
                    content.strip(),
                    category.strip() or "general",
                    note_id
                )
            )

            conn.commit()

            if cursor.rowcount == 0:
                return {
                    "success": False,
                    "message": "Note not found"
                }

            return {
                "success": True,
                "message": "Note updated successfully",
                "note_id": note_id
            }

        finally:
            conn.close()

    @mcp.tool()
    def delete_note(note_id: int) -> dict:
        """Delete a saved note using its ID."""

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM notes WHERE id = ?",
                (note_id,)
            )

            conn.commit()

            if cursor.rowcount == 0:
                return {
                    "success": False,
                    "message": "Note not found"
                }

            return {
                "success": True,
                "message": "Note deleted successfully",
                "note_id": note_id
            }

        finally:
            conn.close()
