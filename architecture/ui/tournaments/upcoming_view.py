from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QMessageBox,
)
from PySide6.QtCore import Qt, Signal

from core.tournament import Tournament
from ui.widgets.tournament_card import TournamentCard
from ui.tournaments.dialogs.create_tournament import CreateTournamentDialog
from storage.tournaments import TournamentStorage


class UpcomingView(QWidget):
    """
    Vue des tournois à venir.
    """

    # 🔗 Signal vers TournamentViewMain
    launch_requested = Signal(Tournament)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("UpcomingView")
        self.setAttribute(Qt.WA_StyledBackground, True)

        # =========================
        # Données (OBJETS METIER UNIQUEMENT)
        # =========================
        self._tournaments: list[Tournament] = []
        self._tournament_ids: dict[int, str] = {}
        self._cards_by_id: dict[int, TournamentCard] = {}

        self._build_ui()
        self._load_tournaments_from_storage()

    # ======================================================
    # ID MANAGEMENT
    # ======================================================
    def _get_next_free_id(self) -> int:
        used_ids = sorted(t.id for t in self._tournaments)
        current = 1
        for tid in used_ids:
            if tid != current:
                return current
            current += 1
        return current

    # ======================================================
    # UI
    # ======================================================
    def _build_ui(self):
        self.root_layout = QVBoxLayout(self)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(16)

        # ---------- Header ----------
        header = QFrame()
        header.setObjectName("UpcomingHeader")
        header.setAttribute(Qt.WA_StyledBackground, True)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("⏳ Tournois à venir")
        title.setObjectName("UpcomingTitle")

        add_btn = QPushButton("➕  Nouveau tournoi")
        add_btn.setObjectName("UpcomingPrimaryButton")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self._open_create_dialog)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(add_btn)

        self.root_layout.addWidget(header)

        # ---------- Scroll ----------
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

        scroll.setWidget(content)

        scroll_container = QFrame()
        scroll_container.setObjectName("UpcomingScrollContainer")
        scroll_container.setAttribute(Qt.WA_StyledBackground, True)

        scroll_container_layout = QVBoxLayout(scroll_container)
        scroll_container_layout.setContentsMargins(12, 12, 12, 12)
        scroll_container_layout.addWidget(scroll)

        self.root_layout.addWidget(scroll_container, 1)

    # ======================================================
    # Create / Edit
    # ======================================================
    def _open_create_dialog(self):
        dialog = CreateTournamentDialog(self)

        if not dialog.exec():
            return

        tid = self._get_next_free_id()
        tournament = dialog.build_tournament(tournament_id=tid)

        # 1️⃣ Modèle
        self._tournaments.append(tournament)

        # 2️⃣ UI
        self._register_tournament(tournament)

        # 3️⃣ Persistance
        self._save_all()

    def _register_tournament(self, tournament: Tournament):
        tid = tournament.id
        self._tournament_ids[tid] = tournament.name

        card = TournamentCard(tournament, self)
        self._cards_by_id[tid] = card

        card.request_edit.connect(
            lambda t=tournament, c=card: self._edit_tournament(c, t)
        )
        card.request_launch.connect(self._send_to_launch)
        card.request_delete.connect(
            lambda t=tournament, c=card: self._delete_tournament(c, t)
        )

        self.cards_layout.insertWidget(
            self.cards_layout.count() - 1,
            card
        )

    def _edit_tournament(self, card: TournamentCard, tournament: Tournament):
        dialog = CreateTournamentDialog(self, tournament=tournament)

        if not dialog.exec():
            return

        dialog.apply_changes()
        self._save_all()
        card._refresh()

    def _delete_tournament(self, card: TournamentCard, tournament: Tournament):
        reply = QMessageBox.question(
            self,
            "Supprimer le tournoi",
            f"Supprimer définitivement « {tournament.name} » ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        tid = tournament.id

        self._tournaments = [t for t in self._tournaments if t.id != tid]
        self._tournament_ids.pop(tid, None)
        self._cards_by_id.pop(tid, None)

        self.cards_layout.removeWidget(card)
        card.deleteLater()

        self._save_all()

    # ======================================================
    # Launch
    # ======================================================
    def _send_to_launch(self, tournament: Tournament):
        self.launch_requested.emit(tournament)

    def hide_tournament_card(self, tournament_id: int):
        card = self._cards_by_id.get(tournament_id)
        if card:
            card.hide()

    def show_tournament_card(self, tournament_id: int):
        card = self._cards_by_id.get(tournament_id)
        if card:
            card.show()

    def refresh_tournament(self, tournament: Tournament):
        card = self._cards_by_id.get(tournament.id)
        if card:
            card._refresh()
        self._save_all()

    # ======================================================
    # Storage
    # ======================================================
    def _load_tournaments_from_storage(self):
        raw = TournamentStorage.load()
        self._tournaments.clear()

        for data in raw:
            tournament = Tournament.from_dict(data)
            self._tournaments.append(tournament)
            self._register_tournament(tournament)

    def _save_all(self):
        TournamentStorage.save([t.to_dict() for t in self._tournaments])
