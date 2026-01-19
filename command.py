class Command:
    """
    Cette classe représente une commande. Une commande est composée d'un mot-clé,
    d'un message d'aide, d'une action et d'un nombre de paramètres.
    """

    def __init__(self, command_word, help_string, action, number_of_parameters):
        self.command_word = command_word
        self.help_string = help_string
        self.action = action
        self.number_of_parameters = number_of_parameters
    
    def __str__(self):
        return  self.command_word + self.help_string