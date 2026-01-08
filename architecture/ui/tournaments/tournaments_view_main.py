from PySide6.QtWidgets import QWidget, QVBoxLayout
from ui.tournaments.upcoming_view import UpcomingTournamentsView
from ui.tournaments.launch_view import LaunchTournamentView
from ui.tournaments.historic_view import HistoricTournamentsView
from ui.tournaments.dialogs.create_tournament import CreateTournamentDialog



class TournamentViewMain(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # === DONNÉES PARTAGÉES (mock pour l’instant) ===
        self.upcoming_tournaments = [
            {"id": 1, "name": "Friday Night Magic", "date": "2024-10-04", "format": "Commander"},
            {"id": 2, "name": "Modern League", "date": "2024-10-11", "format": "Modern"},
        ]

        self.historic_tournaments = [
            {"id": 99, "name": "Commander Cup", "date": "2024-09-20", "winner": "Martin", "players": 24},
        ]

        self.active_tournament = None

        # === LAYOUT ===
        root = QVBoxLayout(self)
        root.setSpacing(30)
        root.setContentsMargins(0, 0, 0, 0)

        # === SOUS-VUES ===
        self.upcoming_view = UpcomingTournamentsView(self)
        self.launch_view = LaunchTournamentView(self)
        self.historic_view = HistoricTournamentsView(self)

        root.addWidget(self.upcoming_view)
        root.addWidget(self.launch_view)
        root.addWidget(self.historic_view)
        root.addStretch()

        # === LIAISONS ===
        self.upcoming_view.tournament_selected.connect(
            self.launch_view.set_selected_tournament
        )
        self.launch_view.tournament_launched.connect(
            self._on_tournament_launched
        )

        self.upcoming_view.create_requested.connect(
            self._open_create_tournament
        )

        self.upcoming_view.launch_requested.connect(
            self._launch_tournament
        )


        # Init
        self.upcoming_view.set_tournaments(self.upcoming_tournaments)
        self.historic_view.set_tournaments(self.historic_tournaments)

    # =================================================
    # LOGIQUE CENTRALE
    # =================================================
    def _on_tournament_launched(self, tournament: dict):
        self.active_tournament = tournament

        # retirer de "à venir"
        self.upcoming_tournaments = [
            t for t in self.upcoming_tournaments if t["id"] != tournament["id"]
        ]

        # (plus tard) → déplacer en historique quand terminé
        self.upcoming_view.set_tournaments(self.upcoming_tournaments)

    def _launch_tournament(self, tournament: dict):
        self.active_tournament = tournament

        # Retirer de "à venir"
        self.upcoming_tournaments = [
            t for t in self.upcoming_tournaments if t["id"] != tournament["id"]
        ]

        self.upcoming_view.set_tournaments(self.upcoming_tournaments)

        # Mettre à jour la colonne active
        self.active_view.set_tournament(tournament)

    def _open_create_tournament(self):
        dialog = CreateTournamentDialog(self)

        if dialog.exec() != dialog.accepted:
            return

        data = dialog.get_data()

        # ID simple (mock)
        new_id = max([t["id"] for t in self.upcoming_tournaments], default=0) + 1

        tournament = {
            "id": new_id,
            "name": data["name"],
            "format": data["format"],
            "date": data["date"],
            "players": data["players"],
        }

        self.upcoming_tournaments.append(tournament)
        self.upcoming_view.set_tournaments(self.upcoming_tournaments)
