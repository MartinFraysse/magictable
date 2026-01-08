from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, QPoint, QEvent
from PySide6.QtGui import QCursor
from ui.widgets.player_matches_popup import PlayerMatchesPopup


class DashboardRankingView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("DashboardCard")

        self.player_matches = {}

        self._last_popup_pos = None

        layout = QVBoxLayout(self)
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
            item_name.setTextAlignment(Qt.AlignCenter) 
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

    def set_player_matches(self, player_matches: dict):
        self.player_matches = player_matches

    # =================================================
    # Hover
    # =================================================
    def _on_player_hover(self, table, item):
        if not item:
            self.popup.hide()
            self._last_popup_pos = None
            return

        row = item.row()
        name_item = table.item(row, 1)

        if not name_item:
            self.popup.hide()
            self._last_popup_pos = None
            return

        name = name_item.text()
        matches = self.player_matches.get(name)

        if not matches:
            self.popup.hide()
            self._last_popup_pos = None
            return

        self.popup.set_player(name, matches)

        pos = QCursor.pos() + QPoint(15, 15)
        if self._last_popup_pos != pos:
            self.popup.move(pos)
            self._last_popup_pos = pos

        self.popup.show()


    def eventFilter(self, obj, event):
        # Souris quitte le tableau → on cache la popup
        if obj is self.ranking_viewport and event.type() == QEvent.Leave:
            self.popup.hide()
            self._last_popup_pos = None
            return False

        # Souris bouge DANS le tableau → popup suit sans jitter
        if obj is self.ranking_viewport and event.type() == QEvent.MouseMove:
            if self.popup.isVisible():
                pos = QCursor.pos() + QPoint(15, 15)
                if self._last_popup_pos != pos:
                    self.popup.move(pos)
                    self._last_popup_pos = pos
            return False

        return super().eventFilter(obj, event)