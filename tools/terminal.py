import subprocess


class TerminalTool:

    def run(self, command):

        if not command:
            return "هیچ دستوری وارد نشده است."

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
