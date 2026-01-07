class Table:
	def __init__(self, table_id, players):
		self.id = table_id
		self.players = players
		self.results = {}

	def set_result(self, results):
		"""results = {player_id: points}"""
		self.results = results