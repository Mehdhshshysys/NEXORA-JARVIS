import json
from pathlib import Path


class Memory:

    def __init__(self, file_path="data/memory.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self.save({})

    def load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)

        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save(self, data):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    def remember(self, key, value):
        data = self.load()
        data[key] = value
        self.save(data)

        return f"ذخیره شد: {key}"

    def recall(self, key):
        data = self.load()
        return data.get(key)

    def forget(self, key):
        data = self.load()

        if key in data:
            del data[key]
            self.save(data)
            return f"حذف شد: {key}"

        return "چیزی با این نام پیدا نشد."

    def all_memory(self):
        return self.load()
