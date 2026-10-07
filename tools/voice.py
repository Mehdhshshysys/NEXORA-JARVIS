import subprocess
import platform


class VoiceTool:

    def __init__(self):
        self.system = platform.system().lower()

    def speak(self, text):
        if not text:
            return ""

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
            return ""

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

            return result.stdout.strip()

        except Exception:
            return ""

    def detect_wake_word(self, text):
        if not text:
            return False

        normalized = text.lower().strip()

        wake_words = [
            "nexora",
            "nexora jarvis",
            "نکسورا",
            "نکسورا جارویس"
        ]

        for wake_word in wake_words:
            if wake_word in normalized:
                return True

        return False

    def wait_for_wake_word(self):
        while True:

            heard = self.listen()

            if not heard:
                continue

            if self.detect_wake_word(heard):
                self.say_ready()
                return True

    def say_ready(self):
        return self.speak("بله؟")

    def say_response(self, response):
        return self.speak(response)
