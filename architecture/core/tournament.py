from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Tournament:
    id: int
    name: str
    format: str
    date: str

    players: List[str] = field(default_factory=list)

    # =====================
    # Business logic
    # =====================

    def add_player(self, name: str) -> bool:
        name = name.strip()
        if not name:
            return False

        # Empêcher les doublons (case-insensitive)
        if name.lower() in (p.lower() for p in self.players):
            return False

        self.players.append(name)
        return True

    def remove_player(self, name: str):
        self.players = [
            p for p in self.players
            if p.lower() != name.lower()
        ]

    @property
    def player_count(self) -> int:
        return len(self.players)

    def table_count(self, seats_per_table: int = 4) -> int:
        if self.player_count == 0:
            return 0
        return max(1, self.player_count // seats_per_table)

    # =====================
    # Serialization
    # =====================

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "format": self.format,
            "date": self.date,
            "players": self.players,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Tournament":
        return cls(
            id=data["id"],
            name=data["name"],
            format=data["format"],
            date=data["date"],
            players=data.get("players", []),
        )
