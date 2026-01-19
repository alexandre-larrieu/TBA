class Player():
    """
    Représente le joueur (Cricri).
    """
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.inventory = {} 
        self.max_weight = 12.0 
        self.current_weight = 0.0
        self.ego = 100 
        self.history = [] 
        self.rewards = [] # Pour les quêtes
    
    def move(self, direction):
        """Déplace le joueur vers une autre salle."""
        if direction not in self.current_room.exits:
            print("\nAucune porte dans cette direction !\n")
            return False
            
        next_room = self.current_room.exits[direction]

        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # 1. Sauvegarde historique
        self.history.append(self.current_room)
        
        old_room = self.current_room
        self.current_room = next_room
        
        # 2. Gestion suiveur (Cylian)
        for char_name, character in list(old_room.characters.items()):
            if character.is_following:
                del old_room.characters[char_name]
                self.current_room.characters[char_name] = character
                character.current_room = self.current_room
                print(f"\n({character.name} vous suit.)")

        print(self.current_room.get_long_description())
        print(self.get_history()) 
        
        return True
        
    def go_back(self):
        """Permet de revenir à la salle précédente."""
        if not self.history:
            print("\nImpossible de revenir en arrière, vous êtes au début !")
            return False
            
        previous_room = self.history.pop()
        old_room = self.current_room
        self.current_room = previous_room
        
        # Gestion suiveur retour
        for char_name, character in list(old_room.characters.items()):
            if character.is_following:
                del old_room.characters[char_name]
                self.current_room.characters[char_name] = character
                character.current_room = self.current_room
                print(f"\n({character.name} vous suit.)")

        print("\nVous retournez sur vos pas...")
        print(self.current_room.get_long_description())
        print(self.get_history())
        return True
    
    def get_history(self):
        if not self.history:
            return ""
        output = "\nVous avez déjà visité les pièces suivantes :"
        for room in self.history:
            output += f"\n - {room.description}"
        return output
    
    def get_inventory_str(self):
        if not self.inventory:
            return "Votre inventaire est vide."
        output = f"Votre inventaire ({self.current_weight:.1f}/{self.max_weight} kg) :\n"
        for item in self.inventory.values():
            output += f"    - {item}\n"
        
        if self.rewards:
            output += "\nRécompenses de quêtes :\n"
            for reward in self.rewards:
                output += f"    🏆 {reward}\n"
        return output

    def damage_ego(self, amount, reason):
        self.ego -= amount
        print(f"\n💔 EGO -{amount} ({reason})")
        print(f"Ego actuel : {self.ego}/100")
        if self.ego <= 0:
            print("\n😭 Votre complexe est trop fort. Vous vous roulez en boule par terre en pleurant.")
            print("GAME OVER (Dépression Capillaire)")
            return False 
        return True

    def add_reward(self, reward):
        self.rewards.append(reward)
        print(f"Vous avez reçu : {reward} !")