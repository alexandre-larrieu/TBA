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
        # Méthode optionnelle pour le futur
        return False