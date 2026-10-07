import subprocess
import platform


class VoiceTool:

    def __init__(self):
        self.system = platform.system().lower()

    def speak(self, text):
        if not text:
            return

        if self.system == "windows":
            try:
                escaped_text = str(text).replace("'", "''")

                command = (
                    "Add-Type -AssemblyName System.Speech; "
                    "$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                    f"$speak.Speak('{escaped_text}');"
                )

                subprocess.Popen(
                    [
                        "powershell",
                        "-NoProfile",
                        "-Command",
                        command
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

                return "صدا پخش شد."

            except Exception as error:
                return f"خطا در پخش صدا: {error}"

        return "سیستم‌عامل فعلی برای خروجی صوتی تعریف نشده است."

    def listen(self):
        if self.system != "windows":
            return "سیستم‌عامل فعلی برای دریافت صدا تعریف نشده است."

        try:
            command = """
Add-Type -AssemblyName System.Speech

$recognizer = New-Object System.Speech.Recognition.SpeechRecognitionEngine
$recognizer.SetInputToDefaultAudioDevice()

$grammar = New-Object System.Speech.Recognition.DictationGrammar
$recognizer.LoadGrammar($grammar)

$result = $recognizer.Recognize()

if ($result) {
    Write-Output $result.Text
}

$recognizer.Dispose()
"""

            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    command
                ],
                capture_output=True,
                text=True
            )

            text = result.stdout.strip()

            if text:
                return text

            return ""

        except Exception as error:
            return f"خطا در دریافت صدا: {error}"

    def say_ready(self):
        return self.speak("بله؟")

    def say_response(self, response):
        return self.speak(response)
