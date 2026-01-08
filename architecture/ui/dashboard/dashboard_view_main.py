from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QTimer

from ui.dashboard.tiles_view import DashboardTilesView
from ui.dashboard.ranking_view import DashboardRankingView
from ui.dashboard.tables_view import DashboardTablesView


class DashboardViewMain(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.player_matches = {
            "Martin": [
                {"round": 1, "table": 3, "position": "1er"},
                {"round": 2, "table": 1, "position": "2e"},
                {"round": 3, "table": 5, "position": "5er"},
                {"round": 4, "table": 3, "position": "4e"},
                {"round": 5, "table": 2, "position": "1e"},
            ],
            "Audric": [
                {"round": 1, "table": 2, "position": "2e"},
                {"round": 2, "table": 4, "position": "3e"},
            ],
        }

        root = QVBoxLayout(self)
        root.setSpacing(30)
        root.setContentsMargins(0, 0, 0, 0)

        # === TUILES ===
        self.tiles_view = DashboardTilesView(self)
        root.addWidget(self.tiles_view)

        # === CLASSEMENT ===
        self.ranking_view = DashboardRankingView(self)
        self.ranking_view.set_player_matches(self.player_matches)
        root.addWidget(self.ranking_view)

        # === TABLES DE JEU ===
        self.tables_view = DashboardTablesView(self)
        root.addWidget(self.tables_view)

        # === STRETCH TOUJOURS EN DERNIER ===
        root.addStretch()
        root.addStretch()

        # === TIMER MOCK ===
        self.remaining_seconds = 15 * 60
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(1000)

    def _tick(self):
        if self.remaining_seconds <= 0:
            return

        self.remaining_seconds -= 1
        m = self.remaining_seconds // 60
        s = self.remaining_seconds % 60
        self.tiles_view.set_timer_text(f"{m:02d}:{s:02d}")
