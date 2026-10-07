class Brain:

    def understand(self, command):

        command = command.strip()
        text = command.lower()

        # YouTube
        if "یوتیوب" in text:
            return {
                "tool": "browser",
                "action": "youtube",
                "query": command
            }

        # Google / Search
        if (
            "گوگل" in text
            or "جستجو" in text
            or "سرچ" in text
        ):
            return {
                "tool": "browser",
                "action": "google",
                "query": command
            }

        # Open website
        if "باز کن" in text and "سایت" in text:
            return {
                "tool": "browser",
                "action": "open_site",
                "query": command
            }

        # Notepad
        if (
            "نوت پد" in text
            or "نوت‌پد" in text
            or "notepad" in text
        ):
            return {
                "tool": "apps",
                "action": "open_app",
                "query": "notepad"
            }

        # Calculator
        if (
            "ماشین حساب" in text
            or "calculator" in text
            or "calc" in text
        ):
            return {
                "tool": "apps",
                "action": "open_app",
                "query": "calculator"
            }

        # List files
        if "فایل ها" in text or "فایل‌ها" in text:
            return {
                "tool": "files",
                "action": "list_files"
            }

        # Create file
        if (
            "فایل بساز" in text
            or "فایل ایجاد کن" in text
        ):
            return {
                "tool": "files",
                "action": "create_file",
                "query": command
            }

        # Delete file
        if (
            "فایل حذف کن" in text
            or "فایل پاک کن" in text
        ):
            return {
                "tool": "files",
                "action": "delete_file",
                "query": command
            }

        # Time
        if "ساعت" in text:
            return {
                "tool": "system",
                "action": "time"
            }

        # System information
        if (
            "سیستم" in text
            or "مشخصات کامپیوتر" in text
        ):
            return {
                "tool": "system",
                "action": "info"
            }

        # Remember
        if (
            "یاد بگیر" in text
            or "یادت باشه" in text
        ):
            return {
                "tool": "memory",
                "action": "remember",
                "query": command
            }

        # Terminal
        if (
            "اجرا کن" in text
            or "دستور اجرا کن" in text
        ):
            return {
                "tool": "terminal",
                "action": "run",
                "query": command
            }

        # Exit
        if text in [
            "خروج",
            "بستن",
            "exit",
            "quit"
        ]:
            return {
                "tool": "system",
                "action": "exit"
            }

        # Unknown
        return {
            "tool": "unknown",
            "action": "unknown",
            "query": command
        }
