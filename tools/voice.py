import subprocess
import platform

from core.voice_config import (
    WAKE_WORDS,
    READY_MESSAGE,
    VOICE_TIMEOUT
)


class VoiceTool:

    def __init__(self):
        self.system = platform.system().lower()

    def speak(self, text):

        if not text:
            return ""

        if self.system != "windows":
            return "سیستم‌عامل فعلی برای خروجی صوتی تعریف نشده است."

        try:
            escaped_text = str(text).replace("'", "''")

            command = (
                "Add-Type -AssemblyName System.Speech; "
                "$speak = New-Object "
                "System.Speech.Synthesis.SpeechSynthesizer; "
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

    def listen(self):

        if self.system != "windows":
            return ""

        try:

            command = f"""
Add-Type -AssemblyName System.Speech

$recognizer = New-Object System.Speech.Recognition.SpeechRecognitionEngine
$recognizer.SetInputToDefaultAudioDevice()

$grammar = New-Object System.Speech.Recognition.DictationGrammar
$recognizer.LoadGrammar($grammar)

$result = $recognizer.Recognize(
    [TimeSpan]::FromSeconds({VOICE_TIMEOUT})
)

if ($result) {{
    Write-Output $result.Text
}}

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

            return result.stdout.strip()

        except Exception:
            return ""

    def detect_wake_word(self, text):

        if not text:
            return False

        normalized = text.lower().strip()

        for wake_word in WAKE_WORDS:

            if wake_word.lower() in normalized:
                return True

        return False

    def wait_for_wake_word(self):

        while True:

            heard = self.listen()

            if not heard:
                continue

            if self.detect_wake_word(heard):

                self.speak(
                    READY_MESSAGE
                )

                return True

    def say_ready(self):

        return self.speak(
            READY_MESSAGE
        )

    def say_response(self, response):

        return self.speak(
            response
        )
