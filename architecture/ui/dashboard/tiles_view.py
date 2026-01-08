from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy


class DashboardTilesView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
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

    def _tile(self, icon, title, value):
        frame = QFrame()
        frame.setObjectName("DashboardTile")
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout(frame)
        layout.setSpacing(4)
        layout.setContentsMargins(16, 16, 16, 16)

        # === ACCENT VISUEL (Qt-native) ===
        accent = QFrame()
        accent.setObjectName("DashboardTileAccent")
        accent.setFixedWidth(4)
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

    def set_timer_text(self, value: str):
        self.tile_timer.value_label.setText(value)
