class Player():
    """
    Représente le joueur (Cricri).
    """
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.inventory = {} # Dictionnaire {nom_item: objet_Item}
        self.max_weight = 12.0 # Capacité de portage (en kg)
        self.current_weight = 0.0
        self.ego = 100 # Santé mentale (100%)
    
    def move(self, direction):
        """Déplace le joueur vers une autre salle."""
        # Vérifie si la direction existe dans les sorties de la salle actuelle
        if direction not in self.current_room.exits:
            print("\nAucune porte dans cette direction !\n")
            return False
            
        next_room = self.current_room.exits[direction]

        # Vérifie si la sortie est valide (pas None)
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Effectue le déplacement
        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True
    
    def get_inventory_str(self):
        """Affiche l'inventaire et le poids total."""
        if not self.inventory:
            return "Votre inventaire est vide."
        
        output = f"Votre inventaire ({self.current_weight:.1f}/{self.max_weight} kg) :\n"
        for item in self.inventory.values():
            output += f"    - {item}\n"
        return output

    def damage_ego(self, amount, reason):
        """
        Inflige des dégâts à l'Ego du joueur.
        Retourne True si le joueur est toujours 'vivant', False sinon.
        """
        self.ego -= amount
        print(f"\n💔 EGO -{amount} ({reason})")
        print(f"Ego actuel : {self.ego}/100")
        
        if self.ego <= 0:
            print("\n😭 Votre complexe est trop fort. Vous vous roulez en boule par terre en pleurant.")
            print("GAME OVER (Dépression Capillaire)")
            return False # Le joueur a perdu
        return True