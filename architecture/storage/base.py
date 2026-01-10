import json
from pathlib import Path


DATA_DIR = Path("data")


class JsonStorage:
    filename: str  # à définir dans les subclasses

    @classmethod
    def _file(cls) -> Path:
        return DATA_DIR / cls.filename

    @classmethod
    def load(cls) -> list[dict]:
        path = cls._file()

        if not path.exists():
            return []

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def save(cls, data: list[dict]):
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        with open(cls._file(), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
