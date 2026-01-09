from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
)
from PySide6.QtCore import Qt



class LaunchView(QWidget):
    """
    Vue de lancement d’un tournoi.

    Responsabilités :
    - Accueillir un tournoi depuis Upcoming
    - Afficher l’interface de préparation / lancement
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("LaunchView")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._build_ui()

    # =========================
    # UI
    # =========================
    def _build_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        container = QFrame()
        container.setObjectName("LaunchContainerInner")
        container.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)

        title = QLabel("🎮 Lancer un tournoi")
        title.setObjectName("LaunchTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel(
            "Sélectionnez ou déposez un tournoi\n"
            "depuis la liste des tournois à venir"
        )
        subtitle.setObjectName("LaunchSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        root_layout.addWidget(container, 1)
