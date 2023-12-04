import random

class Character:
    def __init__(self, char_type, health, attack, dodge, attack_dice):
        self.type = char_type
        self.health = health
        self.attack = attack
        self.dodge = dodge
        self.attack_dice = attack_dice

    def dice_roll(self, sides):
        return random.randint(1, sides)

    def calculate_damage(self):
        return max(0, self.attack + self.dice_roll(self.attack_dice))

    def calculate_dodge_r(self, damage_recieved):
        return max(0, damage_recieved - self.dice_roll(self.dodge))

def character_info(characters):
    for character in characters:
        print(f"{character.type}: Health - {character.health}, Attack - {character.attack}, Dodge - {character.dodge}")

def damage_result(player_damage, npc_damage, file):
    result = f"Player dealt {player_damage} damage. Opponent dealt {npc_damage} damage."
    print(result)
    file.write(result + '\n')

    if player_damage == 20:
        print("Big hit! Maximum damage dealt!")
    elif player_damage == 1:
        print("Yikes! Minimum damage dealt!")

    if npc_damage == 20:
        print("Oh no! Your opponent hit you critically!")
    elif npc_damage == 1:
        print("Your opponent dealt minimum damage. Lucky you!")

file_name = input("What do you want your transcript to be named: ")
file_name += ".txt"

player_name = input("Welcome to the game! What's your name? ")
print(f"Hello, {player_name} this will be fun!")

playable_chars = [
    Character("Bard", 100, 10, 5, 5),
    Character("Wizard", 100, 15, 10, 5),
    Character("Cleric", 85, 20, 15, 5),
    Character("Barbarian", 80, 25, 20, 10),
    Character("Monk", 75, 25, 25, 10)]

NPC_options = [
    Character("Ranger", 80, 15, 15, 10),
    Character("Paladin", 90, 10, 10, 10),
    Character("Warlock", 70, 20, 20, 10)
]

char_selection = False
selected_character = None

for item in playable_chars:
    print(f"Player type: {item.type} health: {item.health} attack: {item.attack} dodge: {item.dodge} attack dice: {item.attack_dice}")

while not char_selection:
    selected_type = input("Now please choose a character by typing the type: ").capitalize()
    for character in playable_chars:
        if selected_type == character.type:
            print("Great choice!")
            selected_character = character  
            char_selection = True
            break
    else:
        print("Please choose a valid character!")

char_selection = False
opponent_character = None

while not char_selection:
    opponent_type = input("Would you like to fight: \n Ranger \n Paladin \n Warlock (type random to randomize your opponent): ").capitalize()
    if opponent_type == "Random":
        opponent_character = random.choice(NPC_options)
        print("Great choice!")
        char_selection = True
    else:
        for npc in NPC_options:
            if opponent_type == npc.type:
                print("Great choice!")
                opponent_character = npc
                char_selection = True
                break
        else:
            print("Please pick a valid opponent!")

with open(file_name, 'w') as transcript_file:
    transcript_file.write(f"Player Name: {player_name}\n")
    transcript_file.write(f"Selected Character: {selected_character.type}\n")
    transcript_file.write(f"Opponent Character: {opponent_character.type}\n")
    transcript_file.write("\n")

    def combat(player_char, npc_char):
        player_health = player_char.health
        npc_health = npc_char.health
        round_number = 1

        while player_health > 0 and npc_health > 0:
            print(f"\nRound {round_number}: Choose your action:")
            player_move = input("Attack or Dodge? (A/D): ").lower()

            while player_move not in ['a', 'd']:
                print("This is not an option; Choose your action: ")
                player_move = input("Attack or Dodge? (A/D): ").lower()

            npc_move = random.randint(0, 1)
            if player_move == "a":
                player_damage = player_char.calculate_damage()
                npc_damage = npc_char.calculate_damage()
                npc_health = max(npc_health - npc_damage, 0)
                player_health = max(player_health - player_damage, 0)
                damage_result(player_damage, npc_damage, transcript_file)
            else:
                npc_damage = npc_char.calculate_damage()
                player_health = max(player_health - player_char.calculate_dodge_r(npc_damage), 0)
                damage_result(0, npc_damage, transcript_file)

            round_number += 1

        print("Game Over!")
        print(f"You are {selected_character.type} and your opponent is {opponent_character.type}")
        print(f"Your final health is {player_health} and your opponent's final health is {npc_health}")

        if player_health <= 0:
            result = f"Sorry {player_name} you were defeated by {opponent_character.type}! Better luck next time."
            print(result)
            transcript_file.write(result + '\n')
        else:
            result = f"Congratulations {player_name}! You defeated {opponent_character.type}!"
            print(result)
            transcript_file.write(result + '\n')

    combat(selected_character, opponent_character)
