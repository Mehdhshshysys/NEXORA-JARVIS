import subprocess


class TerminalTool:

    def run(self, command):

        if not command:
            return "هیچ دستوری وارد نشده است."

        dangerous_words = [
            "rm ",
            "del ",
            "format ",
            "shutdown",
            "reboot",
            "poweroff",
            "mkfs",
            "diskpart"
        ]

        command_lower = command.lower()

        for word in dangerous_words:
            if word in command_lower:
                return "این دستور به دلیل مسائل امنیتی اجرا نشد."

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )

            output = result.stdout.strip()
            error = result.stderr.strip()

            if output:
                return output

            if error:
                return error

            return "دستور اجرا شد."

        except subprocess.TimeoutExpired:
            return "اجرای دستور بیش از حد طول کشید."

        except Exception as error:
            return f"خطا: {error}"
