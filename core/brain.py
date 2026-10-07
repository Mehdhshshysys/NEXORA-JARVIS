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

        # Google / Search
        if "گوگل" in command or "جستجو" in command or "سرچ" in command:
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

        # Files
        if "فایل ها" in command or "فایل‌ها" in command:
            return {
                "tool": "files",
                "action": "list_files"
            }

        # Delete file
if "فایل حذف کن" in command or "فایل پاک کن" in command:
    return {
        "tool": "files",
        "action": "delete_file",
        "query": command
    }
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

        # Unknown command
        return {
            "tool": "unknown",
            "action": "unknown",
            "query": command
        }
