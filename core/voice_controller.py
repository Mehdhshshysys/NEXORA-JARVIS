from core.config import MAX_COMMAND_LENGTH
from core.voice_config import (
    NO_COMMAND_MESSAGE,
    ALWAYS_LISTENING,
    LISTEN_AFTER_WAKE
)


class VoiceController:

    def __init__(self, voice, agent, memory):
        self.voice = voice
        self.agent = agent
        self.memory = memory

    def wait_for_wake_word(self):
        return self.voice.wait_for_wake_word()

    def listen_command(self):

        command = self.voice.listen()

        if not command:
            self.voice.speak(
                NO_COMMAND_MESSAGE
            )
            return None

        command = command.strip()

        if len(command) > MAX_COMMAND_LENGTH:
            self.voice.speak(
                "دستور بیش از حد طولانی است."
            )
            return None

        return command

    def execute_command(self, command):

        if not command:
            return None

        self.memory.remember(
            "last_command",
            command
        )

        return self.agent.execute(
            command
        )

    def respond(self, result):

        if result is None:
            return

        if result == "EXIT":
            self.voice.speak(
                "در حال خاموش شدن."
            )
            return

        self.voice.say_response(
            str(result)
        )

    def run_once(self):

        if not ALWAYS_LISTENING:
            return False

        activated = self.wait_for_wake_word()

        if not activated:
            return True

        if not LISTEN_AFTER_WAKE:
            return True

        command = self.listen_command()

        if not command:
            return True

        result = self.execute_command(
            command
        )

        if result == "EXIT":
            self.respond(result)
            return False

        self.respond(result)

        return True
