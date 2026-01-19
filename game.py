"""Game class"""

# Import modules
from pathlib import Path
import sys

# Tkinter imports for GUI
import tkinter as tk
from tkinter import ttk, simpledialog

# Imports du jeu
from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from quest import Quest, QuestManager

class Game:
    """The Game class manages the overall game state and flow."""

    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.all_npcs = []
        self.quest_manager = None
        self.game_states = {
            "porte_salon_ouverte": False,
            "cylian_rencontre": False,
            "peigne_insere": False,
            "cylian_sacrifie": False,
            "rat_apprivoise": False
        }

    # Setup the game
    def setup(self, player_name=None):
        """Initialize the game with rooms and commands"""
        self._setup_commands()
        self._setup_world(player_name)

    def _setup_commands(self):
        """Initialize all game commands."""
        self.commands["help"] = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["quit"] = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["go"] = Command("go", " <dir> : se déplacer (N, E, S, O, H, B)", Actions.go, 1)
        self.commands["regarder"] = Command("regarder", " : voir description", Actions.regarder, 0)
        self.commands["inventaire"] = Command("inventaire", " : inventaire", Actions.inventaire, 0)
        self.commands["prendre"] = Command("prendre", " <obj> : prendre", Actions.prendre, 1)
        self.commands["parler"] = Command("parler", " <pnj> : parler", Actions.parler, 1)
        self.commands["utiliser"] = Command("utiliser", " <obj> : utiliser", Actions.utiliser, 1)
        self.commands["combiner"] = Command("combiner", " <obj1> <obj2> : mixer (Labo)", Actions.combiner, 2)
        self.commands["back"] = Command("back", " : retour", Actions.back, 0)
        self.commands["poser"] = Command("poser", " <obj> : poser", Actions.drop, 1)
        self.commands["historique"] = Command("historique", " : historique", Actions.history, 0)
        self.commands["quetes"] = Command("quetes", " : liste des quêtes", Actions.show_quests, 0)

    def _setup_world(self, player_name):
        # --- LIEUX (Avec Indices Intégrés pour jeu autonome) ---
       
        # Entrée : Tutoriel de base
        entree = Room("Entrée de la Grotte",
                      "à l'entrée de la caverne.\nASTUCE : Tapez 'regarder' pour voir les objets et 'prendre [nom_objet]' pour les ramasser.\nVous voyez un passage vers le Nord.",
                      "forest.png")
       
        # Couloir : Indication de direction
        couloir = Room("Couloir Murmures",
                       "dans un couloir sombre. Vous entendez des bruits de rongeurs.\nASTUCE : Tapez 'go [direction]' (ex: 'go N') pour bouger.",
                       "cave.png")
       
        # Jardin : Carrefour
        jardin = Room("Jardin des Statues",
                      "dans une vaste caverne ornée de statues étranges. Plusieurs chemins s'offrent à vous.",
                      "forest.png")
       
        # Labo : Tuto Crafting
        labo = Room("Laboratoire d'Alchimie",
                    "dans un laboratoire rempli de fioles.\n★ TUTO CRAFT : Ici, vous pouvez utiliser la commande 'combiner [obj1] [obj2]'.\nPar exemple pour réparer un objet ou créer une potion.",
                    "cottage.png")
       
        # Biblio : Renferme la "Recette"
        biblio = Room("Bibliothèque Poussiéreuse",
                      "entouré de vieux livres. L'un d'eux semble contenir des recettes importantes.",
                      "castle.png")
       
        # Grenier : Indice pour le rat
        grenier = Room("Grenier Sombre",
                       "dans un petit grenier qui sent le vieux fromage. Idéal pour trouver de la nourriture pour animaux.",
                       "cottage.png")
       
        # Armurerie : Indice objets
        armurerie = Room("Armurerie Oubliée",
                         "dans une salle d'armes en ruine. Il y a beaucoup de débris métalliques au sol.",
                         "castle.png")
       
        # Gouffre : Avertissement
        gouffre = Room("Gouffre Sombre",
                       "au bord d'un précipice sans fin. Ne tombez pas !",
                       "swamp.png")
       
        # Cellule : Indice PNJ
        cellule = Room("Cellule Humide",
                       "devant une grille de prison. Quelqu'un semble enfermé à l'intérieur.\nASTUCE : Utilisez 'parler [nom]' pour interagir.",
                       "cave.png")
       
        # Égouts
        egouts = Room("Égouts Puants",
                      "dans des égouts humides et malodorants.",
                      "swamp.png")
       
        # Miroir
        miroir = Room("Salle du Grand Miroir",
                      "face à un immense miroir magique qui semble vibrer. Il cache peut-être un passage secret...",
                      "tower.png")
       
        # Chambre Karaba
        chambre = Room("Chambre de Karaba",
                       "dans l'antre de la sorcière. Elle n'a pas l'air commode. Préparez-vous à négocier.",
                       "tower.png")
       
        # Porte Finale : Instructions de victoire
        devant_la_porte = Room("Devant la Porte",
                               "devant la Porte Sacrée du Salon.\n⚠️ OBJECTIF FINAL :\n1. Insérez un 'peigne' réparé (commande: utiliser peigne).\n2. Graissez les gonds avec de la 'crème capillaire' (commande: utiliser crème capillaire).",
                               "castle.png")
       
        salon = Room("Le Salon Sacré", "dans le Salon Sacré ! Vos cheveux repoussent instantanément. VICTOIRE !", "forest.png")
       
        cabinet = Room("Cabinet du Miroir", "dans une pièce cachée derrière le miroir. Un docteur étrange vous observe.", "cottage.png")

        self.rooms = [entree, couloir, jardin, labo, biblio, grenier, armurerie, gouffre, cellule, egouts, miroir, chambre, devant_la_porte, salon, cabinet]

        # --- ITEMS (Descriptions explicites) ---
        entree.inventory["manche"] = Item("manche", "un manche en ivoire (partie 1/2 d'un peigne). À combiner avec des dents.", 0.2, True)
       
        armurerie.inventory["dents"] = Item("dents", "des dents en or (partie 2/2 d'un peigne). À combiner avec un manche.", 0.2, True)
        armurerie.inventory["enclume"] = Item("enclume", "une enclume très lourde. Impossible à prendre.", 50.0, False)
       
        gouffre.inventory["bave"] = Item("bave", "de la bave de limace visqueuse (Ingrédient A).", 0.5, True)
       
        cellule.inventory["poudre"] = Item("poudre", "de la poudre de perruque ancienne (Ingrédient B).", 0.3, True)
       
        # LE GRIMOIRE EST LA CLÉ DU JEU POUR LE JOUEUR SANS DOC
        biblio.inventory["grimoire"] = Item("grimoire", "LIVRE DE RECETTES :\n\t- Réparation : Combiner 'manche' + 'dents' = Peigne.\n\t- Alchimie : Combiner 'bave' + 'poudre' = Onguent.", 1.0, False)
       
        grenier.inventory["fromage"] = Item("fromage", "un camembert puant. Les rats en raffolent !", 0.1, False)

        # --- PNJ ---
        homme = Character("homme", "un prisonnier qui ressemble à votre père.", cellule, ["Aidez-moi ! Je connais le chemin vers la victoire.", "Libérez-moi et je vous suivrai."])
        karaba = Character("karaba", "la Sorcière Karaba.", chambre, ["Je possède la Crème Capillaire.", "Mais rien n'est gratuit. Apporte-moi un 'onguent brut' (bave + poudre)."])
        reflet = Character("reflet", "votre propre reflet.", miroir, ["Touchez le miroir... (commande: go miroir)"])
        docteur = Character("docteur", "le Docteur.", cabinet, ["C'est fascinant.", "Ce miroir est une porte."])
        rat = Character("rat", "un rat gris.", jardin, ["Couic ! (Il renifle votre poche... Avez-vous du fromage ?)"])
        surmulot = Character("surmulot", "un gros surmulot.", gouffre, ["Squeek ! (Il a l'air affamé.)"])

        cellule.characters["homme"] = homme
        chambre.characters["karaba"] = karaba
        miroir.characters["reflet"] = reflet
        cabinet.characters["docteur"] = docteur
        jardin.characters["rat"] = rat
        gouffre.characters["surmulot"] = surmulot

        self.all_npcs.append(rat)
        self.all_npcs.append(surmulot)

        # --- SORTIES ---
        entree.exits =  {"N" : couloir}
        couloir.exits = {"S" : entree, "O" : gouffre, "N" : jardin}
        gouffre.exits = {}
        jardin.exits = {"S" : couloir, "N" : biblio, "E" : cellule, "O" : armurerie}
        armurerie.exits = {"E" : jardin}
        biblio.exits = {"S" : jardin, "E" : labo, "H" : grenier}
        grenier.exits = {"B" : biblio}
        labo.exits = {"O" : biblio}
        cellule.exits = {"O" : jardin, "N" : miroir, "B" : egouts}
        egouts.exits = {"H" : cellule, "E" : miroir}
        miroir.exits =  {"S" : cellule, "O" : chambre, "E" : devant_la_porte}
        chambre.exits = {"E" : miroir}
        devant_la_porte.exits = {"O" : miroir}
        salon.exits =   {"O" : devant_la_porte}

        # --- JOUEUR ---
        if player_name is None:
            player_name = input("\nEntrez votre nom: ")
        self.player = Player(player_name)
        self.player.current_room = entree

        # --- QUÊTES (Descriptions claires) ---
        self.quest_manager = QuestManager(self.player)
       
        q1 = Quest("Débutant", "Trouvez 'manche' et 'dents', puis allez au Labo et tapez 'combiner manche dents'.", ["réparer le peigne"], "Confiance")
        self.quest_manager.add_quest(q1)
       
        q2 = Quest("Famille", "Allez à la Cellule (Est du Jardin) et parlez à l'homme.", ["parler homme"], "Souvenirs")
        self.quest_manager.add_quest(q2)
       
        q3 = Quest("Victoire", "Ouvrez la porte finale avec le Peigne et la Crème.", ["Visiter Le Salon Sacré"], "Cheveux soyeux")
        self.quest_manager.add_quest(q3)
       
        q4 = Quest("Ami des bêtes", "Trouvez du fromage au Grenier et utilisez-le sur le Rat.", ["utiliser fromage"], "Respect du rongeur")
        self.quest_manager.add_quest(q4)

        self.quest_manager.activate_quest("Débutant")
        self.quest_manager.activate_quest("Famille")
        self.quest_manager.activate_quest("Victoire")
        self.quest_manager.activate_quest("Ami des bêtes")

    # Play the game (CLI mode)
    def play(self):
        self.setup()
        self.print_welcome()
        while not self.finished:
            self.process_command(input("> "))
            self._on_turn_end()

    # Process the command
    def process_command(self, command_string) -> None:
        list_of_words = command_string.split(" ")
        command_word = list_of_words[0]

        if command_word not in self.commands:
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help'.\n")
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # NOUVEAU : Logique de fin de tour (bouger les NPC, check win) centralisée
    def _on_turn_end(self):
        for npc in self.all_npcs:
            npc.move()
        self.check_win()

    def check_win(self):
        required_quests = ["Débutant", "Famille", "Victoire"]
        all_completed = True
        for q_title in required_quests:
            quest = self.quest_manager.get_quest_by_title(q_title)
            if quest and not quest.is_completed:
                all_completed = False
       
        if all_completed and not self.finished:
            print("\n🎉 TOUTES LES QUÊTES SONT TERMINÉES ! VICTOIRE ! 🎉")
            self.finished = True

    def print_welcome(self):
        if not self.player or not self.player.name: return
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        if self.player.current_room:
            print(self.player.current_room.get_long_description())


##############################
# Tkinter GUI Implementation #
##############################

class _StdoutRedirector:
    """Redirect sys.stdout writes into a Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, msg):
        if msg:
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", msg)
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")

    def flush(self):
        pass


class GameGUI(tk.Tk):
    IMAGE_WIDTH = 600
    IMAGE_HEIGHT = 400

    def __init__(self):
        super().__init__()
        self.title("TBA - Cricri et la Fontaine Capillaire")
        self.geometry("900x700")
        self.minsize(900, 650)

        self.game = Game()

        name = simpledialog.askstring("Nom", "Entrez votre nom:", parent=self)
        if not name:
            name = "Joueur"
        self.game.setup(player_name=name)

        self._build_layout()

        self.original_stdout = sys.stdout
        sys.stdout = _StdoutRedirector(self.text_output)

        self.game.print_welcome()
        self._update_room_image()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_layout(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=(6,3))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)

        image_frame = ttk.Frame(top_frame, width=self.IMAGE_WIDTH, height=self.IMAGE_HEIGHT)
        image_frame.grid(row=0, column=0, sticky="nw", padx=(0,6))
        image_frame.grid_propagate(False)
        self.canvas = tk.Canvas(image_frame, width=self.IMAGE_WIDTH, height=self.IMAGE_HEIGHT, bg="#222")
        self.canvas.pack(fill="both", expand=True)

        self._image_ref = None

        buttons_frame = ttk.Frame(top_frame)
        buttons_frame.grid(row=0, column=1, sticky="ne")
        buttons_frame.grid_columnconfigure(0, weight=1)

        assets_dir = Path(__file__).parent / 'assets'
        try:
            self._btn_help = tk.PhotoImage(file=str(assets_dir / 'help-50.png'))
            self._btn_up = tk.PhotoImage(file=str(assets_dir / 'up-arrow-50.png'))
            self._btn_down = tk.PhotoImage(file=str(assets_dir / 'down-arrow-50.png'))
            self._btn_left = tk.PhotoImage(file=str(assets_dir / 'left-arrow-50.png'))
            self._btn_right = tk.PhotoImage(file=str(assets_dir / 'right-arrow-50.png'))
            self._btn_quit = tk.PhotoImage(file=str(assets_dir / 'quit-50.png'))
        except:
            print("Erreur: Images des boutons non trouvées dans assets/")
            self._btn_help = None # Fallback logic could be added here

        tk.Button(buttons_frame, image=self._btn_help, command=lambda: self._send_command("help"), bd=0).grid(row=0, column=0, sticky="ew", pady=2)
       
        move_frame = ttk.LabelFrame(buttons_frame, text="Déplacements")
        move_frame.grid(row=1, column=0, sticky="ew", pady=4)
        tk.Button(move_frame, image=self._btn_up, command=lambda: self._send_command("go N"), bd=0).grid(row=0, column=0, columnspan=2)
        tk.Button(move_frame, image=self._btn_left, command=lambda: self._send_command("go O"), bd=0).grid(row=1, column=0)
        tk.Button(move_frame, image=self._btn_right, command=lambda: self._send_command("go E"), bd=0).grid(row=1, column=1)
        tk.Button(move_frame, image=self._btn_down, command=lambda: self._send_command("go S"), bd=0).grid(row=2, column=0, columnspan=2)

        # Ajout Boutons Spéciaux (Haut/Bas/Quêtes)
        tk.Button(buttons_frame, text="Monter", command=lambda: self._send_command("go H")).grid(row=2, column=0, sticky="ew")
        tk.Button(buttons_frame, text="Descendre", command=lambda: self._send_command("go B")).grid(row=3, column=0, sticky="ew")
        tk.Button(buttons_frame, text="Quêtes", command=lambda: self._send_command("quetes")).grid(row=4, column=0, sticky="ew", pady=5)

        tk.Button(buttons_frame, image=self._btn_quit, command=lambda: self._send_command("quit"), bd=0).grid(row=5, column=0, sticky="ew", pady=(8,2))

        output_frame = ttk.Frame(self)
        output_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=3)
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical")
        self.text_output = tk.Text(output_frame, wrap="word", yscrollcommand=scrollbar.set, state="disabled", bg="#111", fg="#eee")
        scrollbar.config(command=self.text_output.yview)
        self.text_output.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=2, column=0, sticky="ew", padx=6, pady=(3,6))
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(entry_frame, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()

    def _update_room_image(self):
        if not self.game.player or not self.game.player.current_room:
            return

        room = self.game.player.current_room
        assets_dir = Path(__file__).parent / 'assets'

        if room.image:
            image_path = assets_dir / room.image
        else:
            image_path = assets_dir / 'scene.png'

        try:
            self._image_ref = tk.PhotoImage(file=str(image_path))
            self.canvas.delete("all")
            self.canvas.create_image(self.IMAGE_WIDTH/2, self.IMAGE_HEIGHT/2, image=self._image_ref)
        except (FileNotFoundError, tk.TclError):
            self.canvas.delete("all")
            self.canvas.create_text(self.IMAGE_WIDTH/2, self.IMAGE_HEIGHT/2, text=f"Image: {room.name}", fill="white", font=("Helvetica", 18))

    def _on_enter(self, _event=None):
        value = self.entry_var.get().strip()
        if value:
            self._send_command(value)
        self.entry_var.set("")

    def _send_command(self, command):
        if self.game.finished:
            return
        print(f"> {command}\n")
        self.game.process_command(command)
       
        # --- IMPORTANT : Bouger les NPCs et Check Victoire après chaque commande ---
        self.game._on_turn_end()
        # ---------------------------------------------------------------------------

        self._update_room_image()
        if self.game.finished:
            self.entry.configure(state="disabled")
            self.after(3000, self._on_close)

    def _on_close(self):
        sys.stdout = self.original_stdout
        self.destroy()


def main():
    args = sys.argv[1:]
    if '--cli' in args:
        Game().play()
        return
    try:
        app = GameGUI()
        app.mainloop()
    except tk.TclError as e:
        print(f"GUI indisponible ({e}). Passage en mode console.")
        Game().play()

if __name__ == "__main__":
    main()