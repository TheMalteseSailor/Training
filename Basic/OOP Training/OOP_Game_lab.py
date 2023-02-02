#!/usr/bin/python3

#from typing_extensions import final
import utils
import time
import os

class scenario():
    def __init__(self, name):
        self.realm_name = "Kingdom of Derp"
        self.hero_name = name
        self.dungeon_boss_key_captured = False
        self.instantiateWorld()
        self.createHero()

    def instantiateWorld(self):
        # The util.py will contain the template for each dungeon room
        # This will be a list of dictionaries and each index will be the room count
        self.dungeon = []
        counter = 6
        while counter > 0:
            counter -= 1
            self.dungeon.append(utils.produce_room_template(counter))
        if len(self.dungeon) != 6:
            print("[!] ERROR! world construction failure...")
            exit(-3)
        #print(self.dungeon)

        return

    def createHero(self):
        self.hero = utils.Hero(self.hero_name)
        return



def main():
    print("\tWelcome to Meh! An ok dungeon crawler game designed to exist.\n\n")

    name = ''
    try:
        name = input("What's your name great warrior? ")
    except:
        print("Since you can't get your name figured out You shouldn't embark on this quest. Bye.")
        exit(-1)

    # intantiate scenario object here
    world = scenario(name)
    # I need to build a dictionary that can be saved to disk with all the important HUD related details via json.
    
    print("Old man -- Welcome {0}! The land is in great danger!".format(name))
    time.sleep(1)
    print("Old man -- I've set aside what armor and weapons I could. I hope it helps!")
    time.sleep(1)

    input("[!] When ready hit enter.")
    os.system("cls")

    utils.LaunchHud()
    
    print("Narration - At the entrance of the frightful dungeon you see a piece of parchment on the ground.")
    time.sleep(2)
    print("Narration - You pick it up and read it.")

    print('''
       ____________________________________________________________
     / \                                                           \.
    |   |                                                           |.
     \_ |    Your weapon is sharp. Your armor is untested...        |.
        |    Face your fears and confront the ultimate MEH!         |.
        |    Few who confront the mighty Meh return..               |.
        |    Don't be like them...                                  |.
        |    Destroy the Meh and be renound throughout the land!    |.
        |                                                           |.
        |                          ~                                |.
        |                                                           |.
        |                   ~                                       |.
        |                                       ~                   |.
        |         ~                                                 |.
        |    Also... try not to die...                              |.
        |   ________________________________________________________|___
        |  /                                                           /.
        \_/___________________________________________________________/.
    \n''')

    location = 1
    while True:         
        # display game options
        # I still need to build out the dictionary of choices and the below checks for what's going on and how to track it.
        
        if location == 0:
            print('')
        elif (location >= 1) and (location <= 5):
            space = world.dungeon[location]
            enemies = space['enemies']
            treasure = space['treasure']

            print(" [-] Current room location: {0}".format(location))
            print(" [-] Enemies Present: ")
            for num, enemy in enumerate(enemies):
                print("\t [-] Enemy number: {0}".format(num + 1))
                print("\t [-] Enemy health: {0}".format(enemy.stats['health']))
                print("\t [-] Enemy weapons: {0}".format(enemy.stats['weapons']))
                print("\t [-] Enemy armor: {0}".format(enemy.stats['armor']))

            # The decision options will be displayed here.

        else:
            # Boss Battle
            # Location tracked
            space = world.dungeon[location]
            enemies = space.room['enemies']
            treasure = space.room['treasure']

        living_enemies = []
        enemies_defeated = False
        num_of_enemies = 0
        for num, enemy in enumerate(enemies):
            num_of_enemies += 1
            if enemy.stats['health'] <= 0 :
                living_enemies.append(False)
            else:
                living_enemies.append(True)
        if True not in living_enemies:
            enemies_defeated = True
            
        while True:
            # Get Player command input
            usr_input = input("[{}]> ".format(name))
            if (usr_input == '?') or (usr_input.lower() == 'help'):
                rules()
            elif usr_input.lower() == 'heal':
                world.hero.hero_attribs['health'] = 100
                print(" [!] Your health is now {0}".format(world.hero.hero_attribs['health']))
            elif (usr_input.lower() == ''):
                continue
            # Look at the current room's details
            elif usr_input.lower() == 'look':
                print("Current room location: {0}".format(location))
                print("Enemies Present: ")
                for num, enemy in enumerate(enemies):
                    print("\tEnemy number: {0}".format(num + 1))
                    print("\tEnemy health: {0}".format(enemy.stats['health']))
                    print("\tEnemy weapons: {0}".format(enemy.stats['weapons']))
                    print("\tEnemy armor: {0}".format(enemy.stats['armor']))
                print()
                print("Treasure: {0}".format(space['treasure']))
                print("")
                print("")
                print("")
                print("")

            elif (usr_input.lower() == 'chill'):
                for num, enemy in enumerate(enemies):
                    if enemy.stats['health'] > 0 :
                        print("That's a bold move cotton...")
                print("There is no time to waste... Quit sitting around...")
            elif (len(usr_input.split(" ")) > 1):
                split_input = usr_input.split(" ")
                # MOVE
                if split_input[0].lower() == 'move':
                    # Move FOWARD
                    if split_input[1].lower() == "forward":
                        if (location == 4) and (world.dungeon_boss_key_captured == False):
                            print(" [-] You cannot open the boss battle door because you don't have the key...")
                        elif enemies_defeated == False:
                            print(" [-] You tried to slip past the enemies, but they've blocked the door.")
                        elif location == 5:
                                print(" [-] You're in the final room. There is no next room to move into.")
                        else:
                            location += 1
                            print(" [-] You moved forward to the next room")
                            break

                    # Move BACKWARD
                    elif (split_input[1].lower() == "back") or (split_input[1].lower() == "backward"):
                        if location == 1:
                            dungeon_cleared = False
                            final_enemies = []
                            final_boss = world.dungeon[5]['enemies']
                            for __,boss in enumerate(final_boss):
                                if boss.stats['health'] <= 0:
                                    final_enemies.append(True)
                                else:
                                    final_enemies.append(False)
                            if True not in final_enemies:
                                dungeon_cleared = False

                            if  dungeon_cleared:
                                print(" [!] Congradulations! You won!")
                                exit(0)
                            else:
                                print(" [-] Don't be a coward. You can't leave now; you're already in it.")
                                continue
                        else:
                            # If location 1 and the final room shows the boss is dead you can exit the dungeon
                            # Show congratulations when you beat the game.
                            location -= 1
                            break
                    else:
                        print("Invalid Movement...")
                        continue
                # ATTACK
                elif split_input[0].lower() == 'attack':
                    # check for living enemies
                    if enemies_defeated == True:
                        print(" [-] There are no living enemies in this room.")
                        continue
                    # Attack specific enemy
                    if enemies[int(split_input[1])-1].stats['health'] == 0:
                        print(" [-] Enemey is already dead. You don't have time to stand around smacking dead enemies.")
                        continue
                    try:
                        # Calculate attack damage
                        # attack_results = [die1, die2, die1+die2]
                        roll_result =  utils.roll_dice()
                        weapons = world.hero.hero_attribs['weapons']
                        weapon_damage = 0

                        #for index,weapon in enumerate([weapons]):
                            #weapon_damage += weapons[index][1]
                        weapon_damage += weapons[1]
                            # attack_damage is the final attack value
                        attack_damage = weapon_damage + roll_result[2]

                        # Calculate defensive block value of enemy
                        armor = enemies[int(split_input[1])-1].stats['armor']
                        defensive_value = 0
                        #for index,value in enumerate(armor):
                                #defensive_value = armor[value]
                        if armor == []:
                            pass
                        else:
                            defensive_value = armor[1]
                        
                        final_damage = attack_damage - defensive_value
                        if final_damage < 0:
                            final_damage = 0
                        # subtract attack damage from enemy's health
                        print(" [-] You did {0} of damage to enemy # {1}".format(final_damage,split_input[1]))
                        enemies[int(split_input[1])-1].stats['health'] = enemies[int(split_input[1])-1].stats['health'] - final_damage
                        # Repleace negative health value with 0 
                        if enemies[int(split_input[1])-1].stats['health'] < 0:
                            enemies[int(split_input[1])-1].stats['health'] = 0

                        print(" [-] Enemy {0}'s health is down to {1}".format(split_input[1],enemies[int(split_input[1])-1].stats['health']))

                    # check for enemy death and perform item drop function that should be standardized between treasure chests and enemies.

                    except Exception as ex:
                        print(ex)
                        continue
                # TAKE
                elif split_input[0].lower() == 'take':
                    if split_input[1].lower() == 'treasure':
                        if (split_input[2].lower() == 'key') and ('boss_key' in treasure[0]):
                            world.dungeon_boss_key_captured = True
                            world.hero.hero_attribs["boss_key"] = True
                            print(" [-] You have retrieved the boss key!")
                            treasure = []
                            space['treasure'] = []
                            world.dungeon[location]['treasure'] = []
                        elif (split_input[2].lower() == treasure[0][0]):
                            pass
                        else:
                            print(" [*] Not yet implemented.")
                    elif split_input[1].lower() == 'enemy':
                        if split_input[3] == 'weapon':
                            # Current logic will allow you to steal a weapon from a living enemy. 
                            for index, item in enumerate(enemies[int(split_input[2]) - 1].stats['weapons']):
                                try:
                                    if item[0] == split_input[4]:
                                        world.hero.hero_attribs['weapons'] = enemies[int(split_input[2]) - 1].stats['weapons'][index]
                                        print(world.hero.hero_attribs['weapons'])
                                        enemies[int(split_input[2]) - 1].stats['weapons'][index] = []
                                except:
                                    pass
                                    # This is for when the itteration hits an empty sublist. 

                        elif split_input[3] == 'armor':
                            #if split_input[3] in enemies[int(split_input[2]) - 1].stats['armor']:
                                #world.hero.hero_attribs['armor'] = enemies[int(split_input[2]) - 1].stats['armor']
                                #print(world.hero.hero_attribs['armor'])
                            #for index, item in enumerate(enemies[int(split_input[2]) - 1].stats['armor']):
                            if split_input[4] in enemies[int(split_input[2]) - 1].stats['armor']:
                                world.hero.hero_attribs['armor'] = enemies[int(split_input[2]) - 1].stats['armor']
                                print(world.hero.hero_attribs['armor'])
                                enemies[int(split_input[2]) - 1].stats['armor'] = []

                    else:
                        print(" [!] Invalid option.")
                else:
                    continue

            else:
                print("Invalid option submitted.....")
            
            # Enemy actions happen here.
            # check enemy living status
            living_enemies = []
            for num, enemy in enumerate(enemies):
                if enemy.stats['health'] <= 0 :
                    living_enemies.append(False)
                else:
                    living_enemies.append(True)
            if True not in living_enemies:
                enemies_defeated = True
            
            if enemies_defeated == True:
                continue

            # Loop through the enemies present
            for num, enemy in enumerate(enemies):
                if enemy.stats['health'] <= 0 :
                    pass
                else:
                    # roll dice to determine enemy action
                    roll_result = utils.roll_dice()
                    if roll_result[2] > 10:
                        # Move / take a defensive position
                        print(" [-] Enemy {0} has moved or is taking up a defensive position.".format(num+1))
                    else:
                        # Enemy Attack
                        roll_result =  utils.roll_dice()
                        weapons = enemy.stats['weapons']
                        weapon_damage = 0
                        for index,weapon in enumerate([weapons]):
                            try:
                                weapon_damage += weapons[index][1]
                            except:
                                weapon_damage = 0

                        # Need to calculate:
                        #   cumulative attack damage
                        attack_damage = weapon_damage + roll_result[2]
                        #   defensive amount
                        armor = world.hero.hero_attribs['armor']
                        defensive_value = 0
                        defensive_value = armor[1]
                        #   roll for dodge probability of player
                        dodge = False
                        lucky_dodge = utils.roll_dice()
                        if lucky_dodge[2] >= 10:
                            dodge = True
                            print(" [-] You feel this fight in your bones and are determined to win.")
                        #   check for hero dagger or shield perks
                        if ('dagger' in world.hero.hero_attribs['weapons']):
                            if utils.roll_dice()[2] > 8:
                                dodge = True
                                print(" [-] The light weight of your dagger seems to almost make you faster!")
                        if ('shield' in world.hero.hero_attribs['armor']):
                            if utils.roll_dice()[2] > 8:
                                dodge = True
                                print(" [-] You put your shield up and defend yourself. Bracinging yourself for the onslought!")
                        if dodge == True:
                            attack_damage = 0

                        if attack_damage > 0:
                            final_damage = attack_damage - defensive_value
                            if final_damage < 0:
                                final_damage = 0 
                            # subtract the final calculated battle damage from player health.
                            if (world.hero.hero_attribs['health'] - final_damage) > 0:
                                print(" [!] You took {0} damage".format(final_damage))
                                world.hero.hero_attribs['health'] = world.hero.hero_attribs['health'] - final_damage
                                print(" [!] Your health is now {0}".format(world.hero.hero_attribs['health']))
                            else:
                                world.hero.hero_attribs['health'] = 0 
                                utils.youDied()
                                exit(0)
                world.hero.write_hero_object_to_disk()    

    return

def rules():
    print('''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                            Rules
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    1. Being attacked happens automatically while in a room with undefeated monsters.
        a. Your armor '+' value is added to your defense roll.
        ex. greaves = '+5'; A defend dice roll of 3 + the +5  = you defended 8 points of damage.
    2. When attacking you will roll an attack die as a decision when presented decision options.
        a. Your weapon's attack value is added to your attack dice role to equal your attack.
        ex. long sword = +20; An attack role of 6 + the weapon bonus results in a 26 attack
    3. Room movement can occure in a forward and backward movement between rooms.
        a. There is no defined movement inside the room only actions.
    4. If you encounter a weapon or armor you can pick it up and replace what you currently have.
        a. Your charecter is super weak so there is no pouch or bag to store items. 
        b. You're in here to kill monstors not start a scavanger business. 
    5. Enemies that have had their weapons stolen from them can still attack you with their fists.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ''')

    print('''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                            Decisions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    1. 'help' : Get help, this menu
    2. 'move' : 
        a. 'forward' : Move forward into the next room.
        b. 'backward' : Move back into the previous room.
    4. 'chill' or 'do nothing' : Do nothing...
    5. 'take' : Grab or drop a specific item.
        a. 'treasure' : pickup item in current room
            i. ex. take treasure key
        b. 'enemy' : drop item currently held
            i. ex. take enemy 1 weapon short_sword
            ii. ex. take enemy 2 armor gauntets
    6. 'look' : list the items and enemies visible in the room.
    7. 'attack' : ...
        a. attack <enemy number>

    ''')

    return

def display():
    print('''
                ...     ..      ..                            
              x*8888x.:*8888: -"888:                .uef^"    
             X   48888X `8888H  8888              :d88E       
            X8x.  8888X  8888X  !888>       .u    `888E       
            X8888 X8888  88888   "*8%-   ud8888.   888E .z8k  
            '*888!X8888> X8888  xH8>   :888'8888.  888E~?888L 
              `?8 `8888  X888X X888>   d888 '88%"  888E  888E 
              -^  '888"  X888  8888>   8888.+"     888E  888E 
               dx '88~x. !88~  8888>   8888L       888E  888E 
             .8888Xf.888x:!    X888X.: '8888c. .+  888E  888E 
            :""888":~"888"     `888*"   "88888%   m888N= 888> 
                "~'    "~        ""       "YP'     `Y"   888  
                                                        J88"  
                                                        @%    
                                                      :"      
    ''')
    print('''
        ===============================================================
        =          The Worlds most ok'est text based game             =
        ===============================================================
    ''')
    return


if __name__ == "__main__":
    display()
    main()
