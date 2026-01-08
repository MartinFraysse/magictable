from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QTableWidget,
    QTableWidgetItem, QSizePolicy, QHeaderView,
    QScrollArea
)
from PySide6.QtCore import Qt, QTimer
from ui.widgets.horizontal_scroll_area import HorizontalScrollArea
from ui.widgets.player_matches_popup import PlayerMatchesPopup
from PySide6.QtGui import QCursor
from PySide6.QtCore import QPoint, QEvent


class DashboardView(QWidget):
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
        root.addWidget(self._build_tiles())

        # === CLASSEMENT ===
        root.addWidget(self._build_ranking())

        # === TABLES DE JEU (NOUVELLE SECTION) ===
        root.addWidget(self._build_tables_section())

        # === STRETCH TOUJOURS EN DERNIER ===
        root.addStretch()


        root.addStretch()

        # === TIMER MOCK ===
        self.remaining_seconds = 15 * 60
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(1000)

    # =================================================
    # Tiles
    # =================================================
    def _build_tiles(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tile_active = self._tile("🟢", "Tournoi actif", "Oui")
        self.tile_name = self._tile("🏷", "Nom", "Friday Night Magic")
        self.tile_players = self._tile("👥", "Joueurs", "24")
        self.tile_tables = self._tile("🪑", "Tables", "12")
        self.tile_timer = self._tile("⏱", "Prochaine round", "15:00")

        for tile in (
            self.tile_active,
            self.tile_name,
            self.tile_players,
            self.tile_tables,
            self.tile_timer,
        ):
            layout.addWidget(tile)

        return container

    def _tile(self, icon, title, value):
        frame = QFrame()
        frame.setObjectName("DashboardTile")
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout(frame)
        layout.setSpacing(4)
        layout.setContentsMargins(16, 16, 16, 16)

        # === ACCENT VISUEL (Qt-native) ===
        accent = QFrame()
        accent.setFixedWidth(4)
        accent.setStyleSheet(
            "background-color: #3fd27d; border-radius: 2px;"
        )
        layout.insertWidget(0, accent)

        lbl_icon = QLabel(icon)
        lbl_icon.setObjectName("DashboardTileIcon")

        lbl_value = QLabel(value)
        lbl_value.setObjectName("DashboardTileValue")

        lbl_title = QLabel(title)
        lbl_title.setObjectName("DashboardTileTitle")

        layout.addWidget(lbl_icon)
        layout.addWidget(lbl_value)
        layout.addWidget(lbl_title)

        # 🔑 référence pour mise à jour dynamique
        frame.value_label = lbl_value

        return frame

    # =================================================
    # Ranking
    # =================================================
    def _build_ranking(self):
        frame = QFrame()
        frame.setObjectName("DashboardCard")

        layout = QVBoxLayout(frame)
        layout.setSpacing(12)

        title = QLabel("🏆 Aperçu du classement")
        title.setObjectName("DashboardSectionTitle")
        layout.addWidget(title)

        table = QTableWidget(0, 3)
        table.setObjectName("DashboardTable")

        # --- Structure ---
        table.setHorizontalHeaderLabels(["#", "Joueur", "Évolution"])
        table.verticalHeader().setVisible(False)

        # --- Comportement ---
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setSelectionMode(QTableWidget.SingleSelection)
        table.setFocusPolicy(Qt.NoFocus)
        table.setCursor(Qt.PointingHandCursor)

        # --- Apparence ---
        table.setShowGrid(False)
        table.setAlternatingRowColors(False)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        # --- Header sizing ---
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        data = [
            (1, "Martin", +2),
            (2, "Audric", -1),
            (3, "Luc", +2),
            (4, "Emma", -2),
            (5, "Nina", -4),
            (6, "Gael", +2),
            (7, "Chouchou", -2),
            (8, "Raph", +3),
            (9, "Dylan", 0),
            (10, "Pirate", +1),
            (11, "Lou", +2),
            (12, "Seb", -3),
            (13, "Sebito", -1),
            (14, "Thomas", +1),
            (15, "Mathieux", -4),        
        ]

        # 🔑 CRUCIAL : on fixe les lignes AVANT de remplir
        table.setRowCount(len(data))

        for row, (pos, name, delta) in enumerate(data):
            item_pos = QTableWidgetItem(str(pos))
            item_pos.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 0, item_pos)

            item_name = QTableWidgetItem(name)
            table.setItem(row, 1, item_name)


            if delta > 0:
                txt = f"▲ +{delta}"
                color = Qt.green
            elif delta < 0:
                txt = f"▼ {delta}"
                color = Qt.red
            else:
                txt = "— 0"
                color = Qt.lightGray

            item = QTableWidgetItem(txt)
            item.setTextAlignment(Qt.AlignCenter)
            item.setForeground(color)
            table.setItem(row, 2, item)

        # Hauteur dynamique (évite zone blanche)
            VISIBLE_ROWS = 7  # nombre de lignes visibles souhaitées

            table.setFixedHeight(
                table.horizontalHeader().height()
                + table.rowHeight(0) * VISIBLE_ROWS
                + 4
            )


        layout.addWidget(table)

        table.setMouseTracking(True)
        table.viewport().setMouseTracking(True)

        self.popup = PlayerMatchesPopup(self)
        self.popup.hide()

        table.itemEntered.connect(
            lambda item: self._on_player_hover(table, item)
        )

        self.ranking_table = table
        self.ranking_viewport = table.viewport()
        self.ranking_viewport.installEventFilter(self)

        table.viewport().installEventFilter(self)

        return frame

    # =================================================
    # ACTIVE TABLES
    # =================================================
    def _build_tables_section(self):
        frame = QFrame()
        frame.setObjectName("DashboardCard")

        layout = QVBoxLayout(frame)
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
        #scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        container.setObjectName("TablesScrollContent")  # ⬅️ IMPORTANT
        #container.setStyleSheet("background: transparent;")

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
        return frame

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

    # =================================================
    # Countdown
    # =================================================
    def _tick(self):
        if self.remaining_seconds <= 0:
            return

        self.remaining_seconds -= 1
        m = self.remaining_seconds // 60
        s = self.remaining_seconds % 60
        self.tile_timer.value_label.setText(f"{m:02d}:{s:02d}")

    # =================================================
    # Hover
    # =================================================
    def _on_player_hover(self, table, item):
        if not item:
            self.popup.hide()
            return

        row = item.row()
        name_item = table.item(row, 1)

        if not name_item:
            self.popup.hide()
            return

        name = name_item.text()
        matches = self.player_matches.get(name)

        if not matches:
            self.popup.hide()
            return

        self.popup.set_player(name, matches)
        self.popup.move(QCursor.pos() + QPoint(15, 15))
        self.popup.show()
        
    def eventFilter(self, obj, event):
        # Souris quitte le tableau → on cache la popup
        if obj is self.ranking_viewport and event.type() == QEvent.Leave:
            self.popup.hide()
            return False

        # Souris bouge DANS le tableau → popup suit
        if obj is self.ranking_viewport and event.type() == QEvent.MouseMove:
            if self.popup.isVisible():
                self.popup.move(QCursor.pos() + QPoint(15, 15))
            return False

        return super().eventFilter(obj, event)



