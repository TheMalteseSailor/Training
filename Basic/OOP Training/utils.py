#!/usr/bin/python3

import random
import os
import json

def produce_room_template(room_number):
    #print("produce_room_template()")
    room = {
        "room_number": room_number,
        "enemies": [],
        "treasure": [],
        "details": [],
        }
    
    if room_number < 4:
        room['treasure'].append(get_treasure())
        num_of_enemies = random.randint(1,2)
        while num_of_enemies > 0:
            num_of_enemies -= 1
            room["enemies"].append(Enemy())
    elif room_number == 4:
        room['treasure'].append(["boss_key",True])
        num_of_enemies = random.randint(1,2)
        while num_of_enemies > 0:
            num_of_enemies -= 1
            room["enemies"].append(Enemy(final_boss=True))
    elif room_number == 5:
        room["enemies"].append(Enemy(final_boss=True))
    else:
        # This will be the final room... the Boss fight
        pass

    #print(room)
    #print()
    return room

def loot_drop(scenario):
    # this will be a general function to handle the dropping of loot in a space by an enemy of treasure chest.
    pass

class Enemy:
    def __init__(self, final_boss=False):
        self.final_boss = final_boss
        self.stats = {
            "health" : 100,
            "weapons" : self.get_weapons(),
            "armor" : self.get_armor_meth()
            }

        if self.final_boss == False:
            determine_if_special = random.randint(0,20)
            if determine_if_special >= 15:
                self.stats["health"] = self.stats["health"] * 3
                self.stats["armor"][1] = self.stats["armor"][1] + 5
                for index, weapon in enumerate(self.stats["weapons"]):
                    self.stats["weapons"][index][1] = self.stats["weapons"][index][1] * 2
                    #print(self.stats["weapons"][index])

   
    def get_weapons(self):
        number_of_weapons = random.randint(0,9)
        weapons = []
        if number_of_weapons <= 5:
            weapons.append(get_weapon())
            weapons.append(get_weapon())
        else:
            weapons.append(get_weapon())                           

        return weapons

    def get_armor_meth(self):
        return get_armor()


def get_weapon():
    weapons = {
        "short_sword": 15,
        "long_sword": 20,
        "dagger": 5,
        "spear": 20
        }
    item_number = random.randint(0,3)
    for index, value in enumerate(weapons.keys()):
            if index == item_number:
                    return [value,weapons[value]]
               

def get_armor():
    armor = {
        "breast_plate": 10,
        "helmet": 5,
        "shield": 10,
        "greaves": 5,
        "gauntlets": 5
        }
    item_number = random.randint(0,4)
    for index, value in enumerate(armor.keys()):
            if index == item_number:
                    return [value,armor[value]]



def get_treasure():
    coin_flip = random.randint(0,5)
    if coin_flip == 0:  
        return get_weapon()
    elif coin_flip == 1:
        return get_armor()
    else:
        heart = random.randint(5,50)
        return ["heart", heart]


def roll_dice():
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)

    return [die1, die2, die1+die2]

class Hero():
    # need storage
    def __init__(self, name):
        self.name = name
        self. create_hero_json_object()
        self.write_hero_object_to_disk()

    def create_hero_json_object(self):
        weapons = get_weapon()
        armor = get_armor()
        hero_attribs = {
            "name": self.name,
            "health": 100,
            "armor": armor,
            "weapons": weapons,
            "boss_key": False
            }
        self.hero_attribs = hero_attribs

    def write_hero_object_to_disk(self):
        serializedHero = json.dumps(self.hero_attribs, indent=4)
        with open("HeroObject.json", "w") as _wf:
            _wf.write(serializedHero)



def youDied():
    #os.system("cls")
    print('''


                                                           ..          .                  ..       
           .xnnx.  .xx.                                   dF           @88>              dF         
         .f``"888X< `888.         u.      x.    .        '88bu.        %8P              '88bu.      
         8L   8888X  8888   ...ue888b   .@88k  z88u      '*88888bu      .         .u    '*88888bu   
        X88h. `8888  X888k  888R Y888r ~"8888 ^8888        ^"*8888N   .@88u    ud8888.    ^"*8888N  
        '8888 '8888  X8888  888R I888>   8888  888R       beWE "888L ''888E` :888'8888.  beWE "888L 
         `*88>'8888  X8888  888R I888>   8888  888R       888E  888E   888E  d888 '88%"  888E  888E 
           `! X888~  X8888  888R I888>   8888  888R       888E  888E   888E  8888.+"     888E  888E 
          -`  X*"    X8888 u8888cJ888    8888 ,888B .     888E  888F   888E  8888L       888E  888F 
           xH88hx  . X8888  "*888*P"    "8888Y 8888"     .888N..888    888&  '8888c. .+ .888N..888  
         .*"*88888~  X888X    'Y"        `Y"   'YP        `"888*""     R888"  "88888%    `"888*""   
         `    "8%    X888>                                   ""         ""      "YP'        ""      
            .x..     888f                                                                           
           88888    :88f                                                                            
           "88*"  .x8*~      
           

    ''')
    return

def LaunchHud():
    from subprocess import Popen
    #print(os.getcwd()+"\\"+"utils.py")
    #hud_process = Popen(["start","cmd.exe","\k","python",os.getcwd()+"\\"+"utils.py"], shell=True)
    os.system("start cmd /c python "+os.getcwd()+"\\"+"utils.py")
    return
    
def Hud():
    from time import sleep

    while True:
        # I need to read from the json object on disk to ascertain the details of what to print to screen
        hero_stats = ''
        with open("HeroObject.json", 'r') as _rf:
            hero_stats = json.load(_rf)

        hero_pic = r"""
     /\
     ||
     ||
     ||
     ||           {}
     ||          .--.
     ||         /.--.\
     ||         |====|
     ||         |`::`|
    _||_    .-;`\..../`;_.-^-._
     /\\   /  |...::..|`   :   `|
     |:'\ |   /'''::''|   .:.   |
      \ /\;-,/\   ::  |..:::::..|
       \ <` >  >._::_.| ':::::' |
        `""`  /   ^^  |   ':'   |
              |       \    :    /
              |        \   :   /
              |___/\___|`-.:.-`
               \_ || _/    `
               <_ >< _>
               |  ||  |
               |  ||  |
              _\.:||:./_
             /____/\____\
        """

        stats = {
            "Health": hero_stats["health"],
            "Armor": hero_stats["armor"],
            "Weapons": hero_stats["weapons"]
        }


        # This is what the dungeon layout will be 


        '''
        +=============| |=============+
        |                             |     Room number: 
        |                             |     Enemies:
        |                             |     Treasure:
        |                             |
        |                             |
        |                             |
        |                             |
        |                             |
        +=============| |=============+
        '''

        # This line will present the knight and display derp. 
        # derp will be replaced by the health information
        for index, lines in enumerate(hero_pic.split("\n")):
            if index == 0:
                print("{0:6}   Name: {1}{2:25}".format(lines, hero_stats["name"],''))
            elif index == 1:
                print("{0:5}  Health: {1}{2:25}".format(lines, stats["Health"],''))
            elif index == 2:
                print("{0:5}  Armor: {1:25}".format(lines, ''.join(stats["Armor"][0])))
            elif index == 3:
                print("{0:5}  Weapons: {1:25}".format(lines, ''.join(stats["Weapons"][0])))
            else:
                print("{0:30}".format(lines))

        sleep(3)
        #os.system("clear")
        os.system("cls")


    return


if __name__ == "__main__":
    Hud()


