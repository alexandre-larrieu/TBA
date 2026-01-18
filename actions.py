from item import Item
from character import Character

MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def go(game, list_of_words, number_of_parameters):
        player = game.player
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            if " ".join(list_of_words[1:]).upper() in ["MIROIR", "PORTE"]: 
                pass 
            else:
                print(MSG1.format(command_word=command_word))
                return False
        
        raw_direction = " ".join(list_of_words[1:]).upper() 
        direction_mapping = {
            "NORD": "N", "N": "N", "SUD": "S", "S": "S", "EST": "E", "E": "E",
            "OUEST": "O", "O": "O", "HAUT": "H", "MONTER": "H", "H": "H", "BAS": "B", "DESCENDRE": "B", "B": "B"
        }
        direction = direction_mapping.get(raw_direction, raw_direction)

        if player.current_room.name == "Gouffre Sombre":
            print("\nVous essayez de bouger, mais les murs sont lisses. Vous avez PERDU.")
            return False

        if player.current_room.name == "Devant la Porte" and (direction == "E" or direction == "PORTE"):
            if not game.game_states["porte_salon_ouverte"]:
                print("\nLa porte massive est fermement verrouillée.")
                player.damage_ego(5, "Porte fermée")
                return False 
            else:
                if direction == "E":
                    print("\nLa porte est ouverte, tapez 'go porte'.")
                    return False
        
        if player.current_room.name == "Cabinet du Miroir" and direction == "MIROIR":
            salle_miroir = next(r for r in game.rooms if r.name == "Salle du Grand Miroir")
            player.current_room = salle_miroir
            print(player.current_room.get_long_description())
            print(player.get_history())
            return True

        move_success = player.move(direction)
        
        # TRIGGER QUÊTE
        if move_success:
            game.quest_manager.check_room_objectives(player.current_room.name)

        if move_success and player.current_room.name == "Le Salon Sacré":
            print("\n--- SALLE FINALE ATTEINTE ---")
        
        return move_success

    def back(game, list_of_words, number_of_parameters):
        return game.player.go_back()

    def history(game, list_of_words, number_of_parameters):
        print(game.player.get_history())
        return True

    def show_quests(game, list_of_words, number_of_parameters):
        game.quest_manager.show_quests()
        return True

    def quit(game, list_of_words, number_of_parameters):
        print(f"\nMerci {game.player.name} d'avoir joué. Au revoir.")
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print(f"\t- {command.command_word}{command.help_string}")
        return True

    def regarder(game, list_of_words, number_of_parameters):
        print(game.player.current_room.get_long_description())
        return True

    def inventaire(game, list_of_words, number_of_parameters):
        print(game.player.get_inventory_str())
        return True

    def prendre(game, list_of_words, number_of_parameters):
        player = game.player
        room = player.current_room
        if len(list_of_words) < 2:
            print(f"\nPrécisez l'objet à prendre.")
            return False
        item_name = " ".join(list_of_words[1:])
        
        if item_name == "crème capillaire":
            print("\nVous ne pouvez pas 'prendre' cet objet.")
            return False
        
        if item_name in room.inventory:
            item = room.inventory[item_name]
            if player.current_weight + item.weight > player.max_weight:
                print(f"\nCet objet est trop lourd !")
                player.damage_ego(10, "Lumbago")
                return False

            del room.inventory[item_name]
            player.inventory[item_name] = item
            player.current_weight += item.weight
            print(f"\nVous avez pris : {item.name}.")
            
            # TRIGGER QUÊTE ITEM
            game.quest_manager.check_action_objectives("prendre", item_name)

            if item_name == "peigne" and room.name == "Couloir Murmures":
                room.description = "dans un couloir étroit."
            print(room.get_long_description())
            return True
        else:
            print(f"\nIl n'y a pas d'objet '{item_name}' ici.")
            return False

    def drop(game, list_of_words, number_of_parameters):
        player = game.player
        room = player.current_room
        if len(list_of_words) < 2: return False
        item_name = " ".join(list_of_words[1:])
        
        if item_name in player.inventory:
            item = player.inventory[item_name]
            del player.inventory[item_name]
            player.current_weight -= item.weight
            room.inventory[item_name] = item
            print(f"\nVous avez posé : {item.name}.")
            print(room.get_long_description())
            return True
        else:
            print(f"\nVous n'avez pas ça.")
            return False

    def combiner(game, list_of_words, number_of_parameters):
        player = game.player
        if player.current_room.name != "Laboratoire d'Alchimie":
            print("\nIl faut être au Laboratoire.")
            return False
        if len(list_of_words) < 3: return False
            
        item1_name = list_of_words[1]
        item2_name = list_of_words[2]
        
        if item1_name not in player.inventory or item2_name not in player.inventory:
            print("\nIl vous manque des objets.")
            return False
            
        items_set = {item1_name, item2_name}
        
        if items_set == {"manche", "dents"}:
            print("\nVous assemblez le peigne.")
            del player.inventory["manche"]
            del player.inventory["dents"]
            player.current_weight -= 0.4
            player.inventory["peigne"] = Item("peigne", "un peigne réparé", 0.4)
            player.current_weight += 0.4
            
            # --- TRIGGER QUÊTE : CRAFTING ---
            # On valide la quête "Réparez le peigne"
            game.quest_manager.check_action_objectives("réparer", "peigne")
            # --------------------------------
            
            return True

        elif items_set == {"bave", "poudre"}:
            print("\nVous créez un onguent.")
            del player.inventory["bave"]
            del player.inventory["poudre"]
            player.current_weight -= 0.8
            player.inventory["onguent brut"] = Item("onguent brut", "pâte grise", 0.8)
            player.current_weight += 0.8
            return True
        else:
            print("\nÇa explose !")
            player.damage_ego(20, "Boom")
            return False

    def parler(game, list_of_words, number_of_parameters):
        player = game.player
        room = player.current_room
        if len(list_of_words) < 2: return False
        char_name = " ".join(list_of_words[1:])
        
        if char_name not in room.characters:
            print(f"\nPersonne nommé '{char_name}' ici.")
            return False
        
        character = room.characters[char_name]
        
        # TRIGGER QUÊTE INTERACTION
        game.quest_manager.check_action_objectives("parler", char_name)

        if char_name == "rat" or char_name == "surmulot":
             print(f"\n{character.name.upper()} : {character.get_msg()}")
             if game.game_states["rat_apprivoise"]:
                 print("Le rat vous regarde avec gratitude.")
             else:
                 print("Vous vous sentez ridicule de parler à un rat...")
                 if not player.damage_ego(10, "Parler aux animaux"):
                     game.finished = True
             return True

        if char_name == "homme" and room.name == "Cellule Humide":
            if not game.game_states["cylian_rencontre"]:
                print("\n(L'homme se révèle être Cylian, votre père !)")
                game.game_states["cylian_rencontre"] = True
                del room.characters["homme"]
                cylian_char = Character("cylian", "votre père", room, ["Continuons...", "Négocions avec Karaba."])
                room.characters["cylian"] = cylian_char
                room.description = "dans une ancienne prison."
                print("\nCYLIAN : 'Veux-tu que je vienne avec toi ?' (oui/non)")
                reponse = input("> ").lower()
                if reponse == "oui":
                    cylian_char.is_following = True
                    print("\nCYLIAN : 'Je te suis.'")
                else:
                    cylian_char.is_following = False
                    print("\nCYLIAN : 'Je reste ici.'")
            else:
                print(f"\n{character.name.upper()} : {character.get_msg()}")

        elif char_name == "karaba":
            if game.game_states["cylian_sacrifie"]:
                print("\nKARABA : 'Pars.'")
                return True
            if not game.game_states["cylian_rencontre"]:
                print(f"\n{character.name.upper()} : {character.get_msg()}")
                return True 
            
            cylian_present = False
            if "cylian" in room.characters: cylian_present = True
            
            if "onguent brut" in player.inventory and cylian_present:
                print("\nKARABA : 'Je prends l'onguent et ton père.'")
                game.game_states["cylian_sacrifie"] = True
                del player.inventory["onguent brut"]
                player.current_weight -= 0.8
                player.inventory["crème capillaire"] = Item("crème capillaire", "magique", 1.2)
                player.current_weight += 1.2
                if "cylian" in room.characters:
                    cylian = room.characters["cylian"]
                    cylian.is_following = False
                    cylian.description = "prisonnier"
                print("(Vous obtenez la Crème.)")
            elif "onguent brut" in player.inventory and not cylian_present:
                 print("\nKARABA : 'Il me faut une âme en plus...'")
            else:
                print("\nKARABA : 'Apporte-moi un onguent !'")

        else:
            print(f"\n{character.name.upper()} : {character.get_msg()}")
        return True

    def utiliser(game, list_of_words, number_of_parameters):
        player = game.player
        room = player.current_room
        if len(list_of_words) < 2: return False
        item_name = " ".join(list_of_words[1:])
        
        if item_name not in player.inventory:
            print(f"\nPas de '{item_name}'.")
            return False
            
        if item_name == "fromage":
            rat_present = "rat" in room.characters or "surmulot" in room.characters
            if rat_present:
                print("\nVous donnez le fromage au rongeur.")
                print("Il le dévore instantanément.")
                player.ego = min(100, player.ego + 20)
                del player.inventory["fromage"]
                player.current_weight -= 0.1
                game.game_states["rat_apprivoise"] = True
                game.quest_manager.check_action_objectives("utiliser", "fromage")
                return True
            else:
                print("\nIl n'y a personne qui veut de ce fromage ici.")
                return False

        if item_name == "peigne" and room.name == "Devant la Porte":
            if not game.game_states["peigne_insere"]:
                game.game_states["peigne_insere"] = True
                del player.inventory["peigne"]
                player.current_weight -= 0.4 
                print("\nPeigne inséré.")
            else: print("\nDéjà fait.")

        elif item_name == "crème capillaire" and room.name == "Devant la Porte":
            if game.game_states["peigne_insere"]:
                game.game_states["porte_salon_ouverte"] = True
                del player.inventory["crème capillaire"]
                player.current_weight -= 1.2
                print("\nLa porte s'ouvre !")
                salon = next(r for r in game.rooms if r.name == "Le Salon Sacré")
                room.exits["PORTE"] = salon
            else: print("\nIl manque le peigne.")
        else: print("Rien ne se passe.")
        return True