from core.brain import Brain
from core.agent import Agent
from core.tool_manager import ToolManager

from tools.browser import BrowserTool
from tools.system import SystemTool
from tools.files import FilesTool
from tools.terminal import TerminalTool

from memory.memory import Memory


def main():

    print("================================")
    print("       NEXORA-JARVIS")
    print("       AI AGENT v0.6")
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

        if command.lower() in ["خروج", "exit", "quit"]:
            print("JARVIS: در حال خاموش شدن...")
            break

        # Save last command
        memory.remember("last_command", command)

        # Execute command
        result = agent.execute(command)

        print("JARVIS:", result)


if __name__ == "__main__":
    main()
