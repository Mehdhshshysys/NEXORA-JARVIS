class Brain:

    def understand(self, command):

        command = command.lower().strip()

        # YouTube
        if "یوتیوب" in command:
            return {
                "tool": "browser",
                "action": "youtube",
                "query": command
            }

        # Google
        if "گوگل" in command or "جستجو" in command:
            return {
                "tool": "browser",
                "action": "google",
                "query": command
            }

        # Open website
        if "باز کن" in command and "سایت" in command:
            return {
                "tool": "browser",
                "action": "open_site",
                "query": command
            }

        # Time
        if "ساعت" in command:
            return {
                "tool": "system",
                "action": "time"
            }

        # System information
        if "سیستم" in command or "مشخصات کامپیوتر" in command:
            return {
                "tool": "system",
                "action": "info"
            }

        # Exit
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
