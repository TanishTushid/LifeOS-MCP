
from fastmcp import FastMCP


def register_assistant_prompts(mcp: FastMCP):

    @mcp.prompt()
    def daily_planning(
        goals: str = "Complete my important tasks"
    ) -> str:
        """Generate a personalized daily planning prompt."""

        return f"""
        You are LifeOS, an intelligent personal assistant.

        Help me plan my day effectively.

        My goals for today:
        {goals}

        Follow these instructions:

        1. Identify the most important goals.
        2. Break large goals into smaller tasks.
        3. Prioritize tasks based on importance.
        4. Suggest a realistic daily schedule.
        5. Include short breaks.
        6. Keep the plan achievable.

        Present the result in a clear structured format.
        """

    @mcp.prompt()
    def weekly_review(
        completed_tasks: str,
        pending_tasks: str
    ) -> str:
        """Review weekly productivity and identify improvements."""

        return f"""
        You are LifeOS, my productivity assistant.

        Analyze my weekly performance.

        Completed tasks:
        {completed_tasks}

        Pending tasks:
        {pending_tasks}

        Your responsibilities:

        1. Summarize my accomplishments.
        2. Identify unfinished tasks.
        3. Analyze possible productivity problems.
        4. Highlight areas where I performed well.
        5. Suggest improvements for next week.

        Be constructive and practical.
        """

    @mcp.prompt()
    def task_prioritization(
        tasks: str
    ) -> str:
        """Prioritize tasks based on importance and urgency."""

        return f"""
        You are LifeOS, an intelligent task management assistant.

        Analyze the following pending tasks:

        {tasks}

        Categorize them into:

        - High priority
        - Medium priority
        - Low priority

        Consider deadlines, importance and urgency.

        Explain why each task belongs in its category.
        Recommend which task I should start first.
        """

    @mcp.prompt()
    def learning_plan(
        subject: str,
        available_hours: int = 2,
        duration_days: int = 7
    ) -> str:
        """Create a structured learning schedule."""

        return f"""
        You are LifeOS, my personal learning assistant.

        Create a learning plan using these details:

        Subject: {subject}
        Available study hours per day: {available_hours}
        Duration: {duration_days} days

        Requirements:

        1. Divide the subject into logical topics.
        2. Create daily learning goals.
        3. Include practical exercises.
        4. Include revision sessions.
        5. Include a final assessment.

        Make the schedule realistic and achievable.
        """
