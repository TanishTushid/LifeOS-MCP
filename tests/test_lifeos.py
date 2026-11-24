import asyncio
import tempfile
import unittest
from pathlib import Path
from typing import Any

import main
from src.database import db


class LifeOSSmokeTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db.DB_PATH = Path(self.temp_dir.name) / "lifeos.db"
        db.initialize_db()

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_async(self, operation):
        return asyncio.run(operation)

    def call_tool(self, name, arguments=None):
        return self.run_async(main.mcp.call_tool(name, arguments or {}))

    def tool_data(self, result: Any) -> dict[str, Any]:
        if result.structured_content is None:
            raise AssertionError("Tool result did not include structured content")
        return result.structured_content

    def test_task_lifecycle(self):
        created = self.call_tool("add_task", {
            "title": "Debug LifeOS",
            "description": "Run smoke tests",
            "due_date": "2026-11-24",
            "priority": "high",
        })
        self.assertTrue(self.tool_data(created)["success"])

        task_id = self.tool_data(created)["task_id"]
        completed = self.call_tool("complete_task", {"task_id": task_id})
        self.assertTrue(self.tool_data(completed)["success"])

        tasks = self.call_tool("get_tasks", {"status": "completed"})
        self.assertEqual(self.tool_data(tasks)["count"], 1)

        deleted = self.call_tool("delete_task", {"task_id": task_id})
        self.assertTrue(self.tool_data(deleted)["success"])

    def test_note_lifecycle(self):
        created = self.call_tool("create_note", {
            "title": "Test note",
            "content": "Lifecycle content",
            "category": "testing",
        })
        self.assertTrue(self.tool_data(created)["success"])

        note_id = self.tool_data(created)["note_id"]
        found = self.call_tool("search_notes", {"query": "Lifecycle"})
        self.assertEqual(self.tool_data(found)["count"], 1)

        updated = self.call_tool("update_note", {
            "note_id": note_id,
            "title": "Updated note",
            "content": "Updated content",
            "category": "testing",
        })
        self.assertTrue(self.tool_data(updated)["success"])

        deleted = self.call_tool("delete_note", {"note_id": note_id})
        self.assertTrue(self.tool_data(deleted)["success"])

    def test_reminder_lifecycle(self):
        created = self.call_tool("create_reminder", {
            "title": "Test reminder",
            "remind_at": "2026-11-24T15:30:00",
            "description": "Smoke test",
        })
        self.assertTrue(self.tool_data(created)["success"])

        reminder_id = self.tool_data(created)["reminder_id"]
        completed = self.call_tool("complete_reminder", {
            "reminder_id": reminder_id,
        })
        self.assertTrue(self.tool_data(completed)["success"])

        reminders = self.call_tool("get_reminders", {"status": "completed"})
        self.assertEqual(self.tool_data(reminders)["count"], 1)

        deleted = self.call_tool("delete_reminder", {
            "reminder_id": reminder_id,
        })
        self.assertTrue(self.tool_data(deleted)["success"])

    def test_productivity_and_resources(self):
        created = self.call_tool("add_task", {
            "title": "Task",
            "priority": "medium",
        })
        task_id = self.tool_data(created)["task_id"]
        self.call_tool("complete_task", {"task_id": task_id})

        summary = self.call_tool("get_productivity_summary")
        summary_data = self.tool_data(summary)
        self.assertEqual(summary_data["total_tasks"], 1)
        self.assertEqual(summary_data["completed_tasks"], 1)
        self.assertEqual(summary_data["completion_rate"], 100.0)

        async def inspect_components():
            tools = await main.mcp.list_tools()
            resources = await main.mcp.list_resources()
            templates = await main.mcp.list_resource_templates()
            prompts = await main.mcp.list_prompts()
            return len(tools), len(resources), len(templates), len(prompts)

        counts = asyncio.run(inspect_components())
        self.assertEqual(counts, (19, 5, 1, 4))


if __name__ == "__main__":
    unittest.main()
