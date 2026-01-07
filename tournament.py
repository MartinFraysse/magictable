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
		random.shuffle(self.players)

		table_id = 1
		for i in range(0, len(self.players), 4):
			group = self.players[i:i+4]
			table = Table(table_id, group)
			self.tables.append(table)
			table_id += 1

	def apply_result(self, table_id, result):
		table = next(t for t in self.tables if t.id == tables_id)
		table.set_result(results)

		for player in table.players:
			player.add_score(result[player.name])