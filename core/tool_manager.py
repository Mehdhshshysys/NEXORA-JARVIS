class ToolManager:

    def __init__(self):
        self.tools = {}

    def register(self, name, tool):
        self.tools[name] = tool

    def get(self, name):
        return self.tools.get(name)

    def list_tools(self):
        return list(self.tools.keys())

    def run(self, tool_name, action, *args, **kwargs):

        tool = self.get(tool_name)

        if tool is None:
            return "ابزار موردنظر پیدا نشد."

        method = getattr(tool, action, None)

        if method is None:
            return f"عملیات {action} در ابزار {tool_name} وجود ندارد."

        return method(*args, **kwargs)
