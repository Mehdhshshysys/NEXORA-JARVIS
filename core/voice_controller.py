from core.config import MAX_COMMAND_LENGTH


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

        result = self.agent.execute(command)

        return result

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

        activated = self.wait_for_wake_word()

        if not activated:
            return True

        command = self.listen_command()

        if not command:
            self.voice.speak(
                "دستوری دریافت نکردم."
            )
            return True

        result = self.execute_command(
            command
        )

        if result == "EXIT":
            self.respond(result)
            return False

        self.respond(result)

        return True
