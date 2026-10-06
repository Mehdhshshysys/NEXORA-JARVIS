from datetime import datetime
import platform


class SystemTool:

    def time(self):
        now = datetime.now()
        return f"الان ساعت {now.strftime('%H:%M:%S')} است."

    def info(self):
        return {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
