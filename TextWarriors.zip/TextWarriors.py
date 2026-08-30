import sys
import time
import os
import random
import json
import requests
import re

player_stats = {"health": 100.0, "stamina": 100.0, "min_damage": 5, "max_damage": 7, "xp": 0, "ready": False, "difficulty": "unset", "dev_logs": False, "in_game": False, "inventory": {"healing_potion": 2, "stamina_potion": 1, "super_healing_potion": 0}}
enemy_stats = {"health": 0.0, "damage": 0.0, "stamina": 0.0}
BANNED_WORDS = ["admin", "dev", "mod", "fuck", "shit", "bitch", "asshole", "nigger", "cunt"]

def validate_player_name(name):
    clean_name = name.strip()
    
    if not clean_name:
        return False, "Name cannot be blank!"
    
    if len(clean_name) < 3:
        return False, "Name must be at least 3 characters long."
    if len(clean_name) > 16:
        return False, "Name cannot exceed 16 characters."
        
    if not re.match(r"^[a-zA-Z0-9_\- ]+$", clean_name):
        return False, "Name can only contain letters, numbers, spaces, underscores, and hyphens."
        
    if re.search(r"(.)\1{3,}", clean_name):
        return False, "Name contains too many repeated characters."
        
    name_lower = clean_name.lower()
    for word in BANNED_WORDS:
        if word in name_lower:
            return False, f"Name contains forbidden text: '{word}'"
            
    return True, clean_name

def send_win_online(player_name):
    url = "https://docs.google.com/forms/d/e/1FAIpQLScmMy70jirC-qWpvm704g-nHQIqrIQP4mMiBxHfr-3YL6BaCg/formResponse"

    form_data = {
            "entry.760151206": player_name,
            "entry.502503112": "Completed"
        }
    try:
        response = requests.post(url, data=form_data, timeout=3)
        if response.status_code == 200:
            print("Victory recorded in the Online Hall of Fame!")
    except Exception:
        print("Could not connect online. Victory saved locally.")

def open_shop():
    clean_screen()
    print("Welcome to the shop! ")
    print("[H] -> Healing Potion - 10 XP")
    print("[SH] -> Super Healing Potion - 50 XP")
    print("[S] -> Stamina Potion - 10 XP")
    print("[C] -> Completion - 100 XP")
    print("-----------------")
    choise = input("Choose what to buy: ").lower().rstrip()
    inv = player_stats["inventory"]
    if choise == "h":
        if player_stats["xp"] >= 10:
            player_stats["xp"] -= 10
            inv["healing_potion"] += 1


            
        else:
            if random.randint(1,10) > 8:
                print("your to broke LOL UR SO BROKE U FUCKING CHUMP LMAOOOOOOOOOOOOOOOOOO")
            else:
                print("Not enough XP!")
    elif choise == "sh":
        if player_stats["xp"] >= 50:
            player_stats["xp"] -= 50
            inv["super_healing_potion"] += 1
        else:
            if random.randint(1,10) > 8:
                print("your to broke LOL UR SO BROKE U FUCKING CHUMP LMAOOOOOOOOOOOOOOOOOO")
            else:
                print("Not enough XP!")
    elif choise == "s":
        if player_stats["xp"] >= 10:
            player_stats["xp"] -= 10
            inv["stamina_potion"] += 1
        else:
            if random.randint(1,10) > 8:
                print("your to broke LOL UR SO BROKE U FUCKING CHUMP LMAOOOOOOOOOOOOOOOOOO")
            else:
                print("Not enough XP!")
    elif choise == "c":
        if player_stats["xp"] >= 100:
            player_stats["xp"] -= 100
            raw_name = input("What is your name: ")
            validate_player_name(raw_name)
            is_valid, result = validate_player_name(raw_name)
            if is_valid:
                send_win_online(result)
            else:
                print(f"Invalid Name: {result}")
        else:
            if random.randint(1,10) > 8:
                print("your to broke LOL UR SO BROKE U FUCKING CHUMP LMAOOOOOOOOOOOOOOOOOO")
            else:
                print("Not enough XP!")


def open_inventory():
    clean_screen()
    inv = player_stats["inventory"]
    print("\n--- INVENTORY ---")
    print(f"[H]  Healing Potion:       {inv['healing_potion']}")
    print(f"[SH] Super Healing Potion: {inv['super_healing_potion']}")
    print(f"[S]  Stamina Potion:       {inv['stamina_potion']}")
    print("-----------------")
    
    choice = input("Use item (H / SH / S) or enter to exit: ").strip().lower()

    if choice == "h":
        if inv["healing_potion"] > 0:
            inv["healing_potion"] -= 1
            player_stats["health"] = player_stats["health"] + 30.0
        else:
            print("You have no Healing Potions!")

    elif choice == "sh":
        if inv["super_healing_potion"] > 0:
            inv["super_healing_potion"] -= 1
            player_stats["health"] = player_stats["health"] + 80.0
        else:
            print("You have no Super Healing Potions!")

    elif choice == "s":
        if inv["stamina_potion"] > 0:
            inv["stamina_potion"] -= 1
            player_stats["stamina"] = player_stats["stamina"] + 40.0
        else:
            print("You have no Stamina Potions!")

def save_game(stats, filename="savegame.json"):
    with open(filename, "w") as file:
        json.dump(stats, file, indent=4)
    print("Saved data")

def load_game(filename="savegame.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            stats = json.load(file)
        print("Game loaded!")
        return stats
    else:
        print("No save file found.")
        return None

def find_enemy_stats():
    if player_stats["difficulty"] == "e":
        enemy_stats["health"] = random.randint(50, 80)
        enemy_stats["stamina"] = random.randint(70, 90)
    elif player_stats["difficulty"] == "n":
        enemy_stats["health"] = random.randint(70, 100)
        enemy_stats["stamina"] = random.randint(90, 120)
    elif player_stats["difficulty"] == "h":
        enemy_stats["health"] = random.randint(100, 130)
        enemy_stats["stamina"] = random.randint(100, 150)
    elif player_stats["difficulty"] == "ex":
        enemy_stats["health"] = random.randint(140, 170)
        enemy_stats["stamina"] = random.randint(160, 200)
    print("Enemy HP: ", enemy_stats["health"])
    print("Enemy Stamina: ", enemy_stats["stamina"])

def enemy_damage():
    if player_stats["difficulty"] == "e":
        enemy_stats["damage"] = random.randint(5, 7)
    elif player_stats["difficulty"] == "n":
        enemy_stats["damage"] = random.randint(8, 12)
    elif player_stats["difficulty"] == "h":
        enemy_stats["damage"] = random.randint(12, 15)
    elif player_stats["difficulty"] == "ex":
        enemy_stats["damage"] = random.randint(15, 18)
    if player_stats["dev_logs"]:
        print("Enemy DMG: ", enemy_stats["damage"], " DEV LOG")

def clean_screen():
    os.system('clear')

def confirmstart(confirm_start):
    if confirm_start.lower() == "y":
        player_stats["ready"] = True

        print("Welcome to the lands of the Text Gods! Please choose the difficulty: (E (easy) N (normal) H (hard) EX(extreme))")
        player_stats["difficulty"] = input().lower()
        if player_stats["dev_logs"]:
            print(player_stats["difficulty"])
        time.sleep(0.5)

        txl1 = input("Welcome to the Text Plains. This is where you earn your first TextLine. A Textline is a stat booster, however you may also lose stats based on what you get. Please choose your TextLine: Strength I (S1), + 5 Strength but - 10 Stamina, Tank I (T1), + 25 Health but - 10 Stamina, or Athlete I (A1) + 25 Stamina but - 2 Damage:" )
        if txl1.lower() == "s1":
            player_stats["damage"] = player_stats["max_damage"] + 5
            player_stats["stamina"] = player_stats["stamina"] - 10
            if player_stats["dev_logs"] == True:
                print("Class1: ", txl1.lower(), " | Damage: ", player_stats["max_damage"], " | Stamina: ", player_stats["stamina"])
        elif txl1.lower() == "t1":
            player_stats["health"] = player_stats["health"] + 25
            player_stats["stamina"] = player_stats["stamina"] - 10
            if player_stats["dev_logs"]:
                print("Class1: ", txl1.lower(), " | Health: ", player_stats["health"], " | Stamina: ", player_stats["stamina"])
        elif txl1.lower() == "a1":
            player_stats["damage"] = player_stats["max_damage"] - 2
            player_stats["stamina"] = player_stats["stamina"] + 25
            if player_stats["dev_logs"]:
                print("Class1: ", txl1.lower(), " | Damage: ", player_stats["max_damage"], " | Stamina: ", player_stats["stamina"])
        else:
            print("Err: Invalid Argument. S1 has been chosen for you! ")
            txl1 = "S1"
            player_stats["damage"] = player_stats["max_damage"] + 5
            player_stats["stamina"] = player_stats["stamina"] - 10
            if player_stats["dev_logs"] == True:
                print("Class1: ", txl1.lower(), " | Damage: ", player_stats["max_damage"], " | Stamina: ", player_stats["stamina"])

        time.sleep(0.5)
        print("Now that you have everything you need, go fight some other Texts!")
        player_stats["in_game"] = True
        clean_screen()

    elif confirm_start.lower() == "n":

        print("Well why the fuck did you open this. (closing terminal)")
        time.sleep(3.0)
        os.system("kill -9 $PPID")

    elif confirm_start.rstrip() == "Dev_Tools":

        print("Welcome to Dev Tools. This allows you to customise your health, damage or stamina.")
        item_choise = input("What would you like to edit?: ")
        if item_choise.lower() == "health" or item_choise.lower() == "hp":
            player_stats["health"] = float(input("Please enter your new Health value: "))
            print("Health is now: ", player_stats["health"])
        elif item_choise.lower() == "damage" or item_choise.lower() == "dmg":
            player_stats["max_damage"] = int(input("Please enter your new Damage value: "))
            print("Max Damage is now: ", player_stats["max_damage"])
        elif item_choise.lower() == "stamina" or item_choise.lower() == "stm":
            player_stats["stamina"] = int(input("Please enter your new Stamina value: "))
            print("Stamina is now: ", player_stats["stamina"])
        elif item_choise.lower() == "dvl":
            if player_stats["dev_logs"] == False:
                player_stats["dev_logs"] = True
                print("Dev Logs are now enabled")
            else:
                player_stats["dev_logs"] = False
                print("Dev Logs are now disabled")
        elif item_choise.lower() == "xp":
            player_stats["xp"] = float(input("Please enter an XP amount: "))
            print("Stamina is now: ", player_stats["xp"])
        else:
            print("Error: Unknown variable. (closing terminal)")
            time.sleep(3.0)
            os.system("kill -9 $PPID")

while True:

    if player_stats["ready"] == False and player_stats["in_game"] == False:
        confirm_start = input("Welcome to Text Warriors! Are you ready to start? Y/n: ")
        confirmstart(confirm_start)
    elif player_stats["ready"] == True and player_stats["in_game"] == True:
        
        print("What would you like to do? View stats[VS], Go Battle[B], Save Data[SD], Load Data[LD], Inventory[I], Shop[S], ")
        action = input().lower()
        if action == "sd":
            save_game(player_stats)
        elif action == "ld":
            
            saved_stats = load_game()
            if saved_stats:
              player_stats = saved_stats
        elif action == "vs":
            clean_screen()

            print("Health: ", player_stats["health"])
            print("Max Damage: ", player_stats["max_damage"])
            print("Stamina: ", player_stats["stamina"])
            print("XP: ", player_stats["xp"])
            if player_stats["dev_logs"]:
                print("max damage: ", player_stats["max_damage"])
                print("ready: ", player_stats["ready"])
                print("difficulty: ", player_stats["difficulty"])
                print("dev_logs: ", player_stats["dev_logs"])
                print("in_game: ", player_stats["in_game"])
        elif action == "b":
            
            print("searching.")
            time.sleep(0.75)
            clean_screen()
            print("searching..")
            time.sleep(0.75)
            clean_screen()
            print("searching...")
            time.sleep(0.75)
            clean_screen()
            find_enemy_stats()
            enemy_damage()
            player_stats["ready"] = False
            print("You have encountered another TextFile!")
            in_battle = True
            while in_battle == True:

                print("Your current stats are: ")
                print("Health: ", player_stats["health"])
                print("Max Damage: ", player_stats["max_damage"])
                print("Stamina: ", player_stats["stamina"])
                

                decision = input("What do you want to do? Attack[A], Rest[R], Run[RU], Inv[I]: ").lower()
                if decision == "a":
                    clean_screen()
                    if player_stats["stamina"] >= 15:
                        player_stats["stamina"] = player_stats["stamina"] - random.randint(10,15)
                        enemy_stats["health"] -= random.randint(player_stats["min_damage"], player_stats["max_damage"])

                    print("Enemy HP: ", enemy_stats["health"])
                    print("Enemy Stamina: ", enemy_stats["stamina"])

                    if enemy_stats["health"] <= 0.0:
                        print("You have defeated the TextFile. +10xp. Returning to choices...")
                        player_stats["xp"] = player_stats["xp"] + 10
                        time.sleep(2.5)
                        clean_screen()
                        in_battle = False 
                        player_stats["ready"] = True
                    else:
                        if enemy_stats["stamina"] >= 15:
                            enemy_stats["stamina"] -= random.randint(10, 15)
                            player_stats["health"] = player_stats["health"] - enemy_stats["damage"]
                            print("You took ", enemy_stats["damage"], " damage!")
                            enemy_damage()
                            if player_stats["health"] <= 0.0:
                                clean_screen()
                                print("You have perished. It was a good attempt. [killing terminal]")
                                os.system("kill -9 $PPID")
                        else:
                            print("Enemy is resting!")
                            enemy_stats["stamina"] += random.randint(10, 20)
                elif decision == "r":
                    clean_screen()
                    amount = random.randint(10, 20)
                    print("You are resting. You will gain ", amount, " stamina next turn.")
                    player_stats["stamina"] += amount

                    if enemy_stats["stamina"] >= 15:
                        enemy_stats["stamina"] -= random.randint(10, 15)
                        player_stats["health"] = player_stats["health"] - enemy_stats["damage"]
                        print("You took ", enemy_stats["damage"], " damage!")
                        enemy_damage()
                        if player_stats["health"] <= 0.0:
                            clean_screen()
                            print("You have perished. It was a good attempt. [killing terminal]")
                            os.system("kill -9 $PPID")
                        else:
                            print("Enemy is resting!")
                            enemy_stats["stamina"] += random.randint(10, 20)
                elif decision == "ru":
                    clean_screen()
                    if random.randint(1,2) == 1:
                        print("You successfully ran away! (coward). Returning to choises...")
                        time.sleep(2.5)
                        clean_screen()
                        in_battle = False 
                        player_stats["ready"] = True
                    else:
                        print("Failed to run away!")
                        if enemy_stats["stamina"] >= 15:
                            enemy_stats["stamina"] -= random.randint(10, 15)
                            player_stats["health"] = player_stats["health"] - enemy_stats["damage"]
                            print("You took ", enemy_stats["damage"], " damage!")
                            enemy_damage()
                            if player_stats["health"] <= 0.0:
                                clean_screen()
                                print("You have perished. It was a good attempt. [killing terminal]")
                                os.system("kill -9 $PPID")
                        else:
                            print("Enemy is resting!")
                            enemy_stats["stamina"] += random.randint(10, 20)
                elif decision == "i":
                    open_inventory()
        elif action == "i":
            clean_screen()
            open_inventory()
        elif action == "s":
            clean_screen()
            open_shop()