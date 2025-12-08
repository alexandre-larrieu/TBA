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
        self.history = [] # Historique des salles
    
    def move(self, direction):
        """Déplace le joueur vers une autre salle."""
        if direction not in self.current_room.exits:
            print("\nAucune porte dans cette direction !\n")
            return False
            
        next_room = self.current_room.exits[direction]

        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Sauvegarde historique (ajoute la salle actuelle avant de partir)
        self.history.append(self.current_room)
        
        # Effectue le déplacement
        self.current_room = next_room
        print(self.current_room.get_long_description())
        
        # Affiche l'historique automatiquement après chaque déplacement
        print(self.get_history()) 
        
        return True
        
    def go_back(self):
        """Permet de revenir à la salle précédente."""
        if not self.history:
            print("\nImpossible de revenir en arrière, vous êtes au début !")
            return False
            
        previous_room = self.history.pop()
        self.current_room = previous_room
        print("\nVous retournez sur vos pas...")
        print(self.current_room.get_long_description())
        
        print(self.get_history())
        return True
    
    def get_history(self):
        """Retourne le parcours complet sous la forme Salle 1 -> Salle 2..."""
        # On crée une liste temporaire avec l'historique + la salle actuelle
        full_path = self.history + [self.current_room]
        
        # On extrait les noms des salles
        names = [room.name for room in full_path]
        
        # On joint les noms avec des flèches
        return "\nParcours : " + " -> ".join(names)
    
    def get_inventory_str(self):
        """Affiche l'inventaire et le poids total."""
        if not self.inventory:
            return "Votre inventaire est vide."
        
        output = f"Votre inventaire ({self.current_weight:.1f}/{self.max_weight} kg) :\n"
        for item in self.inventory.values():
            output += f"    - {item}\n"
        return output

    def damage_ego(self, amount, reason):
        """Inflige des dégâts à l'Ego du joueur."""
        self.ego -= amount
        print(f"\n💔 EGO -{amount} ({reason})")
        print(f"Ego actuel : {self.ego}/100")
        
        if self.ego <= 0:
            print("\n😭 Votre complexe est trop fort. Vous vous roulez en boule par terre en pleurant.")
            print("GAME OVER (Dépression Capillaire)")
            return False 
        return True