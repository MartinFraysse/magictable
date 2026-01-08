from PySide6.QtWidgets import (
    QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame,
    QButtonGroup, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStackedWidget
from ui.dashboard_view import DashboardView
from ui.tournaments_view import TournamentsView
from ui.players_view import PlayersView
from ui.matches_view import MatchesView
from ui.settings_view import SettingsView
from ui.dashboard_view import DashboardView



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MagicTable — Tournament Manager")

        # Taille standard
        self.resize(1280, 800)
        self.setMinimumSize(1280, 800)

        # === CENTRAL ROOT ===
        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # === SIDEBAR ===
        self.sidebar = self._build_sidebar()
        root_layout.addWidget(self.sidebar)

        # === CONTENT CONTAINER ===
        self.content_container = self._build_content_container()
        root_layout.addWidget(self.content_container)

        # === CONNECT NAVIGATION ===
        for index, btn in enumerate(self.nav_buttons):
            btn.clicked.connect(lambda checked, i=index: self.stack.setCurrentIndex(i))

    # ========================
    # Sidebar
    # ========================
    def _build_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(260)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Logo
        logo = QLabel("🟢  MagicTable")
        logo.setObjectName("Logo")
        layout.addWidget(logo)

        layout.addSpacing(30)

        # Navigation
        self.nav_group = QButtonGroup()
        self.nav_group.setExclusive(True)

        self.nav_buttons = []

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
            btn.setMinimumHeight(44)
            btn.setCursor(Qt.PointingHandCursor)

            self.nav_group.addButton(btn)
            self.nav_buttons.append(btn)
            layout.addWidget(btn)


        # Actif par défaut
        self.nav_group.buttons()[0].setChecked(True)

        layout.addStretch()

        quit_btn = QPushButton("⏻  Quitter")
        quit_btn.setObjectName("QuitButton")
        quit_btn.setMinimumHeight(44)
        layout.addWidget(quit_btn)

        return sidebar

    # ========================
    # Content container
    # ========================
    def _build_content_container(self):
        container = QFrame()
        container.setObjectName("ContentContainer")

        container.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(0)

        # === STACK DE VUES ===
        self.stack = QStackedWidget()

        self.dashboard_view = DashboardView()
        self.tournaments_view = TournamentsView()
        self.players_view = PlayersView()
        self.matches_view = MatchesView()
        self.settings_view = SettingsView()

        self.stack.addWidget(self.dashboard_view)   # index 0
        self.stack.addWidget(self.tournaments_view) # index 1
        self.stack.addWidget(self.players_view)     # index 2
        self.stack.addWidget(self.matches_view)     # index 3
        self.stack.addWidget(self.settings_view)    # index 4

        layout.addWidget(self.stack)

        return container
