from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QMenu,
)


class TournamentCard(QFrame):
    """
    Carte représentant un tournoi.
    """

    request_edit = Signal(dict)
    request_launch = Signal(dict)

    def __init__(self, data: dict, parent=None):
        super().__init__(parent)

        self.data = data

        self.setObjectName("TournamentCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(Qt.PointingHandCursor)

        self._build_ui()

    # =========================
    # UI
    # =========================
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        # === NOM ===
        self.title_label = QLabel(self.data.get("name", "Nom du tournoi"))
        self.title_label.setObjectName("TournamentCardTitle")
        self.title_label.setWordWrap(False)
        self.title_label.setToolTip(self.data.get("name", ""))

        # === FORMAT ===
        self.format_label = QLabel(self.data.get("format", ""))
        self.format_label.setObjectName("TournamentCardFormat")

        # === DATE • JOUEURS ===
        meta_text = (
            f'{self.data.get("date")} • '
            f'{self.data.get("players")} joueurs'
        )
        self.meta_label = QLabel(meta_text)
        self.meta_label.setObjectName("TournamentCardMeta")

        layout.addWidget(self.title_label)
        layout.addWidget(self.format_label)
        layout.addWidget(self.meta_label)

    # =========================
    # Context menu
    # =========================
    def contextMenuEvent(self, event):
        menu = QMenu(self)

        edit_action = menu.addAction("✏️ Modifier le tournoi")
        menu.addSeparator()
        launch_action = menu.addAction("🚀 Envoyer vers Launch")

        action = menu.exec(event.globalPos())

        if action == edit_action:
            self.request_edit.emit(self.data)
        elif action == launch_action:
            self.request_launch.emit(self.data)

    def update_data(self, data: dict):
        """
        Met à jour les données de la carte et rafraîchit l'affichage.
        """
        self.data = data

        self.title_label.setText(data.get("name", ""))
        self.format_label.setText(data.get("format", ""))

        meta_text = (
            f'{data.get("date")} • '
            f'{data.get("players")} joueurs'
        )
        self.meta_label.setText(meta_text)
