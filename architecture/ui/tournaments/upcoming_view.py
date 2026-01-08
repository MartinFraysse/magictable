from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel,
    QListWidget, QListWidgetItem,
    QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt, Signal


class UpcomingTournamentsView(QFrame):
    tournament_selected = Signal(dict)
    create_requested = Signal()
    launch_requested = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("UpcomingColumn")

        self.selected = None

        root = QVBoxLayout(self)
        root.setSpacing(12)

        # === TITRE ===
        title = QLabel("📅 Tournois à venir")
        title.setObjectName("SectionTitle")
        root.addWidget(title)

        # === LISTE ===
        self.list = QListWidget()
        self.list.setObjectName("TournamentList")
        self.list.itemSelectionChanged.connect(self._on_selection)
        root.addWidget(self.list, 1)

        # === ACTIONS ===
        actions = QHBoxLayout()

        self.new_btn = QPushButton("➕ Nouveau")
        self.launch_btn = QPushButton("▶ Créer le tournoi")
        self.launch_btn.setEnabled(False)

        self.new_btn.clicked.connect(self.create_requested.emit)
        self.launch_btn.clicked.connect(self._emit_launch)

        actions.addWidget(self.new_btn)
        actions.addWidget(self.launch_btn)

        root.addLayout(actions)

    # =================================================
    # DATA
    # =================================================
    def set_tournaments(self, tournaments):
        self.list.clear()
        self.selected = None
        self.launch_btn.setEnabled(False)

        for t in tournaments:
            item = QListWidgetItem(f"{t['name']} — {t['format']} ({t['date']})")
            item.setData(Qt.UserRole, t)
            self.list.addItem(item)

    # =================================================
    # EVENTS
    # =================================================
    def _on_selection(self):
        item = self.list.currentItem()
        if not item:
            self.selected = None
            self.launch_btn.setEnabled(False)
            return

        self.selected = item.data(Qt.UserRole)
        self.launch_btn.setEnabled(True)
        self.tournament_selected.emit(self.selected)

    def _emit_launch(self):
        if self.selected:
            self.launch_requested.emit(self.selected)
