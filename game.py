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
        self.game_states = {
            "porte_salon_ouverte": False,
            "cylian_rencontre": False,
            "peigne_insere": False,
            "cylian_sacrifie": False
        }
    
    def setup(self):
        # --- Commandes ---
        self.commands["help"] = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["quit"] = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["go"] = Command("go", " <direction> : se déplacer (N, E, S, O, U, D)", Actions.go, 1)
        self.commands["regarder"] = Command("regarder", " : observe la salle actuelle", Actions.regarder, 0)
        self.commands["inventaire"] = Command("inventaire", " : affiche votre inventaire", Actions.inventaire, 0)
        self.commands["check"] = Command("check", " : alias pour inventaire", Actions.inventaire, 0)
        self.commands["prendre"] = Command("prendre", " <objet> : prend un objet", Actions.prendre, 1)
        self.commands["take"] = Command("take", " : alias pour prendre", Actions.prendre, 1)
        self.commands["parler"] = Command("parler", " <personnage> : parle à un personnage", Actions.parler, 1)
        self.commands["talk"] = Command("talk", " : alias pour parler", Actions.parler, 1)
        self.commands["utiliser"] = Command("utiliser", " <objet> : utilise un objet", Actions.utiliser, 1)
        self.commands["combiner"] = Command("combiner", " <obj1> <obj2> : fusionne deux objets (Laboratoire seulement)", Actions.combiner, 2)
        
        # --- Création des Lieux (13 salles maintenant !) ---
        entree = Room("Entrée de la Grotte", "à l'entrée. Un éboulement bloque la sortie. La vision de la voyante était claire...")
        couloir = Room("Couloir Murmures", "dans un couloir étroit. Des échos étranges résonnent.")
        
        # NOUVEAU: Le Hub central
        jardin = Room("Jardin des Statues", "dans une immense caverne naturelle remplie de statues de pierre... qui ressemblent étrangement à des aventuriers pétrifiés.")
        
        # NOUVEAU: Zone technique
        labo = Room("Laboratoire d'Alchimie", "dans une salle remplie de fioles et d'alambics. C'est le seul endroit stable pour faire des mélanges.")
        biblio = Room("Bibliothèque Poussiéreuse", "devant des étagères remplies de livres en décomposition.")
        armurerie = Room("Armurerie Oubliée", "dans une salle d'armes rouillées. Le sol est jonché de métal inutile.")

        gouffre = Room("Gouffre Sombre", "dans un cul-de-sac. Le sol est instable. En vous avançant, la pierre s'effondre derrière vous ! Vous avez PERDU.")
        cellule = Room("Cellule Humide", "dans ce qui ressemble à une ancienne prison.")
        
        miroir = Room("Salle du Grand Miroir", "dans une salle immense dominée par un miroir terni. Un passage étroit mène à l'OUEST.")
        chambre = Room("Chambre de Karaba", "dans les quartiers privés de la gardienne ! C'est en désordre. Karaba est assise sur un trône.")
        
        devant_la_porte = Room("Devant la Porte", "Vous êtes au pied de la porte massive du Salon Sacré. Elle est verrouillée par une serrure complexe.")
        salon = Room("Le Salon Sacré", "dans la salle de la 'fontaine'. Des étagères remplies de perruques. Au fond, une sortie vers l'air libre !")
        cabinet = Room("Cabinet du Miroir", "dans un bureau stérile et blanc. C'est... un cabinet médical ?")

        self.rooms = [entree, couloir, jardin, labo, biblio, armurerie, gouffre, cellule, miroir, chambre, devant_la_porte, salon, cabinet]

        # --- Création des Items ---
        manche = Item("manche", "un manche en ivoire cassé", 0.2, True)
        dents = Item("dents", "la partie dentée du peigne", 0.2, True)
        bave = Item("bave", "une fiole visqueuse de limace", 0.5, True)
        poudre = Item("poudre", "de la vieille poudre de perruque", 0.3, True)
        
        # NOUVEAUX ITEMS
        livre = Item("grimoire", "un livre ouvert à la page 'Remèdes Capillaires'", 1.0, False)
        enclume = Item("enclume", "une enclume en fer massif", 50.0, False) # Piège de poids

        # Placement des Items
        entree.inventory["manche"] = manche
        armurerie.inventory["dents"] = dents # Déplacé pour forcer l'exploration
        armurerie.inventory["enclume"] = enclume
        gouffre.inventory["bave"] = bave
        cellule.inventory["poudre"] = poudre
        biblio.inventory["grimoire"] = livre # Donne l'indice de la recette

        # --- Création des Personnages (PNJ) ---
        homme = Character("homme", "un homme chauve recroquevillé dans le coin", cellule, 
                          ["...j'ai froid...", "Qui est là ?", "...mes cheveux..."])
        
        karaba = Character("karaba", "la sorcière gardienne du temple", chambre, 
                           ["Que me veux-tu ?", "Déguerpis.", "Mes cheveux sont éternels !"])
        
        reflet = Character("reflet", "votre propre reflet... mais différent", miroir, 
                           ["Bonjour. Je vous attends.", "Le Dr. Cheveux peut vous aider."])
        
        docteur = Character("docteur", "un homme en blouse blanche", cabinet, 
                            ["Bonjour ! Je suis le Dr. Cheveux.", "La Turquie est belle en cette saison."])

        cellule.characters["homme"] = homme
        chambre.characters["karaba"] = karaba
        miroir.characters["reflet"] = reflet
        cabinet.characters["docteur"] = docteur

        # --- Création des Sorties (LE LABYRINTHE) ---
        # L'entrée mène au couloir
        entree.exits =  {"N" : couloir}
        
        # Le couloir mène au Gouffre (O) et au Jardin (N)
        couloir.exits = {"S" : entree, "O" : gouffre, "N" : jardin}
        gouffre.exits = {} 

        # LE JARDIN (Hub Central)
        # N -> Biblio, E -> Cellule, S -> Couloir, O -> Armurerie
        jardin.exits = {"S" : couloir, "N" : biblio, "E" : cellule, "O" : armurerie}

        # Armurerie (Boucle vers le couloir possible si on veut, ou cul de sac)
        armurerie.exits = {"E" : jardin}

        # Bibliothèque (Mène au Labo)
        biblio.exits = {"S" : jardin, "E" : labo}

        # Labo (Cul de sac, sert à crafter)
        labo.exits = {"O" : biblio}

        # Cellule (Mène au Jardin et au Miroir)
        cellule.exits = {"O" : jardin, "N" : miroir}

        # Zone Finale (Miroir -> Chambre/Porte)
        miroir.exits =  {"S" : cellule, "O" : chambre, "E" : devant_la_porte}
        chambre.exits = {"E" : miroir}
        devant_la_porte.exits = {"O" : miroir} 
        salon.exits =   {"O" : devant_la_porte} 

        # --- Setup player ---
        self.player = Player(input("\nEntrez votre nom (ex: Cricri): "))
        self.player.current_room = entree 

    def play(self):
        self.setup()
        self.print_welcome()
        while not self.finished:
            self.process_command(input("> "))

    def process_command(self, command_string) -> None:
        list_of_words = command_string.lower().strip().split(" ")
        if not list_of_words or list_of_words[0] == "":
            if self.player.current_room.name == "Gouffre Sombre":
                 print("\nVous êtes piégé.")
            return
        command_word = list_of_words[0]
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue.")
            Actions.help(self, ["help"], 0) 
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    def print_welcome(self):
        print(f"\n--- Bienvenue {self.player.name} et la Fontaine Capillaire ---")
        print("La voyante l'a prévenu : 'Tu trouveras ce que tu cherches, mais ce n'est pas ce que tu crois.'")
        Actions.help(self, ["help"], 0)
        print(self.player.current_room.get_long_description())

def main():
    Game().play()
    
if __name__ == "__main__":
    main()