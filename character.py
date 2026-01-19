import random

class Character:
    """
    Représente un personnage non joueur (PNJ).
    """
    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs 
        self.is_following = False 

    def __str__(self):
        return f"{self.name} : {self.description}"

    def get_msg(self):
        if not self.msgs:
            return "Il n'a rien à dire."
        msg = self.msgs.pop(0)
        self.msgs.append(msg)
        return msg
    
    def move(self):
        """Déplace le PNJ aléatoirement."""
        if self.is_following:
            return False

        if random.choice([True, False]):
            exits = self.current_room.exits
            possible = [key for key, r in exits.items() if r is not None]
            
            if possible:
                d = random.choice(possible)
                next_r = exits[d]
                if self.name in self.current_room.characters:
                    del self.current_room.characters[self.name]
                self.current_room = next_r
                next_r.characters[self.name] = self
                return True
        return False