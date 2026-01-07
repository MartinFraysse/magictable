def commender_scoring(result):
	"""player list from 1st to 4th"""
	"""exemple lst: ["player1", "player2", "player3", "player4"]"""
	points =[3,2,1,1]
	return {player.name: points[i] for i, player in enumerate(result)}