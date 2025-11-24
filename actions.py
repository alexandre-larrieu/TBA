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

        direction = " ".join(list_of_words[1:]).upper() 

        if player.current_room.name == "Gouffre Sombre":
            print("\nVous essayez de bouger, mais les murs sont lisses. Vous avez PERDU.")
            return False

        if player.current_room.name == "Devant la Porte" and (direction == "E" or direction == "PORTE"):
            if not game.game_states["porte_salon_ouverte"]:
                print("\nLa porte massive est fermement verrouillée.")
                print("VOIX DE KARABA : 'HAHA ! SANS LA CLÉ, POINT DE CHEVEUX !'")
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
            return True

        move_success = player.move(direction)
        
        if move_success and player.current_room.name == "Le Salon Sacré":
            print("\n--- FÉLICITATIONS ! ---")
            print("Vous avez atteint la salle des perruques !")
            print(f"Vous pensez à votre père, {player.name}. Il s'est sacrifié pour vos cheveux.")
            print(f"Vous : 'Ça farte ?'")
            game.finished = True 
        
        return move_success

    def quit(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False
        
        player = game.player
        if player.current_room.name == "Gouffre Sombre":
            print(f"\n{player.name} abandonne dans le noir...")
        elif game.game_states["cylian_rencontre"] and not game.game_states["cylian_sacrifie"]:
            print(f"\n{player.name} reste avec son père pour l'éternité.")
        else:
            print(f"\nMerci {player.name} d'avoir joué. Au revoir.")
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
        
        if item_name == "onguent brut":
             print("\nVous devez le fabriquer, pas le trouver !")
             return False

        if item_name in room.inventory:
            item = room.inventory[item_name]
            
            if player.current_weight + item.weight > player.max_weight:
                print(f"\nCet objet est trop lourd ! ({item.weight} kg)")
                print("Vous vous faites un tour de reins en essayant de le soulever.")
                if not player.damage_ego(15, "Hernie discale"):
                    game.finished = True
                return False

            del room.inventory[item_name]
            player.inventory[item_name] = item
            player.current_weight += item.weight
            
            print(f"\nVous avez pris : {item.name}.")
            if item_name == "peigne":
                print("VOIX DE KARABA : 'NE TOUCHEZ PAS À MES AFFAIRES !'")
            
            # Indice si on prend le grimoire
            if item_name == "grimoire":
                print("\nVous lisez : 'RECETTE SECRÈTE : Mélangez BAVE DE LIMACE et POUDRE DE PERRUQUE dans un LABORATOIRE pour obtenir l'onguent.'")

            print(room.get_long_description())
            return True
        else:
            print(f"\nIl n'y a pas d'objet '{item_name}' ici.")
            return False

    def combiner(game, list_of_words, number_of_parameters):
        player = game.player
        
        # --- MODIFICATION MAJEURE : VÉRIFICATION DE LA SALLE ---
        if player.current_room.name != "Laboratoire d'Alchimie":
            print("\nImpossible de faire des mélanges ici ! Il vous faut un équipement stable.")
            print("Cherchez le 'Laboratoire d'Alchimie'.")
            return False
        # -------------------------------------------------------

        if len(list_of_words) < 3:
            print("\nIl faut deux objets pour combiner. Ex: 'combiner manche dents'")
            return False
            
        item1_name = list_of_words[1]
        item2_name = list_of_words[2]
        
        if item1_name not in player.inventory or item2_name not in player.inventory:
            print("\nVous devez avoir les deux objets dans votre inventaire.")
            return False
            
        items_set = {item1_name, item2_name}
        
        if items_set == {"manche", "dents"}:
            print("\nSur la table du laboratoire, vous emboîtez les dents sur le manche. Clic ! Le peigne est réparé.")
            del player.inventory["manche"]
            del player.inventory["dents"]
            player.current_weight -= 0.4 
            
            peigne_neuf = Item("peigne", "un peigne en ivoire réparé", 0.4, False)
            player.inventory["peigne"] = peigne_neuf
            player.current_weight += 0.4
            return True

        elif items_set == {"bave", "poudre"}:
            print("\nVous utilisez les alambics pour mélanger la poudre et la bave... Ça fume, ça pue, mais ça crée une pâte.")
            del player.inventory["bave"]
            del player.inventory["poudre"]
            player.current_weight -= 0.8
            
            onguent = Item("onguent brut", "une pâte grise qui attend d'être enchantée", 0.8, False)
            player.inventory["onguent brut"] = onguent
            player.current_weight += 0.8
            return True
            
        else:
            print("\nÇa ne marche pas. Le mélange explose au visage !")
            if not player.damage_ego(20, "Explosion chimique"):
                game.finished = True 
            return False

    def parler(game, list_of_words, number_of_parameters):
        player = game.player
        room = player.current_room
        
        if len(list_of_words) < 2:
            print(f"\nPrécisez à qui parler.")
            return False
        
        char_name = " ".join(list_of_words[1:])
        
        if char_name not in room.characters:
            print(f"\nIl n'y a personne nommé '{char_name}' ici.")
            return False
        
        character = room.characters[char_name]
        print(f"\n{character.name.upper()} : {character.get_msg()}")
        
        action_reussie = False

        if char_name == "homme" and room.name == "Cellule Humide":
            if not game.game_states["cylian_rencontre"]:
                print("\n(L'homme se révèle être Cylian, votre père !)")
                game.game_states["cylian_rencontre"] = True
                
                del room.characters["homme"]
                cylian_char = Character("cylian", "votre père", room, ["Continuons, mon fils !", "Il faut trouver un moyen de négocier avec Karaba."])
                room.characters["cylian"] = cylian_char
                
                room.description = "dans une ancienne prison. Le coin est vide."
                action_reussie = True

        elif char_name == "karaba":
            if not game.game_states["cylian_rencontre"]:
                return True 

            if "crème capillaire" in player.inventory:
                return True 

            if "onguent brut" in player.inventory:
                print("\nKARABA : 'Ah, tu as préparé la base (onguent). Pas mal.'")
                print("KARABA : 'Je vais l'enchanter. Mais la magie a un prix : une âme.'")
                print("\nCYLIAN surgit : 'Prends-moi ! Laisse mon fils partir !'")
                print("Karaba accepte. Elle enchante l'onguent qui devient de la CRÈME CAPILLAIRE.")
                
                game.game_states["cylian_sacrifie"] = True
                
                del player.inventory["onguent brut"]
                player.current_weight -= 0.8
                
                creme = Item("crème capillaire", "une crème magique", 1.2)
                player.inventory["crème capillaire"] = creme
                player.current_weight += 1.2
                
                cylian_sacrifie = Character("cylian", "votre père, prisonnier", room, ["Pars... Sauve-toi..."])
                room.characters["cylian"] = cylian_sacrifie
                
                cellule = next(r for r in game.rooms if r.name == "Cellule Humide")
                if "cylian" in cellule.characters:
                    del cellule.characters["cylian"]

                room.description = "dans la chambre. Cylian est prisonnier à côté de Karaba."
                action_reussie = True
            else:
                print("\nKARABA : 'Tu viens les mains vides ? Va au LABORATOIRE et fais-moi un onguent (bave + poudre) !'")
                if not player.damage_ego(10, "Insulte de Karaba"):
                    game.finished = True

        elif char_name == "reflet" and room.name == "Salle du Grand Miroir":
            print("\nLe miroir ondule... Un passage s'ouvre !")
            cabinet = next(r for r in game.rooms if r.name == "Cabinet du Miroir")
            room.exits["MIROIR"] = cabinet
            cabinet.exits["MIROIR"] = room
            del room.characters["reflet"]
            action_reussie = True

        elif char_name == "docteur":
            print("\nVous gagnez une greffe en Turquie !")
            game.finished = True

        if action_reussie:
            print(player.current_room.get_long_description())
        return True

    def utiliser(game, list_of_words, number_of_parameters):
        player = game.player
        room = player.current_room
        
        if len(list_of_words) < 2:
            print(f"\nQuoi utiliser ?")
            return False
        
        item_name = " ".join(list_of_words[1:])
        
        if item_name not in player.inventory:
            print(f"\nVous n'avez pas '{item_name}'.")
            return False
            
        action_reussie = False
        
        if item_name == "peigne" and room.name == "Devant la Porte":
            if not game.game_states["peigne_insere"]:
                game.game_states["peigne_insere"] = True
                del player.inventory["peigne"]
                player.current_weight -= 0.4 
                print("\nPeigne inséré. Il manque le centre.")
                action_reussie = True
            else:
                print("\nDéjà inséré.")

        elif item_name == "crème capillaire" and room.name == "Devant la Porte":
            if game.game_states["peigne_insere"]:
                game.game_states["porte_salon_ouverte"] = True
                del player.inventory["crème capillaire"]
                player.current_weight -= 1.2
                print("\nLa porte s'ouvre ! Tapez 'go porte'.")
                
                salon = next(r for r in game.rooms if r.name == "Le Salon Sacré")
                room.exits["PORTE"] = salon
                room.description = "au pied de la porte ouverte."
                action_reussie = True
            else:
                print("\nIl faut d'abord insérer le peigne.")

        else:
            print("Rien ne se passe.")

        if action_reussie:
            print(player.current_room.get_long_description())
        return True