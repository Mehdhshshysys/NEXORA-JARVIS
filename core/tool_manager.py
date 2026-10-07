class ToolManager:

    def __init__(self):
        self.tools = {}

    def register(self, name, tool):
        if not name:
            return False

        self.tools[name] = tool
        return True

    def get(self, name):
        return self.tools.get(name)

    def exists(self, name):
        return name in self.tools

    def list_tools(self):
        return list(self.tools.keys())

    def run(self, tool_name, action, *args, **kwargs):

        tool = self.get(tool_name)

        if tool is None:
            return f"ابزار '{tool_name}' پیدا نشد."

        method = getattr(tool, action, None)

        if method is None:
            return f"عملیات '{action}' در ابزار '{tool_name}' وجود ندارد."

        try:
            return method(*args, **kwargs)

        except Exception as error:
            return f"خطا در ابزار {tool_name}: {error}"
