class Agent:

    def __init__(self, brain, tool_manager):
        self.brain = brain
        self.tool_manager = tool_manager

    def execute(self, command):

        if not command:
            return "دستوری دریافت نشد."

        try:
            decision = self.brain.understand(command)

            tool = decision.get("tool")
            action = decision.get("action")
            query = decision.get("query")

            if tool == "unknown":
                return "دستور را متوجه نشدم."

            if action == "exit":
                return "EXIT"

            if query:
                result = self.tool_manager.run(
                    tool,
                    action,
                    query
                )
            else:
                result = self.tool_manager.run(
                    tool,
                    action
                )

            return self.format_response(result)

        except Exception as error:
            return f"خطا در اجرای دستور: {error}"

    def format_response(self, result):

        if result is None:
            return "عملیات انجام شد."

        if isinstance(result, dict):
            parts = []

            for key, value in result.items():
                parts.append(f"{key}: {value}")

            return "، ".join(parts)

        return str(result)
