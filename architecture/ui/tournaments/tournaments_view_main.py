from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)
from PySide6.QtCore import Qt

from ui.tournaments.upcoming_view import UpcomingView
from ui.tournaments.launch_view import LaunchView
from ui.tournaments.historic_view import HistoricView


class TournamentViewMain(QWidget):
    """
    Vue principale de la page Tournament.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("TournamentViewMain")

        self._build_ui()

    # =========================
    # UI
    # =========================
    def _build_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(20)

        # =========================
        # Top area (Upcoming | Launch)
        # =========================
        top_container = QFrame()
        top_container.setObjectName("TournamentTopContainer")
        top_container.setAttribute(Qt.WA_StyledBackground, True)

        top_layout = QHBoxLayout(top_container)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(20)

        # === Upcoming (LEFT)
        self.upcoming_container = self._build_upcoming_container()
        top_layout.addWidget(self.upcoming_container, 1)

        # === Launch (RIGHT)
        self.launch_container = self._build_launch_container()
        top_layout.addWidget(self.launch_container, 2)

        root_layout.addWidget(top_container, 1)

        # =========================
        # Bottom area (Historic)
        # =========================
        self.historic_container = self._build_historic_container()
        root_layout.addWidget(self.historic_container, 0)

    # =========================
    # Sub-containers
    # =========================
    def _build_upcoming_container(self):
        frame = QFrame()
        frame.setObjectName("UpcomingContainer")
        frame.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)

        self.upcoming_view = UpcomingView(self)
        layout.addWidget(self.upcoming_view)

        return frame

    def _build_launch_container(self):
        frame = QFrame()
        frame.setObjectName("LaunchContainer")
        frame.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)

        self.launch_view = LaunchView(self)
        layout.addWidget(self.launch_view)

        return frame

    def _build_historic_container(self):
        frame = QFrame()
        frame.setObjectName("HistoricContainer")
        frame.setAttribute(Qt.WA_StyledBackground, True)
        frame.setMaximumHeight(72)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)

        # 🔥 Intégration réelle de HistoricView
        self.historic_view = HistoricView(self)
        layout.addWidget(self.historic_view)

        return frame
