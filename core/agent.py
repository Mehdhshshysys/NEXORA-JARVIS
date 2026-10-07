from core.tool_manager import ToolManager


class Agent:

    def __init__(self, brain, tool_manager):
        self.brain = brain
        self.tool_manager = tool_manager

    def execute(self, command):

        decision = self.brain.understand(command)

        tool = decision.get("tool")
        action = decision.get("action")
        query = decision.get("query", "")

        if tool == "unknown":
            return "دستور را متوجه نشدم."

        if action == "exit":
            return "EXIT"

        if query:
            return self.tool_manager.run(
                tool,
                action,
                query
            )

        return self.tool_manager.run(
            tool,
            action
        )
