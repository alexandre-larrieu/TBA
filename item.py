class Item:
    """
    Représente un objet dans le jeu.
    """
    def __init__(self, name, description, weight, is_mixable=False):
        self.name = name
        self.description = description
        self.weight = weight
        self.is_mixable = is_mixable # Si True, on peut l'utiliser avec 'combiner'

    def __str__(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"