"""
pairing_math.py

Module de calculs et heuristiques pour le pairing de tournois
multi-joueurs (Commander, tables de 3 / 4).

AUCUNE dépendance UI.
Aucune logique métier (pas de création de tables ici).
Uniquement de l'analyse et des recommandations.
"""


# =========================
# BASES MATHÉMATIQUES
# =========================

def average_opponents_per_round(table_sizes):
    """
    Calcule le nombre moyen d'adversaires rencontrés par round.

    table_sizes : liste de tailles de tables (ex: [4,4,3])

    Retour :
        float : adversaires moyens par round
    """
    if not table_sizes:
        return 0.0

    total = 0
    for size in table_sizes:
        total += (size - 1)

    return total / len(table_sizes)


def max_clean_rounds(group_size, avg_opponents):
    """
    Estime le nombre de rounds possibles avant saturation complète
    (tous les adversaires potentiels rencontrés).

    group_size : nombre de joueurs dans le groupe
    avg_opponents : adversaires rencontrés par round

    Retour :
        float : nombre de rounds "propres" théoriques
    """
    if group_size <= 1 or avg_opponents <= 0:
        return 0.0

    return (group_size - 1) / avg_opponents


# =========================
# ANALYSE DE SATURATION
# =========================

def player_remaining_opponents(total_players, already_met):
    """
    Nombre d'adversaires encore possibles pour un joueur.

    total_players : nombre total de joueurs du tournoi
    already_met : nombre d'adversaires uniques déjà rencontrés

    Retour :
        int
    """
    return max(0, (total_players - 1) - already_met)


def will_force_rematch(remaining_opponents, opponents_per_round):
    """
    Détermine si un re-match est mathématiquement inévitable
    au prochain round.

    Retour :
        bool
    """
    return remaining_opponents < opponents_per_round


# =========================
# DIAGNOSTIC DE GROUPE
# =========================

def group_rematch_pressure(
    group_size,
    table_sizes,
    current_round,
    safety_margin=1
):
    """
    Analyse la pression de re-match dans un groupe de score.

    group_size : nombre de joueurs dans le groupe
    table_sizes : tailles des tables prévues dans ce groupe
    current_round : numéro du round actuel (1-based)
    safety_margin : marge avant saturation (par défaut 1 round)

    Retour :
        dict {
            "avg_opponents": float,
            "max_clean_rounds": float,
            "pressure": str ("low", "medium", "high"),
            "recommend_switch": bool
        }
    """
    avg_opponents = average_opponents_per_round(table_sizes)
    max_rounds = max_clean_rounds(group_size, avg_opponents)

    # Pression qualitative
    if current_round < max_rounds - safety_margin:
        pressure = "low"
        recommend = False
    elif current_round < max_rounds:
        pressure = "medium"
        recommend = True
    else:
        pressure = "high"
        recommend = True

    return {
        "avg_opponents": round(avg_opponents, 2),
        "max_clean_rounds": round(max_rounds, 2),
        "pressure": pressure,
        "recommend_switch": recommend
    }


# =========================
# DIAGNOSTIC GLOBAL
# =========================

def tournament_pairing_diagnostic(
    score_groups,
    table_sizes_by_group,
    current_round
):
    """
    Analyse globale du tournoi pour décider si
    le pairing par score devient risqué.

    score_groups : dict {score_value: [players]}
    table_sizes_by_group : dict {score_value: [4,4,3]}
    current_round : numéro du round

    Retour :
        dict {
            "global_pressure": "low|medium|high",
            "recommend_switch": bool,
            "details": {score: diagnostic}
        }
    """
    details = {}
    pressures = []

    for score, players in score_groups.items():
        group_size = len(players)
        table_sizes = t_
