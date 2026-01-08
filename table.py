class Table:
	def __init__(self, table_id, players):
		self.id = table_id
		self.players = players
		self.result = {}

	def set_result(self, result):
		"""results = {player_id: points}"""
		self.result = result