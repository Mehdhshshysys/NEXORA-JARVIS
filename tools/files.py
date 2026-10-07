from pathlib import Path


class FilesTool:

    def list_files(self, folder="."):
        path = Path(folder)

        if not path.exists():
            return "این پوشه وجود ندارد."

        if not path.is_dir():
            return "این مسیر یک پوشه نیست."

        items = []

        for item in path.iterdir():

            if item.is_dir():
                items.append(f"[پوشه] {item.name}")

            else:
                items.append(f"[فایل] {item.name}")

        if not items:
            return "این پوشه خالی است."

        return "\n".join(items)

    def create_file(self, filename):
        path = Path(filename)

        if path.exists():
            return "این فایل از قبل وجود دارد."

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        path.touch()

        return f"فایل {filename} ساخته شد."

    def delete_file(self, filename):
        path = Path(filename)

        if not path.exists():
            return "این فایل وجود ندارد."

        if path.is_dir():
            return "این مسیر یک پوشه است."

        path.unlink()

        return f"فایل {filename} حذف شد."
