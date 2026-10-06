from core.brain import Brain
from core.agent import Agent
from tools.browser import BrowserTool
from tools.system import SystemTool


def main():

    print("================================")
    print("       NEXORA-JARVIS")
    print("       AI AGENT v0.1")
    print("================================")

    brain = Brain()
    browser = BrowserTool()
    system = SystemTool()

    agent = Agent(
        brain,
        browser,
        system
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
