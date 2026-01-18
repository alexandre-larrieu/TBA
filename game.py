from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character

class Game:
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.all_npcs = [] 
        self.game_states = {"porte_salon_ouverte": False, "cylian_rencontre": False, "peigne_insere": False, "cylian_sacrifie": False}
    
    def setup(self):
        self.commands["help"] = Command("help", " : aide", Actions.help, 0)
        self.commands["quit"] = Command("quit", " : quitter", Actions.quit, 0)
        self.commands["go"] = Command("go", " <dir> : bouger", Actions.go, 1)
        self.commands["regarder"] = Command("regarder", " : voir", Actions.regarder, 0)
        self.commands["inventaire"] = Command("inventaire", " : inventaire", Actions.inventaire, 0)
        self.commands["prendre"] = Command("prendre", " <obj> : prendre", Actions.prendre, 1)
        self.commands["parler"] = Command("parler", " <pnj> : parler", Actions.parler, 1)
        self.commands["utiliser"] = Command("utiliser", " <obj> : utiliser", Actions.utiliser, 1)
        self.commands["combiner"] = Command("combiner", " <obj1> <obj2> : mixer", Actions.combiner, 2)
        self.commands["back"] = Command("back", " : retour", Actions.back, 0)
        self.commands["poser"] = Command("poser", " <obj> : poser", Actions.drop, 1)
        self.commands["historique"] = Command("historique", " : historique", Actions.history, 0)
        
        entree = Room("Entrée de la Grotte", "à l'entrée.")
        couloir = Room("Couloir Murmures", "dans un couloir étroit.")
        jardin = Room("Jardin des Statues", "dans une caverne avec des statues.")
        labo = Room("Laboratoire d'Alchimie", "dans un labo.")
        biblio = Room("Bibliothèque Poussiéreuse", "devant des livres.")
        armurerie = Room("Armurerie Oubliée", "dans une salle d'armes.")
        gouffre = Room("Gouffre Sombre", "devant un trou.")
        cellule = Room("Cellule Humide", "dans une prison.")
        miroir = Room("Salle du Grand Miroir", "devant un miroir.")
        chambre = Room("Chambre de Karaba", "chez la sorcière.")
        devant_la_porte = Room("Devant la Porte", "devant la porte finale.")
        salon = Room("Le Salon Sacré", "Gagné !")
        cabinet = Room("Cabinet du Miroir", "chez le docteur.")

        self.rooms = [entree, couloir, jardin, labo, biblio, armurerie, gouffre, cellule, miroir, chambre, devant_la_porte, salon, cabinet]

        entree.inventory["manche"] = Item("manche", "manche ivoire", 0.2, True)
        armurerie.inventory["dents"] = Item("dents", "dents peigne", 0.2, True)
        armurerie.inventory["enclume"] = Item("enclume", "lourd", 50.0, False)
        gouffre.inventory["bave"] = Item("bave", "bave limace", 0.5, True)
        cellule.inventory["poudre"] = Item("poudre", "poudre perruque", 0.3, True)
        biblio.inventory["grimoire"] = Item("grimoire", "recette", 1.0, False)

        homme = Character("homme", "un homme peureux", cellule, ["Qui est là ?"])
        cellule.characters["homme"] = homme
        
        karaba = Character("karaba", "la sorcière", chambre, ["Déguerpis."])
        chambre.characters["karaba"] = karaba
        
        reflet = Character("reflet", "votre reflet", miroir, ["Bonjour."])
        miroir.characters["reflet"] = reflet
        
        docteur = Character("docteur", "le docteur", cabinet, ["Bonjour !"])
        cabinet.characters["docteur"] = docteur

        # --- RATS ---
        rat = Character("rat", "un rat", jardin, ["Couic !"])
        jardin.characters["rat"] = rat
        
        surmulot = Character("surmulot", "un gros surmulot", gouffre, ["Squeek !"])
        gouffre.characters["surmulot"] = surmulot
        
        self.all_npcs.append(rat)
        self.all_npcs.append(surmulot)
        # ------------

        entree.exits =  {"N" : couloir}
        couloir.exits = {"S" : entree, "O" : gouffre, "N" : jardin}
        gouffre.exits = {} 
        jardin.exits = {"S" : couloir, "N" : biblio, "E" : cellule, "O" : armurerie}
        armurerie.exits = {"E" : jardin}
        biblio.exits = {"S" : jardin, "E" : labo}
        labo.exits = {"O" : biblio}
        cellule.exits = {"O" : jardin, "N" : miroir}
        miroir.exits =  {"S" : cellule, "O" : chambre, "E" : devant_la_porte}
        chambre.exits = {"E" : miroir}
        devant_la_porte.exits = {"O" : miroir} 
        salon.exits =   {"O" : devant_la_porte} 

        self.player = Player(input("\nNom : "))
        self.player.current_room = entree 

    def play(self):
        self.setup()
        self.print_welcome()
        while not self.finished:
            self.process_command(input("> "))
            for npc in self.all_npcs:
                npc.move()

    def process_command(self, command_string):
        list_of_words = command_string.lower().strip().split(" ")
        if not list_of_words or list_of_words[0] == "": return
        command_word = list_of_words[0]
        if command_word in self.commands:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)
        else:
            print(f"\nInconnu.")
            Actions.help(self, ["help"], 0)

    def print_welcome(self):
        print(f"\n--- Bienvenue {self.player.name} ---")
        Actions.help(self, ["help"], 0)
        print(self.player.current_room.get_long_description())

if __name__ == "__main__":
    Game().play()