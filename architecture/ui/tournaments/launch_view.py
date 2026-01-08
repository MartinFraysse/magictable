from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal, Qt


class LaunchTournamentView(QFrame):
    tournament_launched = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TournamentCard")

        self.selected = None

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("▶ Lancer un tournoi"))

        self.label = QLabel("Aucun tournoi sélectionné")
        self.label.setAlignment(Qt.AlignCenter)

        self.btn = QPushButton("Lancer")
        self.btn.setEnabled(False)
        self.btn.clicked.connect(self._launch)

        layout.addWidget(self.label)
        layout.addWidget(self.btn)

    def set_selected_tournament(self, tournament: dict):
        self.selected = tournament
        self.label.setText(f"Tournoi sélectionné : <b>{tournament['name']}</b>")
        self.btn.setEnabled(True)

    def _launch(self):
        if self.selected:
            self.tournament_launched.emit(self.selected)
