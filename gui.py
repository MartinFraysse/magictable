import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askinteger
import random

from tournament import Tournament
from player import Player
from pairing_math import tournament_pairing_diagnostic


class TournamentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MTG Commander – Gestion de tournoi")
        self.root.geometry("1000x800")

        self.tournament = Tournament()
        self.round_number = 1

        # Buffer temporaire pour scores générés (non validés)
        self.generated_score_buffer = {}

        self._build_ui()

    # ================= UI ================= #

    def _build_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both")

        self.tab_players = ttk.Frame(notebook)
        self.tab_tables = ttk.Frame(notebook)
        self.tab_scores = ttk.Frame(notebook)
        self.tab_ranking = ttk.Frame(notebook)

        notebook.add(self.tab_players, text="Joueurs")
        notebook.add(self.tab_tables, text="Tables / Rounds")
        notebook.add(self.tab_scores, text="Scores")
        notebook.add(self.tab_ranking, text="Classement")

        self._build_players_tab()
        self._build_tables_tab()
        self._build_scores_tab()
        self._build_ranking_tab()

        self.update_ranking()

    # ================= Joueurs ================= #

    def _build_players_tab(self):
        frame = ttk.Frame(self.tab_players, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Nom du joueur").pack(anchor="w")

        self.player_name_entry = ttk.Entry(frame)
        self.player_name_entry.pack(fill="x", pady=5)
        self.player_name_entry.bind("<Return>", lambda e: self.add_player())

        ttk.Button(frame, text="Ajouter joueur", command=self.add_player).pack(pady=5)

        ttk.Button(
            frame,
            text="🎲 Générer joueurs aléatoires",
            command=self.generate_random_players
        ).pack(pady=5)

        self.players_list = tk.Listbox(frame)
        self.players_list.pack(fill="both", expand=True, pady=10)

    def add_player(self):
        name = self.player_name_entry.get().strip()
        if not name:
            return

        if any(p.name == name for p in self.tournament.players):
            messagebox.showwarning("Erreur", "Ce joueur existe déjà")
            return

        self.tournament.add_player(Player(name))
        self.players_list.insert(tk.END, name)

        self.player_name_entry.delete(0, tk.END)
        self.player_name_entry.focus()
        self.update_ranking()

    def generate_random_players(self):
        n = askinteger("Joueurs aléatoires", "Nombre de joueurs ?", minvalue=3, maxvalue=64)
        if not n:
            return

        self.tournament.players.clear()
        self.tournament.tables.clear()
        self.generated_score_buffer.clear()

        self.players_list.delete(0, tk.END)

        for i in range(1, n + 1):
            name = f"Joueur_{i}"
            self.tournament.add_player(Player(name))
            self.players_list.insert(tk.END, name)

        self.round_number = 1
        self.refresh_score_tab()
        self.update_ranking()

    # ================= Tables / Rounds ================= #

    def _build_tables_tab(self):
        frame = ttk.Frame(self.tab_tables, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Gestion des rounds", font=("Arial", 11, "bold")).pack(anchor="w")

        ttk.Button(frame, text="Créer tables (Round 1)", command=self.create_first_round).pack(pady=5)
        ttk.Button(frame, text="Round suivant", command=self.next_round).pack(pady=5)

        ttk.Button(
            frame,
            text="🎯 Générer scores aléatoires",
            command=self.generate_random_scores
        ).pack(pady=5)

        self.tables_text = tk.Text(frame, state="disabled", height=28)
        self.tables_text.pack(fill="both", expand=True)

    def create_first_round(self):
        try:
            self.tournament.create_tables()
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return

        self.round_number = 1
        self.generated_score_buffer.clear()
        self._refresh_tables_view()
        self.refresh_score_tab()

    def _build_score_groups(self):
        groups = {}
        for p in self.tournament.players:
            groups.setdefault(p.score, []).append(p)
        return groups

    def _estimate_table_sizes_for_group(self, size):
        if size in (0, 1, 2, 5):
            return []

        fours = size // 4
        rem = size % 4
        threes = 0

        if rem == 3:
            threes = 1
        elif rem == 2:
            fours -= 1
            threes = 2
        elif rem == 1:
            fours -= 2
            threes = 3

        return [4] * fours + [3] * threes

    def next_round(self):
        for table in self.tournament.tables:
            if not table.result:
                messagebox.showwarning(
                    "Round incomplet",
                    "Toutes les tables doivent être validées avant le round suivant."
                )
                return

        score_groups = self._build_score_groups()
        table_sizes_by_group = {
            score: self._estimate_table_sizes_for_group(len(players))
            for score, players in score_groups.items()
        }

        diagnostic = tournament_pairing_diagnostic(
            score_groups=score_groups,
            table_sizes_by_group=table_sizes_by_group,
            current_round=self.round_number
        )

        if diagnostic["recommend_switch"]:
            proceed = messagebox.askyesno(
                "Alerte pairing",
                "⚠️ Risque élevé de re-match détecté.\n\n"
                "Continuer en pairing par score ?"
            )
            if not proceed:
                return

        self.tournament.create_tables_by_score()
        self.round_number += 1
        self.generated_score_buffer.clear()
        self._refresh_tables_view()
        self.refresh_score_tab()

    def _refresh_tables_view(self):
        self.tables_text.config(state="normal")
        self.tables_text.delete("1.0", tk.END)

        self.tables_text.insert(tk.END, f"=== Round {self.round_number} ===\n\n")
        for table in self.tournament.tables:
            self.tables_text.insert(tk.END, f"Table {table.id}:\n")
            for p in table.players:
                self.tables_text.insert(tk.END, f"  - {p.name} ({p.score} pts)\n")
            self.tables_text.insert(tk.END, "\n")

        self.tables_text.config(state="disabled")

    # ================= Scores ================= #

    def _build_scores_tab(self):
        self.score_frame = ttk.Frame(self.tab_scores, padding=10)
        self.score_frame.pack(fill="both", expand=True)

    def refresh_score_tab(self):
        for w in self.score_frame.winfo_children():
            w.destroy()

        if not self.tournament.tables:
            ttk.Label(self.score_frame, text="Aucune table.").pack()
            return

        for table in self.tournament.tables:
            ttk.Label(
                self.score_frame,
                text=f"Table {table.id}",
                font=("Arial", 10, "bold")
            ).pack(anchor="w", pady=(10, 0))

            combos = {}
            ranks = list(range(1, len(table.players) + 1))

            for p in table.players:
                row = ttk.Frame(self.score_frame)
                row.pack(anchor="w")

                ttk.Label(row, text=p.name, width=20).pack(side="left")

                combo = ttk.Combobox(row, values=[str(r) for r in ranks], width=5)
                combo.pack(side="left")

                # Pré-remplissage depuis le buffer
                if table.id in self.generated_score_buffer:
                    rank = self.generated_score_buffer[table.id].get(p.name)
                    if rank:
                        combo.set(str(rank))

                combos[p.name] = combo

            ttk.Button(
                self.score_frame,
                text="Valider résultats",
                command=lambda t=table, c=combos: self.apply_results(t, c)
            ).pack(pady=5)

    def _points_from_rank(self, rank):
        if rank == 1:
            return 3
        if rank == 2:
            return 2
        return 1

    def apply_results(self, table, combos):
        try:
            ranks = [int(c.get()) for c in combos.values()]
        except ValueError:
            messagebox.showerror("Erreur", "Classements invalides")
            return

        if len(set(ranks)) != len(ranks):
            messagebox.showerror("Erreur", "Classements en double")
            return

        result = {}
        for name, combo in combos.items():
            result[name] = self._points_from_rank(int(combo.get()))

        self.tournament.apply_result(table.id, result)

        # Nettoyage du buffer une fois validé
        self.generated_score_buffer.pop(table.id, None)

        self.update_ranking()
        self.refresh_score_tab()

    def generate_random_scores(self):
        if not self.tournament.tables:
            messagebox.showwarning("Erreur", "Aucune table à scorer")
            return

        self.generated_score_buffer.clear()

        for table in self.tournament.tables:
            players = table.players[:]
            random.shuffle(players)

            table_buf = {}
            for idx, p in enumerate(players):
                table_buf[p.name] = idx + 1  # rang uniquement

            self.generated_score_buffer[table.id] = table_buf

        self.refresh_score_tab()

    # ================= Classement ================= #

    def _build_ranking_tab(self):
        self.ranking_tree = ttk.Treeview(
            self.tab_ranking,
            columns=("rank", "name", "score"),
            show="headings"
        )
        self.ranking_tree.pack(fill="both", expand=True)

        self.ranking_tree.heading("rank", text="#")
        self.ranking_tree.heading("name", text="Joueur")
        self.ranking_tree.heading("score", text="Score")

    def update_ranking(self):
        for r in self.ranking_tree.get_children():
            self.ranking_tree.delete(r)

        players = sorted(self.tournament.players, key=lambda p: p.score, reverse=True)
        for i, p in enumerate(players, start=1):
            self.ranking_tree.insert("", "end", values=(i, p.name, p.score))


# ================= MAIN ================= #

if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentGUI(root)
    root.mainloop()
