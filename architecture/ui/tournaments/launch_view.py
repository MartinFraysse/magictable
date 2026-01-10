from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QListWidgetItem,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QGridLayout,
    QListWidget,
)
import json

from core.tournament import Tournament


class LaunchView(QWidget):
    """
    Vue de lancement d’un tournoi.
    """

    # =====================
    # Signals
    # =====================
    tournament_taken = Signal(int)
    tournament_cancelled = Signal(int)
    edit_requested = Signal(Tournament)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._current_tournament: Tournament | None = None

        self.setObjectName("LaunchView")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAcceptDrops(True)

        self._build_ui()

    # ======================================================
    # UI
    # ======================================================
    def _build_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # ==================================================
        # PLACEHOLDER
        # ==================================================
        self.placeholder_widget = QFrame()
        self.placeholder_widget.setObjectName("LaunchContainerInner")
        self.placeholder_widget.setAttribute(Qt.WA_StyledBackground, True)

        ph_layout = QVBoxLayout(self.placeholder_widget)
        ph_layout.setAlignment(Qt.AlignCenter)
        ph_layout.setSpacing(12)

        title = QLabel("🎮 Lancer un tournoi")
        title.setObjectName("LaunchTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel(
            "Sélectionnez ou déposez un tournoi\n"
            "depuis la liste des tournois à venir"
        )
        subtitle.setObjectName("LaunchSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        ph_layout.addWidget(title)
        ph_layout.addWidget(subtitle)

        # ==================================================
        # CARD CONTAINER (HEADER + BODY)
        # ==================================================
        self.card_container = QFrame()
        self.card_container.setObjectName("LaunchCardContainer")
        self.card_container.setAttribute(Qt.WA_StyledBackground, True)
        self.card_container.hide()

        card_layout = QVBoxLayout(self.card_container)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        # ==================================================
        # HEADER
        # ==================================================
        self.header_container = QFrame()
        self.header_container.setObjectName("LaunchHeaderContainer")
        self.header_container.setAttribute(Qt.WA_StyledBackground, True)

        header_layout = QGridLayout(self.header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setHorizontalSpacing(16)
        header_layout.setVerticalSpacing(6)

        self.header_title = QLabel()
        self.header_title.setObjectName("LaunchHeaderTitle")

        self.header_format = QLabel()
        self.header_format.setObjectName("LaunchHeaderFormat")

        self.header_meta = QLabel()
        self.header_meta.setObjectName("LaunchHeaderMeta")

        self.edit_btn = QPushButton("Modifier")
        self.edit_btn.setObjectName("LaunchPrimaryButton")
        self.edit_btn.clicked.connect(self._edit_current_tournament)

        self.cancel_btn = QPushButton("Retirer")
        self.cancel_btn.setObjectName("LaunchPrimaryButton")
        self.cancel_btn.clicked.connect(self._cancel_current_tournament)

        header_layout.addWidget(self.header_title, 0, 0)
        header_layout.addWidget(self.edit_btn, 0, 1)
        header_layout.addWidget(self.header_format, 1, 0)
        header_layout.addWidget(self.cancel_btn, 1, 1)
        header_layout.addWidget(self.header_meta, 2, 0, 1, 2)

        card_layout.addWidget(self.header_container)

        # ==================================================
        # BODY
        # ==================================================
        self.body_container = QFrame()
        self.body_container.setObjectName("LaunchPreparationContainer")
        self.body_container.setAttribute(Qt.WA_StyledBackground, True)

        body_layout = QVBoxLayout(self.body_container)
        body_layout.setContentsMargins(0, 0, 0, 0)

        self.prep_container = QFrame()
        self.prep_container.setObjectName("LaunchPreparationInner")

        prep_layout = QVBoxLayout(self.prep_container)
        prep_layout.setContentsMargins(0, 0, 0, 0)
        prep_layout.setSpacing(16)

        players_title = QLabel("👥 Joueurs inscrits")
        players_title.setObjectName("LaunchSectionTitle")
        prep_layout.addWidget(players_title)


        self.players_list = QListWidget()
        prep_layout.addWidget(self.players_list)

        row = QHBoxLayout()
        self.player_input = QLineEdit()
        self.player_input.setObjectName("LaunchPlayerInput")
        self.player_input.setPlaceholderText("Nom du joueur")
        self.player_input.returnPressed.connect(self._add_player_manual)


        add_btn = QPushButton("➕ Ajouter")
        add_btn.setObjectName("LaunchPrimaryButton")
        add_btn.clicked.connect(self._add_player_manual)

        row.addWidget(self.player_input)
        row.addWidget(add_btn)
        prep_layout.addLayout(row)

        self.tables_info = QLabel()
        self.tables_info.setObjectName("LaunchInfoText")
        prep_layout.addWidget(self.tables_info)


        body_layout.addWidget(self.prep_container)
        card_layout.addWidget(self.body_container)

        # ==================================================
        # MAIN LAYOUT
        # ==================================================
        self.main_layout.addWidget(self.placeholder_widget, 1)
        self.main_layout.addWidget(self.card_container, 1)

    # ======================================================
    # Drag & Drop
    # ======================================================
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-magictable-tournament"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        if self._current_tournament:
            event.ignore()
            return

        raw = event.mimeData().data("application/x-magictable-tournament")
        data = json.loads(bytes(raw).decode("utf-8"))
        tournament = Tournament.from_dict(data)

        self._load_tournament(tournament)
        self.tournament_taken.emit(tournament.id)
        event.acceptProposedAction()

    # ======================================================
    # State
    # ======================================================
    def _load_tournament(self, tournament: Tournament):
        self._current_tournament = tournament

        self.placeholder_widget.hide()
        self.card_container.show()

        self.header_title.setText(tournament.name)
        self.header_format.setText(tournament.format)
        self._refresh_meta()

        self.players_list.clear()
        for p in tournament.players:
            self.players_list.addItem(QListWidgetItem(p))

        self._update_tables_info()

    def _edit_current_tournament(self):
        if self._current_tournament:
            self.edit_requested.emit(self._current_tournament)

    def _cancel_current_tournament(self):
        if not self._current_tournament:
            return

        tid = self._current_tournament.id
        self._current_tournament = None

        self.card_container.hide()
        self.placeholder_widget.show()

        self.players_list.clear()
        self.player_input.clear()
        self.tables_info.setText("🪑 0 joueur → 0 table")

        self.tournament_cancelled.emit(tid)

    # ======================================================
    # Players
    # ======================================================
    def _add_player_manual(self):
        if not self._current_tournament:
            return

        name = self.player_input.text().strip()
        if not name:
            return

        if self._current_tournament.add_player(name):
            self.players_list.addItem(QListWidgetItem(name))
            self.player_input.clear()
            self._update_tables_info()

    def _update_tables_info(self):
        if not self._current_tournament:
            self.tables_info.setText("🪑 0 joueur → 0 table")
            return

        players = self._current_tournament.player_count
        tables = self._current_tournament.table_count()

        self.tables_info.setText(
            f"🪑 {players} joueur{'s' if players > 1 else ''} → "
            f"{tables} table{'s' if tables > 1 else ''}"
        )

    def _refresh_meta(self):
        t = self._current_tournament
        self.header_meta.setText(
            f"{t.date} • {t.player_count} joueurs"
        )
