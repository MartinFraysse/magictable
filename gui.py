import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass

# -----------------------------
# Données mock (VISUEL UNIQUEMENT)
# -----------------------------
@dataclass
class MockPlayer:
    name: str
    score: int = 0

@dataclass
class MockTable:
    table_id: int
    players: list[str]
    result: dict[str, int] | None = None


# -----------------------------
# App UI
# -----------------------------
class PairingApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("TableMagic — Tournament Pairing (Mockup)")
        self.geometry("1200x720")
        self.minsize(1100, 650)

        # Mock state
        self.round_number = 1
        self.players: list[MockPlayer] = [
            MockPlayer("Martin", 3),
            MockPlayer("Audric", 1),
            MockPlayer("Gaël", 0),
            MockPlayer("Alexis", 2),
        ]
        self.tables: list[MockTable] = [
            MockTable(1, ["Martin", "Alexis", "Audric", "Gaël"])
        ]

        # Theme colors
        self.C_BG = "#0b1220"
        self.C_PANEL = "#0f1a2e"
        self.C_PANEL_2 = "#0c1629"
        self.C_TEXT = "#e6eefc"
        self.C_MUTED = "#a7b3cc"
        self.C_ACCENT = "#7c5cff"
        self.C_ACCENT_2 = "#22c55e"
        self.C_WARN = "#f59e0b"
        self.C_DANGER = "#ef4444"
        self.C_LINE = "#1c2a44"

        self.configure(bg=self.C_BG)

        self._setup_style()
        self._build_layout()
        self._show_page("players")

    # -----------------------------
    # Style ttk (Treeview etc.)
    # -----------------------------
    def _setup_style(self):
        style = ttk.Style(self)

        # On reste neutre côté theme ttk, on force nos couleurs
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background=self.C_BG)
        style.configure("TLabel", background=self.C_BG, foreground=self.C_TEXT)
        style.configure("Muted.TLabel", background=self.C_BG, foreground=self.C_MUTED)

        style.configure("Panel.TFrame", background=self.C_PANEL)
        style.configure("Panel2.TFrame", background=self.C_PANEL_2)

        style.configure("TSeparator", background=self.C_LINE)

        style.configure(
            "Treeview",
            background=self.C_PANEL_2,
            fieldbackground=self.C_PANEL_2,
            foreground=self.C_TEXT,
            rowheight=28,
            bordercolor=self.C_LINE,
            lightcolor=self.C_LINE,
            darkcolor=self.C_LINE,
        )
        style.configure(
            "Treeview.Heading",
            background=self.C_PANEL,
            foreground=self.C_TEXT,
            relief="flat",
        )
        style.map("Treeview.Heading", background=[("active", self.C_PANEL)])

    # -----------------------------
    # UI building
    # -----------------------------
    def _build_layout(self):
        # Root grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = tk.Frame(self, bg=self.C_PANEL, width=260)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        # Main container
        self.main = tk.Frame(self, bg=self.C_BG)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_rowconfigure(1, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

        self._build_sidebar()
        self._build_header()
        self._build_pages()

    def _build_sidebar(self):
        # Logo area
        logo_wrap = tk.Frame(self.sidebar, bg=self.C_PANEL)
        logo_wrap.pack(fill="x", padx=18, pady=(18, 10))

        canvas = tk.Canvas(logo_wrap, width=56, height=56, bg=self.C_PANEL, highlightthickness=0)
        canvas.pack(side="left")

        # Simple "logo" (cards + spark)
        canvas.create_oval(6, 6, 50, 50, fill=self.C_ACCENT, outline="")
        canvas.create_rectangle(20, 16, 42, 42, fill=self.C_PANEL, outline="")
        canvas.create_line(28, 18, 28, 40, fill=self.C_TEXT, width=2)
        canvas.create_line(34, 18, 34, 40, fill=self.C_TEXT, width=2)
        canvas.create_line(22, 28, 40, 28, fill=self.C_TEXT, width=2)

        title_wrap = tk.Frame(logo_wrap, bg=self.C_PANEL)
        title_wrap.pack(side="left", padx=12)

        tk.Label(
            title_wrap, text="TableMagic", bg=self.C_PANEL, fg=self.C_TEXT,
            font=("TkDefaultFont", 16, "bold")
        ).pack(anchor="w")
        tk.Label(
            title_wrap, text="Pairing & Scores", bg=self.C_PANEL, fg=self.C_MUTED,
            font=("TkDefaultFont", 10)
        ).pack(anchor="w")

        # Divider
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=18, pady=12)

        # Nav buttons
        self.nav_buttons = {}
        nav = [
            ("players", "👤  Joueurs", "Ajouter / gérer les joueurs"),
            ("tables",  "🪑  Tables", "Créer / afficher les tables"),
            ("results", "✅  Résultats", "Saisir les points par table"),
            ("standings", "🏆  Classement", "Voir le classement"),
        ]

        for key, label, hint in nav:
            btn = self._nav_button(self.sidebar, label, hint, lambda k=key: self._show_page(k))
            btn.pack(fill="x", padx=14, pady=6)
            self.nav_buttons[key] = btn

        # Bottom status
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=18, pady=12)
        self.sidebar_status = tk.Label(
            self.sidebar, text="● Ready", bg=self.C_PANEL, fg=self.C_ACCENT_2,
            font=("TkDefaultFont", 10, "bold")
        )
        self.sidebar_status.pack(anchor="w", padx=18, pady=(0, 18))

    def _nav_button(self, parent, text, hint, command):
        wrap = tk.Frame(parent, bg=self.C_PANEL)
        btn = tk.Button(
            wrap,
            text=text,
            command=command,
            bg=self.C_PANEL,
            fg=self.C_TEXT,
            activebackground=self.C_PANEL_2,
            activeforeground=self.C_TEXT,
            relief="flat",
            bd=0,
            padx=14,
            pady=10,
            anchor="w",
            font=("TkDefaultFont", 11, "bold")
        )
        btn.pack(fill="x")

        hint_lbl = tk.Label(
            wrap, text=hint, bg=self.C_PANEL, fg=self.C_MUTED,
            font=("TkDefaultFont", 9)
        )
        hint_lbl.pack(fill="x", padx=14, pady=(0, 10), anchor="w")

        # Hover effect
        def on_enter(_):
            btn.configure(bg=self.C_PANEL_2)
            hint_lbl.configure(bg=self.C_PANEL_2)
            wrap.configure(bg=self.C_PANEL_2)

        def on_leave(_):
            if getattr(wrap, "_active", False):
                return
            btn.configure(bg=self.C_PANEL)
            hint_lbl.configure(bg=self.C_PANEL)
            wrap.configure(bg=self.C_PANEL)

        wrap.bind("<Enter>", on_enter)
        wrap.bind("<Leave>", on_leave)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        hint_lbl.bind("<Enter>", on_enter)
        hint_lbl.bind("<Leave>", on_leave)

        wrap._btn = btn
        wrap._hint = hint_lbl
        wrap._active = False
        return wrap

    def _set_nav_active(self, key: str):
        for k, wrap in self.nav_buttons.items():
            active = (k == key)
            wrap._active = active
            bg = self.C_PANEL_2 if active else self.C_PANEL
            wrap.configure(bg=bg)
            wrap._btn.configure(bg=bg)
            wrap._hint.configure(bg=bg)
            # accent left bar
            # (simple illusion via border using highlightbackground is unreliable on tk.Button)
            # so we just change text color subtly
            wrap._btn.configure(fg=self.C_ACCENT if active else self.C_TEXT)

    def _build_header(self):
        self.header = tk.Frame(self.main, bg=self.C_BG)
        self.header.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 10))
        self.header.grid_columnconfigure(0, weight=1)

        left = tk.Frame(self.header, bg=self.C_BG)
        left.grid(row=0, column=0, sticky="w")

        self.h_title = tk.Label(
            left, text="Tournament Dashboard",
            bg=self.C_BG, fg=self.C_TEXT,
            font=("TkDefaultFont", 18, "bold")
        )
        self.h_title.pack(anchor="w")

        self.h_sub = tk.Label(
            left, text=f"Round {self.round_number} • 4 players • 1 table",
            bg=self.C_BG, fg=self.C_MUTED,
            font=("TkDefaultFont", 10)
        )
        self.h_sub.pack(anchor="w", pady=(2, 0))

        right = tk.Frame(self.header, bg=self.C_BG)
        right.grid(row=0, column=1, sticky="e")

        self.btn_new_round = tk.Button(
            right, text="➕ Nouveau round",
            command=self._mock_new_round,
            bg=self.C_ACCENT, fg="white",
            activebackground=self.C_ACCENT, activeforeground="white",
            relief="flat", bd=0, padx=14, pady=10,
            font=("TkDefaultFont", 10, "bold")
        )
        self.btn_new_round.pack(side="left", padx=(0, 10))

        self.btn_export = tk.Button(
            right, text="⤓ Export (mock)",
            command=lambda: self._toast("Export à brancher plus tard."),
            bg=self.C_PANEL, fg=self.C_TEXT,
            activebackground=self.C_PANEL_2, activeforeground=self.C_TEXT,
            relief="flat", bd=0, padx=14, pady=10,
            font=("TkDefaultFont", 10, "bold")
        )
        self.btn_export.pack(side="left")

    def _build_pages(self):
        self.pages_container = tk.Frame(self.main, bg=self.C_BG)
        self.pages_container.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        self.pages_container.grid_rowconfigure(0, weight=1)
        self.pages_container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        self.pages["players"] = self._page_players(self.pages_container)
        self.pages["tables"] = self._page_tables(self.pages_container)
        self.pages["results"] = self._page_results(self.pages_container)
        self.pages["standings"] = self._page_standings(self.pages_container)

        for p in self.pages.values():
            p.grid(row=0, column=0, sticky="nsew")

    # -----------------------------
    # Pages
    # -----------------------------
    def _card(self, parent, title: str, subtitle: str | None = None):
        outer = tk.Frame(parent, bg=self.C_PANEL, bd=0, highlightthickness=1, highlightbackground=self.C_LINE)
        outer.pack(fill="x", pady=10)

        head = tk.Frame(outer, bg=self.C_PANEL)
        head.pack(fill="x", padx=14, pady=(12, 8))
        tk.Label(head, text=title, bg=self.C_PANEL, fg=self.C_TEXT, font=("TkDefaultFont", 12, "bold")).pack(anchor="w")
        if subtitle:
            tk.Label(head, text=subtitle, bg=self.C_PANEL, fg=self.C_MUTED, font=("TkDefaultFont", 9)).pack(anchor="w", pady=(2, 0))

        body = tk.Frame(outer, bg=self.C_PANEL)
        body.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        return outer, body

    def _page_players(self, parent):
        page = tk.Frame(parent, bg=self.C_BG)
        page.grid_columnconfigure(0, weight=1)

        _, body = self._card(page, "Ajouter des joueurs", "Saisie simple — logique à brancher plus tard")
        form = tk.Frame(body, bg=self.C_PANEL)
        form.pack(fill="x")

        tk.Label(form, text="Nom du joueur", bg=self.C_PANEL, fg=self.C_MUTED).grid(row=0, column=0, sticky="w")
        self.player_name_var = tk.StringVar()
        entry = tk.Entry(form, textvariable=self.player_name_var, bg=self.C_PANEL_2, fg=self.C_TEXT,
                         insertbackground=self.C_TEXT, relief="flat")
        entry.grid(row=1, column=0, sticky="ew", pady=(6, 0), ipady=8)
        form.grid_columnconfigure(0, weight=1)

        btn_add = tk.Button(
            form, text="Ajouter", command=self._mock_add_player,
            bg=self.C_ACCENT_2, fg="white", relief="flat", bd=0, padx=14, pady=10,
            activebackground=self.C_ACCENT_2, activeforeground="white",
            font=("TkDefaultFont", 10, "bold")
        )
        btn_add.grid(row=1, column=1, padx=(10, 0), sticky="e")

        _, body2 = self._card(page, "Liste des joueurs", "Double-clic plus tard pour éditer / supprimer")
        self.players_tv = ttk.Treeview(body2, columns=("score",), show="headings", height=9)
        self.players_tv.heading("score", text="Score")
        self.players_tv.column("score", width=120, anchor="center")
        self.players_tv.pack(fill="both", expand=True)

        self._refresh_players()
        return page

    def _page_tables(self, parent):
        page = tk.Frame(parent, bg=self.C_BG)
        page.grid_columnconfigure(0, weight=1)

        _, body = self._card(page, "Création de table automatique", "Boutons mock — l’algorithme viendra après")
        row = tk.Frame(body, bg=self.C_PANEL)
        row.pack(fill="x")

        btn = tk.Button(
            row, text="🎲 Générer les tables (mock)",
            command=self._mock_generate_tables,
            bg=self.C_ACCENT, fg="white", relief="flat", bd=0, padx=14, pady=10,
            activebackground=self.C_ACCENT, activeforeground="white",
            font=("TkDefaultFont", 10, "bold")
        )
        btn.pack(side="left")

        btn2 = tk.Button(
            row, text="⚠ Diagnostic risque (mock)",
            command=lambda: self._toast("Diagnostic à brancher plus tard (pairing math)."),
            bg=self.C_PANEL_2, fg=self.C_TEXT, relief="flat", bd=0, padx=14, pady=10,
            activebackground=self.C_PANEL_2, activeforeground=self.C_TEXT,
            font=("TkDefaultFont", 10, "bold")
        )
        btn2.pack(side="left", padx=10)

        _, body2 = self._card(page, "Tables du round", "Affichage des groupes par table")
        self.tables_tv = ttk.Treeview(body2, columns=("players",), show="headings", height=10)
        self.tables_tv.heading("players", text="Joueurs")
        self.tables_tv.column("players", anchor="w")
        self.tables_tv.pack(fill="both", expand=True)

        self._refresh_tables()
        return page

    def _page_results(self, parent):
        page = tk.Frame(parent, bg=self.C_BG)
        page.grid_columnconfigure(0, weight=1)

        _, body = self._card(page, "Rentrer des résultats", "Saisie visuelle — appliquera les scores plus tard")
        top = tk.Frame(body, bg=self.C_PANEL)
        top.pack(fill="x")

        tk.Label(top, text="Table:", bg=self.C_PANEL, fg=self.C_MUTED).pack(side="left")
        self.selected_table_var = tk.StringVar(value="1")
        self.table_combo = ttk.Combobox(top, textvariable=self.selected_table_var, values=["1"], state="readonly", width=8)
        self.table_combo.pack(side="left", padx=8)
        self.table_combo.bind("<<ComboboxSelected>>", lambda _e: self._refresh_result_form())

        btn_apply = tk.Button(
            top, text="✅ Enregistrer (mock)",
            command=self._mock_apply_results,
            bg=self.C_ACCENT_2, fg="white", relief="flat", bd=0, padx=14, pady=10,
            activebackground=self.C_ACCENT_2, activeforeground="white",
            font=("TkDefaultFont", 10, "bold")
        )
        btn_apply.pack(side="right")

        self.result_form = tk.Frame(body, bg=self.C_PANEL)
        self.result_form.pack(fill="x", pady=(12, 0))
        self.result_vars: dict[str, tk.IntVar] = {}

        self._refresh_result_form()
        return page

    def _page_standings(self, parent):
        page = tk.Frame(parent, bg=self.C_BG)
        page.grid_columnconfigure(0, weight=1)

        _, body = self._card(page, "Classement", "Trié par score décroissant")
        self.stand_tv = ttk.Treeview(body, columns=("score",), show="headings", height=14)
        self.stand_tv.heading("score", text="Score")
        self.stand_tv.column("score", width=120, anchor="center")
        self.stand_tv.pack(fill="both", expand=True)

        self._refresh_standings()
        return page

    # -----------------------------
    # Refresh helpers
    # -----------------------------
    def _refresh_header(self):
        self.h_sub.configure(text=f"Round {self.round_number} • {len(self.players)} players • {len(self.tables)} table(s)")

    def _refresh_players(self):
        self.players_tv.delete(*self.players_tv.get_children())
        for p in sorted(self.players, key=lambda x: x.name.lower()):
            self.players_tv.insert("", "end", values=(p.score,), text=p.name)
            # Treeview in "headings" mode won't display item text; so we add name as first hidden col workaround:
        # Workaround: rebuild with explicit name column visually
        self.players_tv.destroy()
        parent = self.pages["players"].winfo_children()[-1].winfo_children()[-1]  # body2
        self.players_tv = ttk.Treeview(parent, columns=("name", "score"), show="headings", height=9)
        self.players_tv.heading("name", text="Joueur")
        self.players_tv.heading("score", text="Score")
        self.players_tv.column("name", anchor="w")
        self.players_tv.column("score", width=120, anchor="center")
        self.players_tv.pack(fill="both", expand=True)
        for p in sorted(self.players, key=lambda x: x.name.lower()):
            self.players_tv.insert("", "end", values=(p.name, p.score))

    def _refresh_tables(self):
        self.tables_tv.delete(*self.tables_tv.get_children())
        for t in self.tables:
            self.tables_tv.insert("", "end", values=(", ".join(t.players),))
        # update combobox in results page
        if hasattr(self, "table_combo"):
            vals = [str(t.table_id) for t in self.tables] or ["1"]
            self.table_combo.configure(values=vals)
            if self.selected_table_var.get() not in vals:
                self.selected_table_var.set(vals[0])
            self._refresh_result_form()
        self._refresh_header()

    def _refresh_result_form(self):
        # clear form
        for w in self.result_form.winfo_children():
            w.destroy()
        self.result_vars.clear()

        table_id = int(self.selected_table_var.get() or "1")
        t = next((x for x in self.tables if x.table_id == table_id), None)
        if not t:
            tk.Label(self.result_form, text="Aucune table.", bg=self.C_PANEL, fg=self.C_MUTED).pack(anchor="w")
            return

        tk.Label(self.result_form, text="Points par joueur (mock)", bg=self.C_PANEL, fg=self.C_MUTED).grid(row=0, column=0, sticky="w", pady=(0, 8))
        for i, name in enumerate(t.players, start=1):
            tk.Label(self.result_form, text=name, bg=self.C_PANEL, fg=self.C_TEXT, font=("TkDefaultFont", 10, "bold")).grid(row=i, column=0, sticky="w", pady=6)
            var = tk.IntVar(value=0)
            self.result_vars[name] = var
            sp = tk.Spinbox(
                self.result_form, from_=0, to=5, textvariable=var,
                bg=self.C_PANEL_2, fg=self.C_TEXT, insertbackground=self.C_TEXT,
                relief="flat", width=8
            )
            sp.grid(row=i, column=1, sticky="w", padx=10, ipady=6)

        self.result_form.grid_columnconfigure(0, weight=1)

    def _refresh_standings(self):
        self.stand_tv.delete(*self.stand_tv.get_children())
        for p in sorted(self.players, key=lambda x: x.score, reverse=True):
            self.stand_tv.insert("", "end", values=(p.score,), text=p.name)
        # rebuild with explicit name col like before
        parent = self.pages["standings"].winfo_children()[-1].winfo_children()[-1]
        self.stand_tv.destroy()
        self.stand_tv = ttk.Treeview(parent, columns=("rank", "name", "score"), show="headings", height=14)
        self.stand_tv.heading("rank", text="#")
        self.stand_tv.heading("name", text="Joueur")
        self.stand_tv.heading("score", text="Score")
        self.stand_tv.column("rank", width=60, anchor="center")
        self.stand_tv.column("score", width=120, anchor="center")
        self.stand_tv.column("name", anchor="w")
        self.stand_tv.pack(fill="both", expand=True)

        for idx, p in enumerate(sorted(self.players, key=lambda x: x.score, reverse=True), start=1):
            self.stand_tv.insert("", "end", values=(idx, p.name, p.score))

    # -----------------------------
    # Navigation
    # -----------------------------
    def _show_page(self, key: str):
        self._set_nav_active(key)
        for k, frame in self.pages.items():
            frame.tkraise() if k == key else None

        titles = {
            "players": ("Joueurs", "Ajoute et gère la liste des participants"),
            "tables": ("Tables", "Génère et affiche les tables du round"),
            "results": ("Résultats", "Saisis les points de chaque table"),
            "standings": ("Classement", "Consulte le ranking du tournoi"),
        }
        t, s = titles.get(key, ("Tournament Dashboard", ""))
        self.h_title.configure(text=t)
        self.h_sub.configure(text=f"Round {self.round_number} • {len(self.players)} players • {len(self.tables)} table(s) • {s}")

    # -----------------------------
    # Mock actions (visuel)
    # -----------------------------
    def _mock_add_player(self):
        name = self.player_name_var.get().strip()
        if not name:
            self._toast("Entre un nom de joueur.")
            return
        if any(p.name.lower() == name.lower() for p in self.players):
            self._toast("Ce joueur existe déjà.")
            return
        self.players.append(MockPlayer(name, 0))
        self.player_name_var.set("")
        self._refresh_players()
        self._refresh_standings()
        self._refresh_header()
        self._toast(f"Ajouté: {name}")

    def _mock_generate_tables(self):
        # Mock: mettre les joueurs dans une seule table (ou plusieurs par 4)
        names = [p.name for p in self.players]
        if len(names) < 3:
            self._toast("Il faut au moins 3 joueurs.")
            return

        self.tables.clear()
        tid = 1
        i = 0
        while i < len(names):
            chunk = names[i:i+4]
            self.tables.append(MockTable(tid, chunk))
            tid += 1
            i += 4

        self._refresh_tables()
        self._toast("Tables générées (mock).")

    def _mock_apply_results(self):
        table_id = int(self.selected_table_var.get() or "1")
        t = next((x for x in self.tables if x.table_id == table_id), None)
        if not t:
            self._toast("Table introuvable.")
            return

        result = {name: var.get() for name, var in self.result_vars.items()}
        t.result = result

        # mock: appliquer score
        for p in self.players:
            if p.name in result:
                p.score += int(result[p.name])

        self._refresh_players()
        self._refresh_standings()
        self._toast(f"Résultat enregistré pour Table {table_id} (mock).")

    def _mock_new_round(self):
        self.round_number += 1
        self._refresh_header()
        self._toast(f"Round {self.round_number} (mock).")

    # -----------------------------
    # Toast message
    # -----------------------------
    def _toast(self, msg: str):
        self.sidebar_status.configure(text=f"● {msg}", fg=self.C_ACCENT_2)
        self.after(2200, lambda: self.sidebar_status.configure(text="● Ready", fg=self.C_ACCENT_2))


if __name__ == "__main__":
    app = PairingApp()
    app.mainloop()
