from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QListWidget


class HistoricTournamentsView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TournamentCard")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("🗂 Historique"))

        self.list = QListWidget()
        layout.addWidget(self.list)

    def set_tournaments(self, tournaments):
        self.list.clear()
        for t in tournaments:
            self.list.addItem(
                f"{t['name']} ({t['date']}) — 🏆 {t['winner']} • {t['players']} joueurs"
            )
