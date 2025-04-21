#!/usr/bin/python3

#Developer Notes and Documentation:
'''
/bin/python3 "/home/haim/VS Code/Projects/The_Lost_Realm/The_Lost_Realm.py"

To Do:
- To allow different merchants, stores, taverns, etc. to have their own available characters, pass characters as parameters
- Simplify all while loops for player input into a function in a class
- Allow for exploration within locations
- ascii images in separate files to introduce a visual aspect to the game
- Magic system
- Write more material
- Look into textwrap module

Documentation:
- The game currently runs by the character going to locations via the travel menu and all game-related events triggered by the player going to certain locations, with different functions activated in different locations
'''

import random
import sys

#Shortcuts for commonly used strings:
dotted_line = "-------------------------------"
input_error_message = "ERROR: INCORRECT INPUT. Please try again."
bankrupt_error_message = "Adventurer, you need a bit more money to buy that!"

#Useful functions:
def enter_to_continue():
    player_input = input("Press enter to continue:")
    while player_input != "":
        print(input_error_message)
        player_input = input("Press enter to continue:")
    print("")

def enter():
    player_input = input("")
    while player_input != "":
        print(input_error_message)
        player_input = input("")
    print("")

#Classes:
class Item:
    def __init__(self,name,market_value):
        self.market_value = market_value
        self.name = name

    def __str__(self):
        return f'{self.name}'

class Weapon(Item):
    def __init__(self,name,damage,durability,market_value):
        super().__init__(name,market_value)
        self.damage = damage
        self.durability = durability

    def __str__(self):
        return f'{self.name}, Damage: {self.damage}, Durability: {self.durability}, Market Value: {self.market_value}'
        
class Drink(Item):
    def __init__(self,name,health,market_value):
        super().__init__(name,market_value)
        self.health = health

    def __str__(self):
        return f'{self.name}; Restores {self.health} health; Market Value: {self.market_value}'

class NPC:
    def __init__(self,name,dialogue_list,dialogue_dict):
        self.name = name
        self.dialogue_list = dialogue_list
        self.dialogue_dict = dialogue_dict

    def chat(self):
        print(random.choice(self.dialogue_list))

    def hello(self):
        print(self.dialogue_dict["hello"])

    def farewell(self):
        print(self.dialogue_dict["farewell"])

class Merchant(NPC):
    def __init__(self,name,dialogue_list,dialogue_dict):
        super().__init__(name,dialogue_list,dialogue_dict)
    
    def sell_chat(self):
        print(self.dialogue_dict["sell"])

    def farewell(self):
        return super().farewell()
    
    def hello(self):
        return super().hello()
    
    def chat(self):
        return super().chat()

class Location:
    def __init__(self,name):
        self.name = name

class Area(Location):
    def __init__(self,name,index):
        super().__init__(name)
        self.index = index

class Store(Location):
    def __init__(self,merchandise,merchant,name,description):
        self.merchandise = merchandise #This is a list of objects
        self.merchant = merchant #This is an object of the Character class, represents the merchant of this market
        self.description = description
        super().__init__(name)
        #self.description = description #A description of the place
        
    def enter(self):
        print("You enter the " + self.description["type"] + ".")
        print(dotted_line)
        self.merchant.hello()
        while True:
            print(dotted_line)
            print("Hello traveler! Would you like to buy anything?")
            print("1: yes")
            print("2: leave")
            print("3: I'd like to chat")
            print("4: I'd like to explore the " + self.description["type"])
            player_input = input(":")

            if '1' in player_input: 
                self.merchant.sell_chat()
                print(dotted_line)
                hero.buy(self.merchandise)
                enter_to_continue()

            if '2' in player_input: 
                self.merchant.farewell()
                print(dotted_line)
                enter_to_continue()
                hero.travel_menu()
                break

            if '3' in player_input:
                while True:
                    print(dotted_line)
                    self.merchant.chat()
                    while True:
                        player_input = input("Do you wish to keep talking?(yes/no):")
                        if "no" or "yes" in player_input: break
                        else:
                            print(input_error_message)
                            continue

                    if "no" in player_input:
                        break
                    
                    if "yes" in player_input:
                        continue
            
            if '4' in player_input:
                print(self.description["explore"])
                enter_to_continue()

class Player: #Player data and player functions are stored in this class
    def __init__(self,health,balance,inventory,strength,health_cap,locations,current_area):
        self.health = health #Amount of health meter filled
        self.balance = balance #Amount of money the player has
        self.inventory = inventory #A list of objects that the player owns
        self.strength = strength #The damage a player can inflict on his own. This is added together with his current weapon
        self.health_cap = health_cap #The length of the health meter
        self.locations = locations #This will be a dictionary of allowed locations
        self.current_area = current_area #This number represents an area of the world where the player is. It is used as an index while selecting where to travel to, in order to only show locations in the player's current area.
    
    def buy(self,merchandise):
        for item in merchandise:
            print(item)
            print(dotted_line)

        while True:
            player_input = input("(input item):")
            if any(item.name == player_input for item in merchandise):
                for item in merchandise:
                    if player_input == item.name:
                        if self.balance >= item.market_value:
                            self.inventory.append(item)
                            self.balance -= item.market_value
                            self.inventory_menu()
                        else:
                            print(bankrupt_error_message)
                            enter_to_continue()
                break
            else:
                print(input_error_message) 
                continue
    
    def inventory_menu(self):
        print(dotted_line)
        if self.inventory == []:
            print("Balance: " + str(self.balance))
            print(dotted_line)
            print("Inventory is currently empty. Please check again when you have bought or found something.")
            print(dotted_line)
            enter_to_continue()
        else:
            print("Inventory:")
            print(dotted_line)
            for item in self.inventory:
                print(item)
                print(dotted_line)
            print("Balance: " + str(self.balance))
            print(dotted_line)
            while True:
                player_input = input("Would you like to equip or consume an item (yes/no)?:")
                if "yes" in player_input:
                    player_input = input("Type desired item:")
                    if any(item.name == player_input for item in self.inventory):
                        for item in self.inventory:
                            if player_input == item.name:
                                if type(item) == Drink:
                                    self.health += item.health
                                    print("HP: " + str(self.health))
                                elif type(item) == Weapon:
                                    self.strength += item.damage
                                    print("Strength: " + str(self.strength))
                                else: print("Error: " + item.name + ": class not found")
                                self.home_menu()
                        break
                    else:
                        print(input_error_message)
                        continue
                elif "no" in player_input:
                    self.home_menu()
                else:
                    print(input_error_message) 
                    continue

    def home_menu(self):
        print(dotted_line)
        print("Home Menu:")
        print(dotted_line)
        print("1: Travel Menu")
        print(dotted_line)
        print("2: Inventory")
        print(dotted_line)
        print("3: Quit")
        print(dotted_line)

        while True:
            player_input = input("(Type number):")
            if "1" in player_input: 
                hero.travel_menu()
                break
            if "2" in player_input:
                self.inventory_menu()
                break
            elif "3" in player_input: sys.exit(dotted_line + "\nGame Over. Play again!")
            else:
                print(input_error_message)
                continue
    
    def travel_menu(self):
        i = 1
        print(dotted_line)
        print("Travel Menu:")
        print("Your location: " + self.current_area.name)
        print(dotted_line)
        for location in self.locations[self.current_area.index]:
            print(str(i) + ": " + location.name)
            print(dotted_line)
            i += 1
        print(str(i) + ": Home Menu")
        print(dotted_line)
        
        j = 1
        while True:
            player_input = input("Where to, traveler?(type number):")
            if str(i) not in player_input:
                for location in self.locations[self.current_area.index]:
                    if str(j) in player_input:
                        self.locations[self.current_area.index][j-1].enter()
                        break
                    j += 1
                else:
                    print(input_error_message)
                    continue
            else: self.home_menu()

#Variables used in objects that are just too long to write in the parameters:
#Dialogue
torgon_dialogue_gen =  [
    "Strange things have been happening in these parts...",
    "Do you think this hat looks good on me? Nevermind...",
    "You know, I have some killer deals...",
    "You know the blacksmith, Thordar? He thinks his custom swords of soooo amazing but check out my options!",
    "Check out the local tavern, traveler, you'll meet some interesting characters there.",
    "Have you ever held a weapon as good as mine? I wouldn't go adventuring without these blades."]

torgon_dialogue_pick = {
    "hello": "Hello there traveler!",
    "sell": "Take a gander at my wares!",
    "farewell": "Come back again traveler!"
}

helard_dialogue_gen = [
    "You know Torgon? He's talking about my place as if it's suspicious. What does he mean by 'you'll meet some interesting characters there' hmmm?",
    "You know, this tavern is one of the oldest establishments in  this village. So ancient, it was once visited by the knights of old, in the Era of Tranquility just two hundered years ago. With roving packs of orcs disrupting my supply lines, the world is in pretty bad shape, especially if it has no place to drink.",
    "I heard rumours that to the east the Fire King plans to conquer the Bastion of Light once and for all. If he does that, the world will break its final straw.",
    "Adventurer, if you want better armor and weapons, head east to the Grey Mountains. In the dwarven mines there I have a friend, Thordar. He's a blacksmith, you'll need upgrades if you want to survive.",
    "I myself as an adventurer way back when. Slayed a dragon even, but that's all past. I settled down to take over the family tavern business."]

helard_dialogue_pick = {
    "hello": "You enter the town's tavern, and a man behind the counter begins to talk to you.",
    "sell": "So, here's a menu, tell me what you want to drink",
    "farewell": "Until next time, adventurer!"
}

helard_tavern_description = {
    "explore": "You stride through the wooden tavern, past strange creatures of unknown lands, gruff dwarves and sharp elves among them, and kindly village people relaxing after a long day's work. As you past table after table, past the ancient smell and laughter streaming though the warm air.",
    "type": "tavern"
}

torgon_shoppe_description = {
    "explore": "You take a gander 'round the smooth dark oak shelves, eyeing an array of weapons and other items. Maybe something useful for the adventure, but you're not sure.",
    "type": "shoppe"
}

#Objects:
#Merchant Objects
torgon = Merchant("Torgon",torgon_dialogue_gen,torgon_dialogue_pick)
helard = Merchant("Helard",helard_dialogue_gen,helard_dialogue_pick)

#Weapon Objects
sword = Weapon("Sword",15,20,10)
wooden_axe = Weapon("Wooden Axe",30,10,10)
battle_axe = Weapon("Battle Axe",40,30,20)
spear = Weapon("Spear",40,10,20)

#Drink Objects
beer = Drink("Beer",5,5)
iced_coffee = Drink("Iced Coffee",8,8)
iced_tea = Drink("Iced Tea",8,8)
health_elixir = Drink("Health Elixer",20,15)

#Item Object Lists
weapons = [sword,wooden_axe,battle_axe,spear]
drinks = [beer,iced_coffee,iced_tea,health_elixir]

#Location Objects
torgon_shoppe = Store(weapons,torgon,"Torgon's Shoppe",torgon_shoppe_description)
helard_tavern = Store(drinks,helard,"Helard's Tavern",helard_tavern_description)
sleepy_village = Area("Sleepy Village",0)

#Hero
hero = Player(50,20,[],5,50,[],sleepy_village)
hero.locations = [[helard_tavern,torgon_shoppe]]

#The Game:
print("""
 ████████ ██   ██ ███████     ██       ██████  ███████ ████████     ██████  ███████  █████  ██      ███    ███ 
    ██    ██   ██ ██          ██      ██    ██ ██         ██        ██   ██ ██      ██   ██ ██      ████  ████ 
    ██    ███████ █████       ██      ██    ██ ███████    ██        ██████  █████   ███████ ██      ██ ████ ██ 
    ██    ██   ██ ██          ██      ██    ██      ██    ██        ██   ██ ██      ██   ██ ██      ██  ██  ██ 
    ██    ██   ██ ███████     ███████  ██████  ███████    ██        ██   ██ ███████ ██   ██ ███████ ██      ██ 
---------------------------------------------------------------------------------------------------------------
    """)
enter_to_continue()
print("Welcome to the Lost Realm, adventurer!", end = "")
enter()
print("An unknown land lies before you, and terrible dangers seek your life.")
print("The risk is great, but so is the reward, if you relieve this land of its misery.")
print("To you I bequeath this quest, and the luck that you shall need in it.")
print("But you must make haste.", end = "")
enter()
print("A great adventure lies before you, to free this realm from the darkness that has plagued it.")
print("Good luck, hero!")
enter_to_continue()
print("You begin your adventure in a sleepy, quaint village. Smoke lazily rises from small cottages in the afternoon light.")
enter_to_continue()
print("This is your travel menu. Use it to travel to your desired destination. Listed are the nearby locations you may travel to.")
hero.travel_menu() #This kicks off the game. All further player action is done by jumping between functions.