class Brain:

    def understand(self, command):
        command = command.lower().strip()

        if "یوتیوب" in command:
            return {
                "tool": "browser",
                "action": "youtube",
                "query": command
            }

        if "گوگل" in command or "جستجو" in command:
            return {
                "tool": "browser",
                "action": "google",
                "query": command
            }

        if "ساعت" in command:
            return {
                "tool": "system",
                "action": "time"
            }

        if "سیستم" in command or "مشخصات کامپیوتر" in command:
            return {
                "tool": "system",
                "action": "info"
            }

        if command in ["خروج", "بستن", "exit", "quit"]:
            return {
                "tool": "system",
                "action": "exit"
            }

        return {
            "tool": "unknown",
            "action": "unknown",
            "query": command
          }
