import random

class Character:
    """
    Représente un personnage non joueur (PNJ).
    """
    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs # Liste de messages

    def __str__(self):
        return f"{self.name} : {self.description}"

    def get_msg(self):
        """
        Retourne le prochain message du PNJ de façon cyclique.
        """
        if not self.msgs:
            return "Il n'a rien à dire."
        
        # Prend le premier message, l'affiche, et le remet à la fin de la liste
        msg = self.msgs.pop(0)
        self.msgs.append(msg)
        return msg
    
    def move(self):
        """
        Déplace le PNJ aléatoirement dans une salle adjacente.
        Retourne True si le déplacement a eu lieu.
        """
        # 1 chance sur 2 de bouger à chaque tour
        if random.choice([True, False]):
            exits = self.current_room.exits
            # On récupère les sorties possibles (excluant les murs/None)
            possible_directions = [key for key, room in exits.items() if room is not None]
            
            if possible_directions:
                direction = random.choice(possible_directions)
                next_room = exits[direction]
                
                # Gestion du déplacement dans les dictionnaires
                # 1. Retirer le PNJ de la salle actuelle
                if self.name in self.current_room.characters:
                    del self.current_room.characters[self.name]
                
                # 2. Mettre à jour la salle du PNJ
                self.current_room = next_room
                
                # 3. Ajouter le PNJ dans la nouvelle salle
                next_room.characters[self.name] = self
                
                return True
        return False