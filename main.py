from core.brain import Brain
from core.agent import Agent
from core.tool_manager import ToolManager

from tools.browser import BrowserTool
from tools.system import SystemTool


def main():

    print("================================")
    print("       NEXORA-JARVIS")
    print("       AI AGENT v0.2")
    print("================================")

    brain = Brain()

    browser = BrowserTool()
    system = SystemTool()

    tool_manager = ToolManager()

    tool_manager.register("browser", browser)
    tool_manager.register("system", system)

    agent = Agent(
        brain,
        tool_manager
    )

    while True:

        command = input("\nJARVIS > ")

        result = agent.execute(command)

        print("JARVIS:", result)

        if result == "EXIT":
            print("JARVIS shutting down...")
            break


if __name__ == "__main__":
    main()
