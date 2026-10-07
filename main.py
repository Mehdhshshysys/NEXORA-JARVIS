from core.brain import Brain
from core.agent import Agent
from core.tool_manager import ToolManager
from core.config import APP_NAME, VERSION, EXIT_COMMANDS, MAX_COMMAND_LENGTH

from tools.browser import BrowserTool
from tools.system import SystemTool
from tools.files import FilesTool
from tools.terminal import TerminalTool

from memory.memory import Memory


def main():

    print("================================")
    print(f"       {APP_NAME}")
    print(f"       AI AGENT v{VERSION}")
    print("================================")

    # Core
    brain = Brain()
    tool_manager = ToolManager()
    memory = Memory()

    # Tools
    browser = BrowserTool()
    system = SystemTool()
    files = FilesTool()
    terminal = TerminalTool()

    # Register tools
    tool_manager.register("browser", browser)
    tool_manager.register("system", system)
    tool_manager.register("files", files)
    tool_manager.register("terminal", terminal)
    tool_manager.register("memory", memory)

    # Agent
    agent = Agent(
        brain,
        tool_manager
    )

    print("JARVIS: سیستم آماده است.")
    print("JARVIS: منتظر دستور شما هستم.")

    while True:

        command = input("\nJARVIS > ").strip()

        if not command:
            continue

        if len(command) > MAX_COMMAND_LENGTH:
            print("JARVIS: دستور بیش از حد طولانی است.")
            continue

        if command.lower() in EXIT_COMMANDS:
            print("JARVIS: در حال خاموش شدن...")
            break

        memory.remember("last_command", command)

        result = agent.execute(command)

        print("JARVIS:", result)


if __name__ == "__main__":
    main()
