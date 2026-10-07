from core.brain import Brain
from core.agent import Agent
from core.tool_manager import ToolManager

from tools.browser import BrowserTool
from tools.system import SystemTool
from tools.files import FilesTool

from memory.memory import Memory


def main():

    print("================================")
    print("       NEXORA-JARVIS")
    print("       AI AGENT v0.4")
    print("================================")

    brain = Brain()

    browser = BrowserTool()
    system = SystemTool()
    files = FilesTool()

    tool_manager = ToolManager()

    tool_manager.register("browser", browser)
    tool_manager.register("system", system)
    tool_manager.register("files", files)

    memory = Memory()

    agent = Agent(
        brain,
        tool_manager
    )

    print("JARVIS: سیستم آماده است.")

    while True:

        command = input("\nJARVIS > ")

        if command.lower() in ["خروج", "exit", "quit"]:
            print("JARVIS: در حال خاموش شدن...")
            break

        memory.remember("last_command", command)

        result = agent.execute(command)

        print("JARVIS:", result)


if __name__ == "__main__":
    main()
