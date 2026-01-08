from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton,
    QLabel, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from ui.widgets.down_only_combo_box import DownOnlyComboBox


class CreateTournamentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Nouveau tournoi")
        self.setModal(True)
        self.setFixedSize(380, 380)
        self.setObjectName("CreateTournamentDialog")

        root = QVBoxLayout(self)
        root.setSpacing(18)
        root.setContentsMargins(20, 20, 20, 20)

        # =====================
        # Title
        # =====================
        title = QLabel("🏆 Nouveau tournoi")
        title.setObjectName("DialogTitle")
        root.addWidget(title)

        # =====================
        # Name
        # =====================
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom du tournoi")
        self.name_input.textChanged.connect(self._update_preview)
        root.addWidget(self.name_input)

        # =====================
        # Format + Date
        # =====================
        row = QHBoxLayout()
        row.setSpacing(12)

        self.format_input = DownOnlyComboBox()
        self.format_input.addItems([
            "Commander", "Draft", "AP Magic",
            "Pokemon ?", "Rise ?"
        ])
        self.format_input.currentTextChanged.connect(self._update_preview)

        self.date_input = QLineEdit()
        self.date_input.setInputMask("00/00/0000;_")
        self.date_input.setFixedWidth(110)
        self.date_input.setAlignment(Qt.AlignCenter)

        row.addWidget(self.format_input)
        row.addWidget(self.date_input)
        root.addLayout(row)

        # =====================
        # Players
        # =====================
        players_frame = QFrame()
        players_frame.setObjectName("InlineFrame")

        players_layout = QHBoxLayout(players_frame)
        players_layout.setContentsMargins(12, 8, 12, 8)

        players_icon = QLabel("👥 ")
        players_icon.setObjectName("PlayersIcon")

        players_label = QLabel("Joueurs max")
        players_label.setObjectName("PlayersLabel")

        self.players_input = QLineEdit("24")
        self.players_input.setObjectName("PlayersInput")
        self.players_input.setValidator(QIntValidator(2, 128, self))
        self.players_input.setFixedWidth(60)
        self.players_input.setAlignment(Qt.AlignRight)
        self.players_input.textChanged.connect(self._update_preview)
        self.players_input.setAttribute(Qt.WA_StyledBackground, True)

        players_layout.addWidget(players_icon)
        players_layout.addWidget(players_label)
        players_layout.addStretch()
        players_layout.addWidget(self.players_input)

        root.addWidget(players_frame)

        # =====================
        # Preview
        # =====================
        self.preview = QLabel()
        self.preview.setObjectName("TournamentPreview")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setWordWrap(True)
        self.preview.setMinimumHeight(70)
        root.addWidget(self.preview)

        root.addStretch()

        # =====================
        # Actions
        # =====================
        actions = QHBoxLayout()
        actions.addStretch()

        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.setObjectName("CancelButton")
        self.cancel_btn.clicked.connect(self.reject)

        self.create_btn = QPushButton("Créer")
        self.create_btn.setObjectName("CreateButton")
        self.create_btn.setEnabled(False)
        self.create_btn.clicked.connect(self._validate)

        actions.addWidget(self.cancel_btn)
        actions.addWidget(self.create_btn)
        root.addLayout(actions)

        self._update_preview()

    # =====================
    # Logic
    # =====================
    def _update_preview(self):
        name = self.name_input.text().strip()
        self.create_btn.setEnabled(bool(name))

        self.preview.setText(
            f"<b>{name or 'Nom du tournoi'}</b><br>"
            f"{self.format_input.currentText()} • "
            f"{self.date_input.text()} • "
            f"{self.players_input.text()} joueurs"
        )

    def _validate(self):
        if len(self.date_input.text()) != 10:
            self.date_input.setFocus()
            return
        self.accept()

    def get_data(self):
        return {
            "name": self.name_input.text(),
            "format": self.format_input.currentText(),
            "date": self.date_input.text(),
            "players": int(self.players_input.text()),
        }
