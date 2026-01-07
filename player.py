class Player:
	def __init__(self, name):
		self.name = name
		self.score = 0
		self.tables_played = []

	def add_score(self, point):
		self.score += point