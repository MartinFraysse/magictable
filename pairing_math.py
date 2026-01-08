"""
pairing_math.py

Analyse mathématique des risques de re-match
pour tournois multi-joueurs (tables de 3 / 4).
"""


# =========================
# BASES
# =========================

def average_opponents_per_round(table_sizes):
    if not table_sizes:
        return 0.0
    return sum(size - 1 for size in table_sizes) / len(table_sizes)


def max_clean_rounds(group_size, avg_opponents):
    if group_size <= 1 or avg_opponents <= 0:
        return 0.0
    return (group_size - 1) / avg_opponents


# =========================
# ANALYSE DE GROUPE
# =========================

def group_rematch_pressure(group_size, table_sizes, current_round, safety_margin=1):
    avg_opponents = average_opponents_per_round(table_sizes)
    max_rounds = max_clean_rounds(group_size, avg_opponents)

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
# ANALYSE GLOBALE
# =========================

def tournament_pairing_diagnostic(score_groups, table_sizes_by_group, current_round):
    details = {}
    pressures = []

    for score, players in score_groups.items():
        group_size = len(players)
        table_sizes = table_sizes_by_group.get(score, [])

        diag = group_rematch_pressure(
            group_size=group_size,
            table_sizes=table_sizes,
            current_round=current_round
        )

        details[score] = diag
        pressures.append(diag["pressure"])

    if "high" in pressures:
        global_pressure = "high"
        recommend = True
    elif "medium" in pressures:
        global_pressure = "medium"
        recommend = True
    else:
        global_pressure = "low"
        recommend = False

    return {
        "global_pressure": global_pressure,
        "recommend_switch": recommend,
        "details": details
    }
14