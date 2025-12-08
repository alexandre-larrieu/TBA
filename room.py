class Room:
    """
    Représente un lieu dans le jeu.
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}   # Dictionnaire {nom_item: objet_Item}
        self.characters = {}  # Dictionnaire {nom_pnj: objet_Character}

    def get_exit(self, direction):
        """Retourne la salle dans la direction donnée si elle existe."""
        if direction in self.exits:
            return self.exits[direction]
        return None

    def get_exit_string(self):
        """Retourne la liste des sorties sous forme de chaîne."""
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        return exit_string.strip(", ")

    def get_inventory_string(self):
        """Retourne une chaine décrivant les objets et PNJ présents."""
        output = ""
        if self.inventory:
            output += "Vous voyez ici :\n"
            for item in self.inventory.values():
                output += f"    - {item}\n"
        
        if self.characters:
            output += "Personnages présents :\n"
            for char in self.characters.values():
                output += f"    - {char.name}\n"
        return output

    def get_long_description(self):
        """Retourne la description complète du lieu."""
        # Affiche le nom de la salle en titre
        return f"\n--- {self.name.upper()} ---\nVous êtes {self.description}\n{self.get_inventory_string()}\n{self.get_exit_string()}\n"