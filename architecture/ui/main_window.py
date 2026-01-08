from PySide6.QtWidgets import (
    QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame,
    QGraphicsDropShadowEffect,
    QProgressBar, QButtonGroup
)
from PySide6.QtCore import Qt, QPropertyAnimation, QRect
from PySide6.QtGui import QColor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MagicTable — Tournament Manager")
        # Taille standard de référence
        self.resize(1920, 1080)

        # Taille minimale (sécurité layout)
        self.setMinimumSize(1920, 1080)

        # Fenêtre flottante (Wayland / Hyprland friendly)
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowCloseButtonHint
        )


        screen = self.screen().availableGeometry()
        window = self.frameGeometry()
        window.moveCenter(screen.center())
        self.move(window.topLeft())

        self.animations = []

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._sidebar())
        root.addWidget(self._main_area())

    # -------- Sidebar --------
    def _sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(260)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        logo = QLabel("🟢  MagicTable")
        logo.setObjectName("Logo")
        layout.addWidget(logo)

        layout.addSpacing(30)

        self.nav_group = QButtonGroup()
        self.nav_group.setExclusive(True)

        for icon, name in [
            ("📊", "Dashboard"),
            ("🏆", "Tournois"),
            ("👥", "Joueurs"),
            ("⚔️", "Matchs"),
            ("⚙️", "Paramètres"),
        ]:
            btn = QPushButton(f"{icon}  {name}")
            btn.setObjectName("NavButton")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(44)

            self.nav_group.addButton(btn)
            layout.addWidget(btn)

        self.nav_group.buttons()[0].setChecked(True)

        layout.addStretch()

        quit_btn = QPushButton("⏻  Quitter")
        quit_btn.setObjectName("QuitButton")
        quit_btn.setMinimumHeight(44)
        layout.addWidget(quit_btn)

        return sidebar

    # -------- Main area --------
    def _main_area(self):
        area = QWidget()
        layout = QVBoxLayout(area)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        layout.addWidget(self._header())

        content = QFrame()
        content.setObjectName("ContentArea")
        layout.addWidget(content)

        return area

    # -------- Header --------
    def _header(self):
        header = QFrame()
        header.setObjectName("Header")

        layout = QHBoxLayout(header)
        layout.setSpacing(20)

        cards = [
            ("🟢", "État du tournoi", "En cours", 65),
            ("👥", "Joueurs", "24", 80),
            ("⚔️", "Matchs", "5", 40),
            ("📅", "Prochaine ronde", "14:30", 100),
        ]

        for icon, title, value, progress in cards:
            card = self._stat_card(icon, title, value, progress)
            layout.addWidget(card)
            self._animate_card(card)

        return header

    def _stat_card(self, icon, title, value, progress_value):
        card = QFrame()
        card.setObjectName("StatCard")
        card.setCursor(Qt.PointingHandCursor)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(35)
        shadow.setYOffset(12)
        shadow.setColor(QColor(0, 0, 0, 180))
        card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(card)
        layout.setSpacing(6)

        i = QLabel(icon)
        i.setObjectName("StatIcon")

        val = QLabel(value)
        val.setObjectName("StatValue")

        t = QLabel(title)
        t.setObjectName("StatTitle")

        progress = QProgressBar()
        progress.setObjectName("StatProgress")
        progress.setRange(0, 100)
        progress.setValue(progress_value)
        progress.setFixedHeight(6)
        progress.setTextVisible(False)

        layout.addWidget(i)
        layout.addWidget(val)
        layout.addWidget(t)
        layout.addWidget(progress)

        return card

    def _animate_card(self, card):
        anim = QPropertyAnimation(card, b"geometry")
        anim.setDuration(600)

        g = card.geometry()
        anim.setStartValue(QRect(g.x(), g.y() + 30, g.width(), g.height()))
        anim.setEndValue(g)

        anim.start()
        self.animations.append(anim)
