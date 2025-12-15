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
        self.all_npcs = [] # Liste pour gérer les mouvements des PNJ
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
        # Directions en français et anglais
        self.commands["go"] = Command("go", " <direction> : se déplacer (NORD, SUD, EST, OUEST, HAUT, BAS)", Actions.go, 1)
        self.commands["regarder"] = Command("regarder", " : observe la salle actuelle", Actions.regarder, 0)
        self.commands["inventaire"] = Command("inventaire", " : affiche votre inventaire", Actions.inventaire, 0)
        self.commands["prendre"] = Command("prendre", " <objet> : prend un objet", Actions.prendre, 1)
        self.commands["parler"] = Command("parler", " <personnage> : parle à un personnage", Actions.parler, 1)
        self.commands["utiliser"] = Command("utiliser", " <objet> : utilise un objet", Actions.utiliser, 1)
        self.commands["combiner"] = Command("combiner", " <obj1> <obj2> : fusionne deux objets (Laboratoire seulement)", Actions.combiner, 2)
        self.commands["back"] = Command("back", " : revenir en arrière", Actions.back, 0)
        self.commands["poser"] = Command("poser", " <objet> : poser un objet", Actions.drop, 1)
        self.commands["historique"] = Command("historique", " : afficher le parcours", Actions.history, 0)
        # --- Création des Lieux ---
        entree = Room("Entrée de la Grotte", "à l'entrée. Un éboulement bloque la sortie. La vision de la voyante était claire...")
        couloir = Room("Couloir Murmures", "dans un couloir étroit. Des échos étranges résonnent.")
        jardin = Room("Jardin des Statues", "dans une immense caverne naturelle remplie de statues de pierre... des aventuriers pétrifiés ?")
        labo = Room("Laboratoire d'Alchimie", "dans une salle remplie de fioles et d'alambics. C'est le seul endroit stable pour faire des mélanges.")
        biblio = Room("Bibliothèque Poussiéreuse", "devant des étagères remplies de livres en décomposition.")
        armurerie = Room("Armurerie Oubliée", "dans une salle d'armes rouillées. Le sol est jonché de métal inutile.")
        gouffre = Room("Gouffre Sombre", "dans un cul-de-sac. Le sol est instable. En vous avançant, la pierre s'effondre derrière vous ! Vous avez PERDU.")
        cellule = Room("Cellule Humide", "dans ce qui ressemble à une ancienne prison.")
        miroir = Room("Salle du Grand Miroir", "dans une salle immense dominée par un miroir terni. Un passage étroit mène à l'OUEST, et un autre passage mène à l'EST vers une grande porte.")
        chambre = Room("Chambre de Karaba", "dans les quartiers privés de la gardienne ! C'est en désordre. Karaba, la sorcière, est assise sur un trône d'ossements.")
        devant_la_porte = Room("Devant la Porte", "Vous êtes au pied de la porte massive du Salon Sacré. Elle est verrouillée par une serrure complexe en forme de peigne.")
        salon = Room("Le Salon Sacré", "dans la salle de la 'fontaine'. Des étagères remplies de perruques. Au fond, une sortie vers l'air libre !")
        cabinet = Room("Cabinet du Miroir", "dans un bureau stérile et blanc. C'est... un cabinet médical ?")

        self.rooms = [entree, couloir, jardin, labo, biblio, armurerie, gouffre, cellule, miroir, chambre, devant_la_porte, salon, cabinet]

        # --- Création des Items ---
        manche = Item("manche", "un manche en ivoire cassé", 0.2, True)
        dents = Item("dents", "la partie dentée du peigne", 0.2, True)
        bave = Item("bave", "une fiole visqueuse de limace", 0.5, True)
        poudre = Item("poudre", "de la vieille poudre de perruque", 0.3, True)
        livre = Item("grimoire", "un livre ouvert à la page 'Remèdes Capillaires'", 1.0, False)
        enclume = Item("enclume", "une enclume en fer massif", 50.0, False)

        # Placement des Items
        entree.inventory["manche"] = manche
        armurerie.inventory["dents"] = dents
        armurerie.inventory["enclume"] = enclume
        gouffre.inventory["bave"] = bave
        cellule.inventory["poudre"] = poudre
        biblio.inventory["grimoire"] = livre

        # --- Création des Personnages (PNJ) ---
        homme = Character("homme", "un homme chauve recroquevillé dans le coin", cellule, 
                          ["...j'ai froid...", "Qui est là ?", "...mes cheveux..."])
        
        karaba = Character("karaba", "la sorcière gardienne du temple", chambre, 
                           ["Que me veux-tu ?", "Déguerpis.", "Mes cheveux sont éternels !"])
        
        reflet = Character("reflet", "votre propre reflet... mais différent", miroir, 
                           ["Bonjour. Je vous attends.", "Le Dr. Cheveux peut vous aider."])
        
        docteur = Character("docteur", "un homme en blouse blanche", cabinet, 
                            ["Bonjour ! Je suis le Dr. Cheveux.", "La Turquie est belle en cette saison."])

        # NOUVEAU PNJ MOBILE : Le Rat Pelé
        rat = Character("rat", "un rat complètement chauve qui court partout", jardin, 
                        ["Couic !", "Il grignote une perruque invisible.", "Squeek !"])

        # Placement initial
        cellule.characters["homme"] = homme
        chambre.characters["karaba"] = karaba
        miroir.characters["reflet"] = reflet
        cabinet.characters["docteur"] = docteur
        jardin.characters["rat"] = rat

        # Liste de tous les PNJ mobiles (seul le rat bouge)
        self.all_npcs.append(rat)

        # --- Création des Sorties ---
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

        # --- Setup player ---
        self.player = Player(input("\nEntrez votre nom (ex: Cricri): "))
        self.player.current_room = entree 

    def play(self):
        self.setup()
        self.print_welcome()
        while not self.finished:
            self.process_command(input("> "))
            
            # --- DÉPLACEMENT DES PNJ ---
            for npc in self.all_npcs:
                npc.move()

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