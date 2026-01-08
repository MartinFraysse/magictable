from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout,
    QLabel, QWidget
)
from PySide6.QtCore import Qt

from ui.widgets.horizontal_scroll_area import HorizontalScrollArea


class DashboardTablesView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("DashboardCard")

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("🎲 Tables en cours")
        title.setObjectName("DashboardSectionTitle")
        layout.addWidget(title)

        scroll = HorizontalScrollArea()
        scroll.setObjectName("TablesScrollArea")  # ⬅️ IMPORTANT
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        container.setObjectName("TablesScrollContent")  # ⬅️ IMPORTANT

        h_layout = QHBoxLayout(container)
        h_layout.setSpacing(16)
        h_layout.setContentsMargins(16, 0, 16, 0)  # ⬅️ empêche le blanc latéral

        # --- MOCK DATA ---
        tables = [
            {
                "id": 1,
                "players": ["Martin", "Jean-Francois", "Gael", "Gaethan"],
                "finished": True,
                "winner": "None",
            },
            {
                "id": 2,
                "players": ["Audric", "Emma"],
                "finished": True,
                "winner": "Audric",
            },
            {
                "id": 3,
                "players": ["Nina", "Paul", "Tom"],
                "finished": False,
                "winner": None,
            },
            {
                "id": 4,
                "players": ["Nina", "Paul", "Tom"],
                "finished": False,
                "winner": None,
            },
            {
                "id": 5,
                "players": ["Nina", "Paul", "Tom"],
                "finished": False,
                "winner": None,
            },
        ]

        for t in tables:
            h_layout.addWidget(self._table_card(t))

        h_layout.addStretch()
        scroll.setWidget(container)

        layout.addWidget(scroll)

    def _table_card(self, table):
        card = QFrame()
        card.setObjectName("TableCard")
        card.setFixedWidth(220)
        card.setFixedHeight(150)

        layout = QVBoxLayout(card)
        layout.setSpacing(6)

        lbl_id = QLabel(f"Table {table['id']}")
        lbl_id.setObjectName("TableCardTitle")

        players = table["players"]  # liste de noms
        players_text = " vs ".join(players)

        lbl_players = QLabel(players_text)
        lbl_players.setObjectName("TableCardPlayers")
        lbl_players.setWordWrap(True)
        lbl_players.setMaximumHeight(40)  # force 2 lignes max

        if table["finished"]:
            status = QLabel("✔ Terminée")
            status.setObjectName("TableCardFinished")

            winner = QLabel(f"Gagnant : {table['winner']}")
            winner.setObjectName("TableCardWinner")

            layout.addWidget(lbl_id)
            layout.addWidget(lbl_players)
            layout.addWidget(status)
            layout.addWidget(winner)
        else:
            status = QLabel("⏳ En cours")
            status.setObjectName("TableCardRunning")

            layout.addWidget(lbl_id)
            layout.addWidget(lbl_players)
            layout.addWidget(status)

        if table["finished"]:
            card.setProperty("status", "finished")
        else:
            card.setProperty("status", "running")

        return card
