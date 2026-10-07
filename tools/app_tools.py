import subprocess
import platform


class AppsTool:

    ALLOWED_APPS = {
        "notepad": {
            "windows": ["notepad.exe"]
        },
        "calculator": {
            "windows": ["calc.exe"]
        }
    }

    def open_app(self, app_name):

        app_name = app_name.lower().strip()
        system = platform.system().lower()

        app = self.ALLOWED_APPS.get(app_name)

        if not app:
            return "این برنامه در فهرست برنامه‌های مجاز نیست."

        command = app.get(system)

        if not command:
            return "این برنامه برای سیستم‌عامل فعلی تعریف نشده است."

        try:
            subprocess.Popen(command)
            return f"{app_name} باز شد."

        except Exception as error:
            return f"خطا در باز کردن برنامه: {error}"
