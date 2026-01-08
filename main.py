from tournament import Tournament
from player import Player

tournoie = Tournament()

martin = Player("Marfin")
gael = Player("Le Hobbit")
audric = Player("Chouchouuu")
alexis = Player("Slivoid")

tournoie.add_player(martin)
tournoie.add_player(gael)
tournoie.add_player(audric)
tournoie.add_player(alexis)

tournoie.create_tables()

print(tournoie.players)

result = {"Marfin": 3, "Slivoid": 2, "Le Hobbit": 1, "Chouchouuu": 1}

tournoie.apply_result(1, result)

print(tournoie.tables[0].players)
print(tournoie.tables[0].result)