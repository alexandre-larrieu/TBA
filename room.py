class Room:
    """
    Représente un lieu dans le jeu.
    """
    def __init__(self, name, description, image=None):
        self.name = name
        self.description = description
        self.image = image # C'est cette ligne qui manquait !
        self.exits = {}
        self.inventory = {}  
        self.characters = {}

    def get_exit(self, direction):
        if direction in self.exits:
            return self.exits[direction]
        return None

    def get_exit_string(self):
        exit_string = "Sorties: "
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        return exit_string.strip(", ")

    def get_inventory_string(self):
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
        return f"\n--- {self.name.upper()} ---\nVous êtes {self.description}\n{self.get_inventory_string()}\n{self.get_exit_string()}\n"
