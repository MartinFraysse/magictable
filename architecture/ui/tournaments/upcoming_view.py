from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
)
from PySide6.QtCore import Qt, Signal

from ui.widgets.tournament_card import TournamentCard
from ui.tournaments.dialogs.create_tournament import CreateTournamentDialog
# from ui.widgets.tournament_scorecard import TournamentScoreCard


class UpcomingView(QWidget):
    """
    Vue des tournois à venir.

    Responsabilités :
    - Afficher la liste des tournois futurs
    - Permettre la création de nouveaux tournois
    - Servir de source pour le lancement d’un tournoi
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("UpcomingView")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._tournaments = []

        self._build_ui()
        # DEV ONLY — Seed UI
        self._seed_test_tournaments()

    # =========================
    # UI
    # =========================
    def _build_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(16)

        # =========================
        # Header
        # =========================
        header = QFrame()
        header.setObjectName("UpcomingHeader")
        header.setAttribute(Qt.WA_StyledBackground, True)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("⏳ Tournois à venir")
        title.setObjectName("UpcomingTitle")

        add_btn = QPushButton("➕ Nouveau tournoi")
        add_btn.setObjectName("AddTournamentButton")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self._open_create_dialog)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(add_btn)

        root_layout.addWidget(header)

        # =========================
        # Scroll area
        # =========================
        scroll = QScrollArea()
        scroll.setObjectName("UpcomingScrollArea")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        content.setObjectName("UpcomingContent")
        content.setAttribute(Qt.WA_StyledBackground, True)

        self.cards_layout = QVBoxLayout(content)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(12)
        self.cards_layout.addStretch()

        # =========================
        # Scroll Container
        # =========================
        scroll_container = QFrame()
        scroll_container.setObjectName("UpcomingScrollContainer")
        scroll_container.setAttribute(Qt.WA_StyledBackground, True)

        scroll_container_layout = QVBoxLayout(scroll_container)
        scroll_container_layout.setContentsMargins(12, 12, 12, 12)
        scroll_container_layout.setSpacing(0)

        scroll_container_layout.addWidget(scroll)
        scroll.setWidget(content)

        root_layout.addWidget(scroll_container, 1)

    # =========================
    # Logic
    # =========================
    def _open_create_dialog(self):
        dialog = CreateTournamentDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            self._add_tournament(data)

    def _add_tournament(self, data: dict):
        self._tournaments.append(data)

        card = TournamentCard(data, self)

        card.request_edit.connect(
            lambda d, c=card: self._edit_tournament(c, d)
        )

        # === Connexions ===
        card.request_edit.connect(self._edit_tournament)
        card.request_launch.connect(self._send_to_launch)

        self.cards_layout.insertWidget(
            self.cards_layout.count() - 1,
            card
        )

    # =========================
    # Context menu actions
    # =========================
    def _edit_tournament(self, card: TournamentCard, data: dict):
        dialog = CreateTournamentDialog(self, data=data)

        if dialog.exec():
            new_data = dialog.get_data()

            # Mise à jour des données internes
            index = self._tournaments.index(data)
            self._tournaments[index] = new_data

            # Mise à jour VISUELLE de la carte
            card.update_data(new_data)



    def _send_to_launch(self, data: dict):
        """
        Envoyer le tournoi vers la LaunchView.
        (placeholder pour l’instant)
        """
        print("SEND TO LAUNCH:", data)
        # plus tard : signal vers TournamentViewMain / LaunchView

    def _update_tournament(self, old: dict, new: dict):
        """
        Met à jour un tournoi existant (dev-only pour l’instant).
        """
        old.update(new)

        # Rafraîchissement visuel basique
        for i in range(self.cards_layout.count()):
            widget = self.cards_layout.itemAt(i).widget()
            if hasattr(widget, "get_data") and widget.get_data() is old:
                widget.title_label.setText(new["name"])
                widget.meta_label.setText(
                    f'{new["format"]} • {new["date"]} • {new["players"]} joueurs'
                )
                break






# ----------------------------------------------------------------------------------
    # =========================
    # DEV — Seed test data
    # =========================
    def _seed_test_tournaments(self):
        """
        Ajoute des tournois de test pour le développement UI.
        À supprimer ou désactiver en production.
        """
        test_data = [
            {
                "name": "Friday Night Magic",
                "format": "Commander",
                "date": "12/01/2026",
                "players": 24,
            },
            {
                "name": "Weekly Duel",
                "format": "Standard",
                "date": "15/01/2026",
                "players": 16,
            },
            {
                "name": "Modern League",
                "format": "Modern",
                "date": "18/01/2026",
                "players": 32,
            },
            {
                "name": "Casual Commander Night",
                "format": "Commander",
                "date": "20/01/2026",
                "players": 20,
            },
            {
                "name": "Draft du Samedi",
                "format": "Draft",
                "date": "22/01/2026",
                "players": 12,
            },
        ]

        for data in test_data:
            self._add_tournament(data)
