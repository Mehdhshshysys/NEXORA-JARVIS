from core.brain import Brain
from core.agent import Agent
from core.tool_manager import ToolManager
from core.config import (
    APP_NAME,
    VERSION,
    EXIT_COMMANDS,
    MAX_COMMAND_LENGTH,
    VOICE_ENABLED
)

from tools.browser import BrowserTool
from tools.system import SystemTool
from tools.files import FilesTool
from tools.terminal import TerminalTool
from tools.app_tools import AppsTool
from tools.voice import VoiceTool

from memory.memory import Memory


def build_agent():

    brain = Brain()
    tool_manager = ToolManager()
    memory = Memory()

    browser = BrowserTool()
    system = SystemTool()
    files = FilesTool()
    terminal = TerminalTool()
    apps = AppsTool()
    voice = VoiceTool()

    tool_manager.register("browser", browser)
    tool_manager.register("system", system)
    tool_manager.register("files", files)
    tool_manager.register("terminal", terminal)
    tool_manager.register("memory", memory)
    tool_manager.register("apps", apps)
    tool_manager.register("voice", voice)

    agent = Agent(
        brain,
        tool_manager
    )

    return agent, memory, voice


def text_mode(agent, memory, voice):

    print("JARVIS: حالت متنی فعال است.")

    while True:

        command = input("\nJARVIS > ").strip()

        if not command:
            continue

        if len(command) > MAX_COMMAND_LENGTH:
            print("JARVIS: دستور بیش از حد طولانی است.")
            continue

        if command.lower() in EXIT_COMMANDS:
            print("JARVIS: در حال خاموش شدن...")
            voice.speak("در حال خاموش شدن.")
            break

        memory.remember("last_command", command)

        result = agent.execute(command)

        print("JARVIS:", result)

        if result != "EXIT":
            voice.say_response(str(result))


def voice_mode(agent, memory, voice):

    print("JARVIS: حالت صوتی فعال است.")
    print("JARVIS: منتظر کلمه NEXORA هستم.")

    while True:

        activated = voice.wait_for_wake_word()

        if not activated:
            continue

        command = voice.listen()

        if not command:
            voice.speak("دستوری دریافت نکردم.")
            continue

        if len(command) > MAX_COMMAND_LENGTH:
            voice.speak("دستور بیش از حد طولانی است.")
            continue

        if command.lower() in EXIT_COMMANDS:
            voice.speak("در حال خاموش شدن.")
            break

        memory.remember("last_command", command)

        result = agent.execute(command)

        if result == "EXIT":
            voice.speak("در حال خاموش شدن.")
            break

        print("JARVIS:", result)

        voice.say_response(str(result))


def main():

    print("================================")
    print(f"       {APP_NAME}")
    print(f"       AI AGENT v{VERSION}")
    print("================================")

    agent, memory, voice = build_agent()

    print("JARVIS: سیستم آماده است.")

    if VOICE_ENABLED:
        voice_mode(
            agent,
            memory,
            voice
        )
    else:
        text_mode(
            agent,
            memory,
            voice
        )


if __name__ == "__main__":
    main()
