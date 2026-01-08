from player import Player
from table import Table
import random

class Tournament:
	def __init__(self):
		self.players = []
		self.tables = []

	def add_player(self, player):
		self.players.append(player)

	def create_tables(self):
	    import random
	    random.shuffle(self.players)

	    n = len(self.players)
	    if n in (0, 1, 2, 5):
	        raise ValueError(f"Répartition impossible pour {n} joueur(s) sans table de 2 ou 5.")

	    fours = n // 4
	    rem = n % 4
	    threes = 0

	    if rem == 0:
	        pass
	    elif rem == 3:
	        threes = 1
	    elif rem == 2:
	        # 4+2 -> 3+3 (donc on remplace 1 table de 4 par 2 tables de 3)
	        if fours < 1:
	            raise ValueError(f"Répartition impossible pour {n} joueur(s).")
	        fours -= 1
	        threes = 2
	    elif rem == 1:
	        # 4+4+1 -> 3+3+3 (donc on remplace 2 tables de 4 par 3 tables de 3)
	        if fours < 2:
	            raise ValueError(f"Répartition impossible pour {n} joueur(s).")
	        fours -= 2
	        threes = 3

	    sizes = [4] * fours + [3] * threes
	    # (optionnel) mélanger l'ordre des tailles pour éviter que les 3 soient toujours à la fin
	    # random.shuffle(sizes)

	    self.tables.clear()
	    table_id = 1
	    idx = 0
	    for sz in sizes:
	        group = self.players[idx:idx + sz]
	        self.tables.append(Table(table_id, group))
	        idx += sz
	        table_id += 1

	def create_tables_by_score(self):
	    """
	    Crée les tables pour un nouveau round
	    en groupant les joueurs par score décroissant.
	    """
	    # 1) Trier par score (desc)
	    players_sorted = sorted(self.players, key=lambda p: p.score, reverse=True)

	    n = len(players_sorted)
	    if n in (0, 1, 2, 5):
	        raise ValueError(f"Répartition impossible pour {n} joueurs")

	    # 2) Calcul des tailles (4 / 3)
	    fours = n // 4
	    rem = n % 4
	    threes = 0

	    if rem == 0:
	        pass
	    elif rem == 3:
	        threes = 1
	    elif rem == 2:
	        if fours < 1:
	            raise ValueError("Répartition impossible")
	        fours -= 1
	        threes = 2
	    elif rem == 1:
	        if fours < 2:
	            raise ValueError("Répartition impossible")
	        fours -= 2
	        threes = 3

	    sizes = [4] * fours + [3] * threes

	    # 3) Création des tables
	    self.tables.clear()
	    idx = 0
	    table_id = 1

	    for size in sizes:
	        group = players_sorted[idx:idx + size]
	        self.tables.append(Table(table_id, group))
	        idx += size
	        table_id += 1


	def apply_result(self, table_id, result):
		table = next(t for t in self.tables if t.id == table_id)
		table.set_result(result)

		for player in table.players:
			player.add_score(result[player.name])