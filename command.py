class Command:
    """
    This class represents a command. A command is composed of a command word, a help string, an action and a number of parameters.
    """

    def __init__(self, command_word, help_string, action, number_of_parameters):
        self.command_word = command_word
        self.help_string = help_string
        self.action = action
        self.number_of_parameters = number_of_parameters
    
    def __str__(self):
        return  self.command_word + self.help_string