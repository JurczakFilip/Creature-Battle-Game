# Services/Dependancies
import random as rand
from alive_progress import alive_bar
import time
# Variables x States
gameState = {
    "isPlaying": True,
    "level": 1,
    "YapTimer": 3
}

User = []

#Functions
def GenDamage(agent):
    damage = ((agent.health/(rand.randint(800,1000)/100))*agent.level)
    return int(damage)

def PointlessBar(sleepTime):
    randomNumberToApperentlyLoad=rand.randint(300,500)
    with alive_bar(randomNumberToApperentlyLoad) as bar:
        for item in range(0,randomNumberToApperentlyLoad):
            bar()
            time.sleep(sleepTime)

def health_bar(current, maximum, width=20):
    ratio = current / maximum
    filled = int(ratio * width)
    empty = width - filled
    return f"[{'+' * filled}{'#' * empty}]"

def agentCard(agent):
    if agent.isCreature:
        print(f"{agent.name} [LVL {agent.level}] {health_bar(agent.health, agent.max_health)} {agent.health}/{agent.max_health}")
    else:
        print(f"{agent.name} (You) [LVL {agent.level}] {health_bar(agent.health, agent.max_health)} {agent.health}/{agent.max_health}")
    return True

#Classes
class CreatureAgent:
    def __init__(self, name, maxhp, level):
        self.name = name
        self.health = maxhp
        self.max_health = maxhp
        self.level = level
        self.isCreature = True
        self.isDodging = False
    
    def take_damage(self, amount):
        if self.isDodging:
            amount = max(1, amount // 2)
            self.isDodging = False
            print(f"{self.name} tried to dodge! Damage reduced to {amount}!")

        if self.health <= amount:
            self.health = 0
            print(f"{self.name} has been Slayed!")
        else:
            self.health -= amount
            print(f"{self.name} took {amount} HP!")

            

    def attack(self, target):
        damage = GenDamage(self)
        target.take_damage(damage)

    
    def isAlive(self):
        return self.health > 0

    def CheckDamage(self):
        print(GenDamage(self))

    def Dodge(self):
        self.isDodging = True
        #print(f"{self.name} Chose to Dodge!") Debug Stuff

    def choose_action(self):
        # 1 = attack, 2 = dodge
        return rand.randint(1, 2)

    def execute_action(self, action, target):
        if action == 1:
            damage = GenDamage(self)
            target.take_damage(damage, attacker=self)
            print(f"{self.name} attacked and dealt {damage} damage!")
        elif action == 2:
            self.Dodge()
            print(f"{self.name} chose to dodge!")

class UserAgent:
    def __init__(self, name):
        self.name = name
        self.max_health = 100
        self.health = self.max_health
        self.level = 1
        self.isCreature = False
        self.isDodging = False
        self.consecutiveDodges = 0


    def take_damage(self, amount, attacker=None):
        reflected = 0

        if self.isDodging:
            reflected = max(1, amount // 2)
            amount = reflected
            self.isDodging = False
            print(f"{self.name} (You) dodged! Damage reduced to {amount}!")

            if attacker:
                attacker.take_damage(reflected)
                print(f"[Counter!] {attacker.name} took {reflected} reflected damage!")

        if self.health <= amount:
            self.health = 0
            print("You have died...")
        else:
            self.health -= amount
            print(f"{self.name} (You) took {amount} HP!")



    def attack(self, target):
        self.consecutiveDodges = 0
        target.take_damage(GenDamage(self))


    def isAlive(self):
        return self.health > 0
    
    def CheckDamage(self):
        print(GenDamage(self))

    def Dodge(self):
        self.isDodging = True
        self.consecutiveDodges += 1
        print(f"{self.name} (You) Chose to Dodge!")

        if self.consecutiveDodges >= 3:
            punishment = max(1, self.health // 2)
            self.health -= punishment
            self.consecutiveDodges = 0
            self.isDodging = False  # punishment breaks dodge
            print(f"\n[DodgeSpam!] punishment! You took {punishment} damage!")


#Main
while gameState["isPlaying"]:
    if gameState["level"] == 1:
        # This level is scripted so you get how to play the game twust
        print(chr(27) + "[2J")
        print("Epic Creature Battle Game")
        print("""                                                                                          
        _____     _        _____             _                  _____     _   _   _        _____               
        |   __|___|_|___   |     |___ ___ ___| |_ _ _ ___ ___   | __  |___| |_| |_| |___   |   __|___ _____ ___ 
        |   __| . | |  _|  |   --|  _| -_| .'|  _| | |  _| -_|  | __ -| .'|  _|  _| | -_|  |  |  | .'|     | -_|
        |_____|  _|_|___|  |_____|_| |___|__,|_| |___|_| |___|  |_____|__,|_| |_| |_|___|  |_____|__,|_|_|_|___|
            |_|                                                                                               
                    
        """)
        print("Welcome, to the epic Creature Battle Game! (Yes i am very creative right!)                                       ", end='\r')
        time.sleep(gameState["YapTimer"])
        print("To start playing you might want to make generate your self a User Agent,                                         ", end='\r')
        time.sleep(gameState["YapTimer"])
        print("todo this all you'll have to do is just make a username for your self which                                      ", end='\r')
        time.sleep(gameState["YapTimer"])
        print("is very simple stuff.                                                                                            ", end='\r')

        def CreateUsername():
            username = str(input("Username: "))
            if not username:
                print("Ummm, Try that again.")
                CreateUsername()
            if len(username) > 12:
                print("Ummm, Try a username under 12 characters this time.")
                CreateUsername()
            else:
                return username
        print(" "*30, end="\r")
        User = UserAgent(CreateUsername())
        print(" "*30, end="\r")

        print("Loading...", end="\r")
        makeItLookLikeSomethingIsLoadingLol = (rand.randint(100,300)/100) # <- 100% does nothing sus i promise. Select it and CTRL+F if u wanna see!
        time.sleep((makeItLookLikeSomethingIsLoadingLol/100))
        print(f"{User.name}, that's an awsome username lets go battle some creatures!")
        time.sleep(3)
        print(chr(27) + "[2J")

        LoadingLevel = (rand.randint(50,100)/100) # was 300 , 500 Change back later! (On a side note i dont think i will tbh)
        print(f"[LOADING] Loading Level[{gameState['level']}]")
        PointlessBar(LoadingLevel/100)
        time.sleep(LoadingLevel/100)
        print(chr(27) + "[2J")

        Snake = CreatureAgent("Snake", 50, 1)
        print("A Wild Snake has appeared!")

        time.sleep(gameState["YapTimer"])

        print("You must kill it to pass this land!")

        agentCard(Snake)

        time.sleep(gameState["YapTimer"])

        agentCard(User)

        time.sleep(.5)  

        print(chr(27) + "[2J")

        agentCard(Snake)
        agentCard(User)

        Rounds = 1
        while Snake.isAlive() and User.isAlive():
            Rounds = Rounds + 1
            snake_action = Snake.choose_action()

            print(f"\n{User.name}'s Turn!")
            print("[CONTROLS] [1] Attack | [2] Dodge")

            while True:
                try:
                    userInput = int(input("> "))
                    if userInput in (1, 2):
                        break
                    print("Try again.")
                except:
                    print("Invalid input.")

            print(" "*10)
            print("==========BATTLE LOG==========")
            if userInput == 1:
                User.attack(Snake)
            elif userInput == 2:
                User.Dodge()

            if Snake.isAlive():
                Snake.execute_action(snake_action, User)
            print("==============================")
            time.sleep(1.5)
            print(" "*10)
            agentCard(Snake)
            agentCard(User)
            print(f"=========Starting Round {Rounds} in 5 seconds=========")
            with alive_bar(5) as bar:
                for item in range(0,5):
                    bar()
                    time.sleep(1)

            print(chr(27) + "[2J")
            print(" "*10)
            agentCard(Snake)
            agentCard(User)
        
        if not User.isAlive():
            print(chr(27) + "[2J")
            print("\n\nYou suck...\nHow do you fail a attack spam level.")
            print("\n\n[EXITING] Auto closing game in 5 seconds.")
            with alive_bar(5) as bar:
                for item in range(0,5):
                    bar()
                    time.sleep(1)
            break
        else:
            print(chr(27) + "[2J")
            print("I Kinda dont have anything else planned so im gonna close this window for you.")
            print("\n\n[EXITING] Auto closing game in 5 seconds.")
            with alive_bar(5) as bar:
                for item in range(0,5):
                    bar()
                    time.sleep(1)
            break
