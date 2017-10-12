# Own game with combat system and character stats


# Improvements - "press space to continue" - improve player experience and go at own pace. Or have slow scroll line by line 

# Tidy up code in Combat System. Replace "Guard" with enemy name. Tell player what attack the enemy is going to use on them.

# Currently if hero has better dexterity than guard's agility, enemy never gets chance to hit back. Too easy. Need a who goes first method?

# Initiative test to determine who goes first?

# Ideally don't want to have to keep switching between terminal and Python article. Want to be smooth gameplay.

''' 
Requirements:

	- Use more than one file
	- Use one class per room and give classes a name that fits their purpose
	- Runner (game engine?) will need to know about the rooms - consider having each room return what room/scene is next
	
	Purpose: Teach one how to structure classes that need other classes inside other files. 
	
Basic story/description of game:
	
	"Set in a medieval fantasy world, a young man has been imprisoned by an evil wizard within a castle dungeoun.
	 Our hero has no memory of his name or how he came to be imprisoned. As the player, you must find a way to escape 
	 the castle dungeon and discover your true identity... only then can you help lift the darkness that has shrouded the realm."

	Scenes:
		
		Death - Where the player dies. Have option to re-start from latest save point or quit?
		
		Prison cell - The start of the game. Have description of scene (method called 'describe'?) 
		
		Dungeon corridor - Sneak through the shadows to avoid the guards... if detected you will be killed
		
		Armory - Steal a sword. 
		
		Torture Chamber - Fight your way past a host of guards here. Have some form of combat system.
		
		Sewar - Find a way into caste sewar... rats, fire-torch, some kind of sewar monster as final boss?
		
		Escape - You emerge into daylight next to the Castle moat and swim to freedom. End of Part 1. 
	
	
	Next step:
		Extract all Nouns and Verbs
		
		
		Nouns: Player(Hero), Soldiers/Guards, Death, Cell, Corridor, Armory, Chamber, Sewer, Exit
		
	
	Create Class Hierarchy:
	
		"What is similar to other things?"
			Hero/Player and Soldiers are the same - use to create character profile and implement battle system
			Death, Cell, Corridor, Armory, Chamber, Sewer and Exit are scenes or scenarios. 
		
		"What is basically another word for another thing?"
			All above can be seen as stages or levels or scenarios
			Hero and Soldiers are characters. Initialise with pre-defined stats
	
	Basic Hierarchy:
	
	- Map
		- generate scene
	- Engine
		- Initialises with Map scene object. 
		- play
	- Combat
		- Intialises with instantiation of character classes involved. Composition
		- fight method: Infinite loop with dice rolls etc. 
	- Scene
		- enter (or describe)
		Death
		Cell - want to try and "fish" key from guard using long pole of mop in bucket next to prison cell. Press arrows keys in correct order. If get wrong order then knocked unconscious by guard. Start again. Every time hit correct key, get a message saying "Almost there" If wrong, then message "the guard noticed something...". Three of the latter messages in a row means game-over/death
		Corridor - Same concept as above, but sneaking along corridor. Implement combat system here? Use fists
		Armory - Steal sword from guard. Update attack stats?
		Chamber - Purely combat room
		Sewer - Use up arrow to move through sewer. Randomly generate rat to kill. After certain number of up strokes, generate killer rat boss?
		Exit - Just simple description of exit and game (part 1) end. 
	- Character
		- Just initialise here with load of stats just as attack, defence etc. Hero's health will be attribute or public variable to keep track of health throughout the game
		Hero
		Soldier 
		
	Ideas:
		It would be good to have some sort of key stroke detection like left/right arrow space-bar etc. instead of relying on
		raw_input function... Use module called pygame? See here: https://www.pygame.org/docs/.
		
		See here on moving a snake around a screen: http://www.learningpython.com/2006/03/12/creating-a-game-in-python-using-pygame-part-one/
		See here for detecting which key is pressed: https://stackoverflow.com/questions/25494726/how-to-use-pygame-keydown. Note that 
		pygame.KEYDOWN and pygame.KEYUP detects if a key is physically pressed down or released.
'''


# Try and experiment with pygame for key detection
import pygame
from sys import exit
from random import randint
import time

# Center text in console window: https://stackoverflow.com/questions/33594958/is-it-possible-to-align-a-print-statement-to-the-center-in-python
import os


# Base class
class Scene(object):	
		
	# Method to detect which keys are pressed on the keyboard
	def run_pygame(self):		
		
		while True:			
			for event in pygame.event.get():
			
				if event.type == pygame.QUIT:
					exit(1)	
							
				# If a key is pressed instead... (can also use pygame.key.get_pressed() which generates a list of the pressed key)
				if event.type == pygame.KEYDOWN:
					if (event.key == pygame.K_LEFT):
						return "Left"
					elif (event.key == pygame.K_RIGHT):
						return "Right"
					elif (event.key == pygame.K_UP):
						return "Up"
					elif (event.key == pygame.K_DOWN):
						return "Down"
					elif (event.key == pygame.K_SPACE):
						return "Space"			
	
	# Method to move story on when user presses space-bar
	def story_reader(self, story):
		
		story_index = 0
		
		while True:			
			key_pressed = self.run_pygame()		
			
			if key_pressed == 'Space':
				
				#print "%-45s" % story[story_index]
				print story[story_index]
				story_index += 1
			
			else:
				print "\n*** Please press the space-bar to continue the story ***\n"
					
			# Break this infinite loop if reach end of story array
			if story_index == len(story):
				break
	
	# Method to run story associated with this scene 		
	def enter(self):
		pass


# Base character class
class Character(object):
	
	#Below are examples of class variables
	
	# Attack attributes accessible to all instances of Character class. Note need to have chance-to-hit stat associated with each weapon
	attacks = {
		'fists' : {'damage' : 1, 'dexterity-modifier' : 1},
		'sword' : {'damage' : 3, 'dexterity-modifier' : 2},
		'axe' : {'damage' : 4, 'dexterity-modifier' : 3},
		'mace' : {'damage' : 5, 'dexterity-modifier' : 4},
		'Two-handed-sword' : {'damage' : 6, 'dexterity-modifier' : 5},
		'claw-attack' : {'damage' : 3, 'dexterity-modifier' : 0}
	}
	
	# Could also have stats for armour as well. Also initiative in sub-classes to determine who attacks first. 
	armour_selection = {
		'leather' : {'defence' : 0, 'agility-modifier' : 0 },
		'chainmail' : {'defence' : 1, 'agility-modifier' : 1 },
		'plate': {'defence' : 2, 'agility-modifier' : 2 },
		'shiny-new-plate' : {'defence' : 3, 'agility-modifier' : 3 },	
	}
	
	

# Hero and Guard classes
class Hero(Character):
	
	# Default stats
	hero_defence = 1	
	hero_health = 10
	
	# Dexterity: How well you can wield your weapon to bring about a hit on your opponent
	hero_dexterity = 6
	
	# Agility: How well you can evade an incoming attack
	hero_agility = 5
	
	# Default weapon and armour
	hero_weapon = 'fists'
	hero_armour = 'leather'	
	
	# Instance variables set on instantiation of this class
	def __init__(self):		
			
		# What weapon does our hero have?		
		self.weapon = Hero.hero_weapon	
		print "Hero weapon should be: %s" % Hero.hero_weapon 
		self.damage = Hero.attacks.get(self.weapon).get('damage')
		print "Hero damage should be: %s" % self.damage 
		self.defence = Hero.hero_defence + Hero.armour_selection.get(Hero.hero_armour).get('defence') #33% chance of hero taking damage ie through randint(1, self.defence) If you level up in the game, chance of taking damage lessens i.e. becomes randin(1,4) for example. Or if you acquire improved armour.
		self.dexterity = Hero.hero_dexterity - Hero.attacks.get(self.weapon).get('dexterity-modifier')
		print "Hero armour should be: %s" % Hero.hero_armour 
		self.agility = Hero.hero_agility - Hero.armour_selection.get(Hero.hero_armour).get('agility-modifier')
		print "Hero agility should be: %s" % self.agility
	
class Guard(Character):
	
	# Enemy name
	enemy_name = 'Guard'	
	
	# Default guard stats
	guard_defence = 0	
	
	# Base-level ability to dodge an attack
	guard_agility = 5		
	
	def __init__(self, level):		
		
		if level == 1:		
		
			self.health = 3	
			self.weapon = 'sword'			
			self.damage = Guard.attacks.get(self.weapon).get('damage')
			self.dexterity = 5 - Guard.attacks.get(self.weapon).get('dexterity-modfifier')			
			self.defence = Guard.guard_defence + Guard.armour_selection.get('chainmail').get('defence') #50% chance of hitting Guard i.e. via randint(1,2)
			self.agility = Guard.guard_agility - Guard.armour_selection.get('chainmail').get('agility-modifier')
			
								
		elif level == 2:
						
			self.health = 4	
			self.weapon = 'axe'
			print Guard.attacks.get(self.weapon).get('dexterity-modifier')
			self.damage = Guard.attacks.get(self.weapon).get('damage')
			self.dexterity = 6 - Guard.attacks.get(self.weapon).get('dexterity-modifier')						
			self.defence = Guard.guard_defence + Guard.armour_selection.get('plate').get('defence') #50% chance of hitting Guard i.e. via randint(1,2)
			self.agility = Guard.guard_agility - Guard.armour_selection.get('plate').get('agility-modifier')
		

# Do we need instance variables if not passing any arguments to class?
class BigBoy(Character):
	
	# Enemy name
	enemy_name = 'BigBoy'	
	
	def __init__(self):
		
		self.health = 6
		self.weapon = 'Two-handed-sword'
		self.damage = BigBoy.attacks.get(self.weapon).get('damage')
		self.dexterity = 8 - BigBoy.attacks.get(self.weapon).get('dexterity-modifier')		
		self.defence = 1 + BigBoy.armour_selection.get('shiny-new-plate').get('defence') #50% chance of hitting Guard i.e. via randint(1,2)
		self.agility =  7 - BigBoy.armour_selection.get('shiny-new-plate').get('agility-modifier')

	
class ManRat(Character):
			
	# Enemy name
	enemy_name = 'ManRat'
	
	def __init__(self):
		
		# Claw attack
		self.health = 20
		self.weapon = 'claw-attack'
		self.damage = ManRat.attacks.get(self.weapon).get('damage')			
		self.dexterity = 4		
		self.defence = 1
		self.agility = 4


#Base combat class			
class Combat(object):	
		
	
	# Class variable to hold combat story
	combat_story = []
	
	# Instance variables that methods of only this instantiation can see. Also instantiate/pass different character objects to this depending on stage of game and difficulty
	def __init__(self, hero, enemy, guards):
				
		# Hero stats. Can access instance variables directly, as everything is public in Python. If wanted to be private, then would need a public method to return the instance variables.
		self.hero_weapon = hero.weapon
		self.hero_damage = hero.damage	
		self.hero_defence = hero.defence
		self.hero_dexterity = hero.dexterity
		self.hero_agility = hero.agility				
				
		# Enemy stats. Can access instance variables directly, as everything is public in Python. If wanted to be private, then would need a public method to return the instance variables.
		self.enemy_name = enemy.enemy_name
		self.enemy_weapon = enemy.weapon
		self.guard_damage = enemy.damage
		self.guard_health_begin = enemy.health		
		self.guard_health = enemy.health
		self.guard_defence = enemy.defence 
		self.guard_dexterity = enemy.dexterity
		self.guard_agility = enemy.agility
		
		#Enemies to kill
		self.Guards = guards		
						
		#Initiate pygame object so as to access run_pygame method
		self.pygame = Scene()
	
	
	def combat_dialogue(self):		
		
		index = 0		
		
		# Time loop
		while True:
							
			print Combat.combat_story[index]
			time.sleep(0.5)
			#t-=1	
			index += 1
			#print index
			
			if index == len(Combat.combat_story):
				break
	
	# Player damage calculator
	def player_damage_calculator(self):
		
		# Ok so you've hit your target, how much damage have you caused? Damage is determined by weapon 'damage' value and armour 'defence' value
		# The greater the defence of the defender the less damage caused
		if self.guard_defence > self.hero_damage:
			#print "You hardly made a scratch on this guy though..."
			damage_caused = 1
		else:
			damage_caused = self.hero_damage - self.guard_defence
			
			if damage_caused == 0:
				damage_caused = 1
		
		#OK now subtract damage caused from enemy's HP
		print "Damage caused is: %d" % damage_caused
		
		Combat.combat_story.append("Damage caused is: %d" % damage_caused)
		
		self.guard_health = self.guard_health - damage_caused
		
		if self.guard_health > 0:
			print "%s health is: %s\n" % (self.enemy_name, self.guard_health)
			
			Combat.combat_story.append("%s health is: %s\n" % (self.enemy_name, self.guard_health))			
			
		elif self.guard_health <= 0:
			print "You killed the %s!" % self.enemy_name
			
			Combat.combat_story.append("You killed the %s!" % self.enemy_name)
			
			self.Guards -= 1
		
			# Re-set Guard health bar.
			self.guard_health = self.guard_health_begin
	
			if self.Guards == 0:
				print "Phew! You survived this battle!"
				
				Combat.combat_story.append("Phew! You survived this battle!")
				
				return True
		
			else:
				print "But there are still %s %s remaining!... Better keep swinging!\n" % (self.Guards, self.enemy_name)	
				Combat.combat_story.append("But there are still %s %s remaining!... Better keep swinging your %s!\n" % (self.Guards, self.enemy_name, self.hero_weapon))
				
	
	# Enemy damage calculator
	def enemy_damage_calculator(self):
		
		if self.hero_defence > self.guard_damage:
			#print "You hardly made a scratch on this guy though..."
			damage_caused = 0
		else:
			damage_caused = self.guard_damage - self.hero_defence
			
			if damage_caused == 0:
				damage_caused = 1								
		
		Hero.hero_health = Hero.hero_health - damage_caused	
		
		if Hero.hero_health <= 0:
			print "Oh no, you died!"
			Combat.combat_story.append("Oh no, you died!\n")				
			
			return False

		print "Your health is now: %s\n" % Hero.hero_health	
		Combat.combat_story.append("Your health is now: %s\n" % Hero.hero_health)	
	
	
	# Keep rolling dice until either player or enemy gets the magic_number to attack first
	def initiative_test(self, winner, loser, winner_tuple, loser_tuple):
		
		magic_number = 10
		
		# Keep rolling dice until get a winner
		while True:
		
			# Both players have 50% chance of striking first
			winner_roll = {winner : randint(*winner_tuple)}
			loser_roll = {loser : randint(*loser_tuple)}
			
			print "Winning dice roll is: %d" % winner_roll.get(winner)
			print "Losing dice roll is: %d" % loser_roll.get(loser)
			
			if winner_roll.get(winner) == magic_number:
				print "returning %s" % winner
				return winner
		
			elif loser_roll.get(loser) == magic_number:
				print "returning %s" % loser
				return loser
				
			else:
				continue
		
	
	# Method to determine who attacks first
	def who_attacks_first(self):
		
		# How to determine who strikes first? Compare characters' agilities? If same, or different by only 1 then each has 50% chance of who attacks first.
		# If 2, then each has 25% chance of attacking first. 
		print "Player agility is: %s" % self.hero_agility
		print "Enemy agility is: %s" % self.guard_agility		
		
		# Highest agiity
		agilities = {'Player' : self.hero_agility, 'Enemy' : self.guard_agility}
		winner = max(agilities, key=agilities.get)
		loser = min(agilities, key=agilities.get)
		
		print "%s has the highest agility of %d" % (winner, agilities.get(winner))
		print "%s has the lowest agility of %d" % (loser, agilities.get(loser))
		
		# Magic number to score against
		magic_number = 10				
		
		# If agilities are the same
		if agilities.get(winner) == agilities.get(loser):
			print "Agilities are the same"
			
			# Use tuples to store odds to unpack in randint function
			winner_tuple = (9, 10)
			loser_tuple = (9, 10)
			
			result = self.initiative_test(winner, loser, winner_tuple, loser_tuple)
			return result
			
		
		else:
			difference = agilities.get(winner) - agilities.get(loser)
			print "%s wins by %d" % (winner, difference)
			
			# 50% chance to strike first for winner, 33% for loser
			if difference == 1:
				
				# Use tuples to store odds to unpack in randint function
				winner_tuple = (9, 10)
				loser_tuple = (8, 10)
			
				result = self.initiative_test(winner, loser, winner_tuple, loser_tuple)
				return result				
			
			# 50% for winner, 25% for loser
			elif difference == 2:
				
				# Use tuples to store odds
				winner_tuple = (9, 10)
				loser_tuple = (7, 10)
			
				result = self.initiative_test(winner, loser, winner_tuple, loser_tuple)
				return result				
			
			
			# 50% for winner, 10% for loser
			elif difference >= 3:
				
				# Use tuples to store odds to unpack in randint function
				winner_tuple = (9, 10)
				loser_tuple = (1, 10)
			
				result = self.initiative_test(winner, loser, winner_tuple, loser_tuple)
				return result				
			
	# Turn sequence changes depending on who attacked first
	def attack(self, who_attacks):
		
		print "In attack method"
		
		if who_attacks == 'Player':			
			
			print "In player attack loop"
			
			print "Hero dexterity is: %d" % self.hero_dexterity			
			print "%s agility is: %d" % (self.enemy_name, self.guard_agility)
			
			# To hit, compare hero dexterity vs enemy agility
			if self.hero_dexterity < self.guard_agility:			
				
				print "In outer loop 1"	
				print "Hero dexterity is: %d" % self.hero_dexterity
				print "%s agility is: %d" % (self.enemy_name, self.guard_agility)									
			
				dice_roll = randint(self.hero_dexterity, self.guard_agility)
			
				print "Dice roll to hit is: %d" % dice_roll
			
				if dice_roll == self.guard_agility:
				
					print "Inside inner loop 1"
					print "That's a hit!"
					Combat.combat_story.append("You hit the %s!" % self.enemy_name)						
					print "Hero damage is: %d" % self.hero_damage
					print "%s defence is: %d" % (self.enemy_name, self.guard_defence)
				
					# Player hit, so attacks
					if self.player_damage_calculator():	
						return True		
				
				# If you missed...enemy attacks
				elif dice_roll != self.guard_agility:
					print "You missed! Watch out, the %s is attacking with a %s!" % (self.enemy_name, self.enemy_weapon)
					Combat.combat_story.append("You missed! Watch out, the %s is attacking with a %s!" % (self.enemy_name, self.enemy_weapon))	
					# Now need to compare guard dexterity against hero agility
					print "Hero agility is: %s" % self.hero_agility
					print "Guard dexterity is: %s" % self.guard_dexterity						
				
					if self.guard_dexterity < self.hero_agility:											
			
						dice_roll = randint(self.guard_dexterity, self.hero_agility) #50% chance of hitting if difference is 1
			
						print "Dice roll to hit is: %d" % dice_roll
					
						if dice_roll == self.hero_agility:
						
							print "Inside inner loop 2"
							print "You've been hit!"
							Combat.combat_story.append("You've been hit!")						
							print "Guard damage is: %d" % self.guard_damage
							print "Hero defence is: %d" % self.hero_defence
						
							return_value = self.enemy_damage_calculator()								
						
							if return_value == False:
								return False													
						
						else:
							print "Luckily the %s missed and caused no damage!\n" % self.enemy_name
							Combat.combat_story.append("Luckily the %s missed and caused no damage!\n" % self.enemy_name)
					
					# Automatically hit if guard is too dextrous with weapon 
					elif self.guard_dexterity >= self.hero_agility:
					
						print "Inside inner loop 3"
						print "You've been hit!"							
						Combat.combat_story.append("You've been hit!")	
						print "%s damage is: %d" % (self.enemy_name, self.guard_damage)
						print "Hero defence is: %d" % self.hero_defence
					
						return_value = self.enemy_damage_calculator()
					
						if return_value == False:
							return False				
				
			# if hero dexterity is same or equal to Guard's
			elif self.hero_dexterity >= self.guard_agility:
		
				print "Inside inner loop 4"
				print "That's a hit!"		
				Combat.combat_story.append("You hit the %s!" % self.enemy_name)			
							
				if self.player_damage_calculator():
					return True							
		
		# If enemy attacks first
		else:
			
			print "In enemy attack loop\n"
						
			if self.guard_dexterity < self.hero_agility:											
				
				# Now need to compare guard dexterity against hero agility
				print "Hero agility is: %s" % self.hero_agility
				print "Guard dexterity is: %s" % self.guard_dexterity	
				
				dice_roll = randint(self.guard_dexterity, self.hero_agility) #50% chance of hitting if difference is 1
	
				print "Dice roll to hit is: %d" % dice_roll
			
				if dice_roll == self.hero_agility:
				
					print "Inside inner loop 2"
					print "You've been hit!"	
					Combat.combat_story.append("You've been hit!")								
					print "Guard damage is: %d" % self.guard_damage
					print "Hero defence is: %d" % self.hero_defence
				
					return_value = self.enemy_damage_calculator()								
				
					if return_value == False:
						return False													
				
				else:
					print "Luckily the %s missed and caused no damage!\n" % self.enemy_name
					Combat.combat_story.append("Luckily the %s missed and caused no damage!\n" % self.enemy_name)
			
			# Automatically hit if guard is too dextrous with weapon 
			elif self.guard_dexterity >= self.hero_agility:
			
				print "Inside inner loop 3"
				print "You've been hit!"
				Combat.combat_story.append("You've been hit!")							
				print "%s damage is: %d" % (self.enemy_name, self.guard_damage)
				print "Hero defence is: %d" % self.hero_defence
			
				return_value = self.enemy_damage_calculator()
			
				if return_value == False:
					return False
		
	
	# Main method to orchestrate turn-based combat
	def fight(self):
						
		print "\n*** Click the yellow Python to ensure keystroke detection is active ***\n"
		
		print "Get ready!"			
			
		while True:		
			
			print "Hit the space-bar to attack!"
				
			#Run pygame method to detect key strokes
			action = self.pygame.run_pygame()	
			
			print "At beginning"		
			
			if action == 'Space':
				
				print "In first loop"				
						
				# Who attacks first
				who_attacks = self.who_attacks_first()
				
				print "Return from who_attacks is: %s" % who_attacks
				
				if who_attacks == 'Player':
									
					Combat.combat_story.append("%s attacks first" % who_attacks)	
					Combat.combat_story.append("%s is attacking with %s" % (who_attacks, self.hero_weapon))				
					value_return = self.attack(who_attacks)					
										
					if value_return == True:
						return True
					elif value_return == False:
						
						# Tell story of fight before die
						self.combat_dialogue()
						
						return False					
				
				else:						
				
					Combat.combat_story.append("%s attacks first" % who_attacks)
					Combat.combat_story.append("%s is attacking with %s" % (who_attacks, self.enemy_weapon))
					value_return = self.attack(who_attacks)
					
					if value_return == True:
						return True
					elif value_return == False:
					
						# Tell story of fight before die
						self.combat_dialogue()
						
						return False
					
				# Tell story of fight
				self.combat_dialogue()
		
				# Re-set array
				Combat.combat_story = []
				
			else:
				print "Hit the space bar to attack!"
			
			


class Cell(Scene):	
	
	def enter(self):
		
		
		# Array of strings to print
		story = [
			"\nYou awake in a cold, dark damp dungeon. You have no memory of how you got here or why you were imprisoned...only that an evil wizard is somehow responsible.",	
			"Through the darkness all you can make out is a long wooden mop pole in a bucket outside the bars of your cell.",
			"A Guard sits in slumber nearby and you notice a set of keys hangs from his side.",
			"Perhaps you can use the pole to fish the keys from the sleeping guard...",
			"\n*** Use the arrow keys on your keyboard to retrieve the keys from the guard. But beware! You must press the keys in the correct order or risk that the guard awakes! ***\n"
		]
		
		self.story_reader(story)			
		
		# Key_order to be pressed to retrieve keys from cell guard. May choose to randomly generate - harder the game mode, the longer the list to guess. 
		key_order = ['Left', 'Up', 'Right', 'Down']
		
		correct = 0
		wrong = 0
		
		for key in key_order:
		
			#Call keystroke detection from pygame for game-play
			while True:
				key_pressed = self.run_pygame()
				#key_pressed = pygame.key.get_pressed()				
							
				if key_pressed == key:
					print "\nAlmost there...\n"
					correct += 1
					
					if correct == len(key_order):
						print "\nNice! You successfully retrieved the keys and have opened your cell without the guard noticing!\n"
						return 'Corridor'
					
					break
			
				else:
					print "\nCareful, you poked the guard and he has stirred from his slumber!\n" 
					wrong += 1
					
					if wrong == len(key_order):
						print "\nAlas, you have awoken the guard and he shows you no mercy, impaling you with his sword!\n"
						return 'Death'

class Corridor(Scene):
	
	
	def enter(self):		
		
		story = [
			"You manage to sneak past the sleeping guard into the outside corridor.",
			"The corridor is dark, lit only by candlelight. You know to have any hope of escape you must find a weapon to defend yourself.",
			"If only you can find the castle armory...",
			"You start to sneak along the corridor to the end doorway. You know for now you must hide in the shadows to avoid detection and certain death.",
			"\n*** Help the hero as he sneaks along the corridor. Use the left or right arrow keys when a guard appears to dive into the shadows! ***\n"		
		]		
		
		
		self.story_reader(story)	
		
		steps = 0 
		guards_silenced = 0
		
		#progress_message = ["That's it... keep moving", "Easy does it...", "Careful, slowly now", "The guards are watching...keep going"]
		
		movement_directions = ['Left', 'Right', 'Up', 'Down']
		
		# Randomly generate time to finish loop	
		t = randint(2,5)		
			
		# Keep time loop running forever	
		while True:

			# Time loop
			while t:
				
				print '.'
				time.sleep(1)
				t-=1								
			
			print "A guard has appeared! Which direction should you turn?"
			#print_message = False
			# Generate random time delay
			t = randint(2, 5)
			
			key_pressed = self.run_pygame()
			comparison = movement_directions[randint(0, (len(movement_directions) - 1))]
			print comparison
			
			# Randomly select direction from array.. if matches, then carry on, if not .. battle guard. Basically 25% chance of getting correct
			if key_pressed == comparison:
				steps += 1
				print "\nThat was lucky.. let's carry on"
				
				# Get 4 correct guesses or kill/silence 4 guards 
				if steps + guards_silenced == 3:
					print 'Phew! You made it to the end of the corridor... looks like this could be promising!'
					return 'Armory'
					
				continue
				
			else:
				print "\nOh no! The guard has caught you! There's no escape without a fight!\n"
				
				# Begin combat with Guard. Base class (level 1)
				hero = Hero()
				guard = Guard(1)
				
				c = Combat(hero, guard, 1)
				result = c.fight()	
				
				# Make sure to re-set combat dialogue array
				Combat.combat_story = []
				
				if result:
				
					guards_silenced += 1
					
					if guards_silenced + steps == 3:
						print '\nYou make it to the end of the corridor...and open the wooden door that awaits there...\n'
						return 'Armory'
					
					continue
		
				elif not result:
					return 'Death'
					
class Armory(Scene):
	
	
	def equipment(self):
		
		weapons = ['sword', 'axe', 'mace', 'Two-handed-sword']
		armour = ['chainmail', 'plate', 'shiny-new-plate']
		
		# Modify hero class variable with this? so that everytime hero class is instantiated this is kept track of
		Hero.hero_weapon = weapons[randint(0, (len(weapons)-1))]
		Hero.hero_armour = armour[randint(0, (len(armour)-1))]			
		
		print "Contained within the chest are some very useful items indeed! You have found a %s and %s armour.\n" % (Hero.hero_weapon, Hero.hero_armour)
			
		print "*** The %s confers an attack bonus of %d to your character, while %s armour provides a defence bonus of %d. ***\n" % (Hero.hero_weapon, Hero.attacks.get(Hero.hero_weapon).get('damage'), Hero.hero_armour, Hero.armour_selection.get(Hero.hero_armour).get('defence'))
			
		#print "Let's get moving!"		
	
	
	def enter(self):
		
		
		
		print "Your health is currently: %s" % Hero.hero_health
		
		
		story = [
			 "Beyond lies a large room, littered with an array of weaponry and armour. Likely this is indeed the Castle Armoury.",
			 "Your attention is drawn immediately to 3 very conveniently placed chests that lie in the centre of the room.",
			 "You know their being there is likely all part of some sadistic game orchestrated by the evil wizard who imprisoned you here.",
			 "However, you can't resist opening one of the chests all the same.\n",
			 "Which chest should you open?\n"	
		]
		
		
		self.story_reader(story)
		
		chest_number = raw_input("> ")		
		
		# Cycle the players choice
		chest_number = str(randint(1,3))
		
		# Create random outcomes below i.e. 1 in 3 chance of choosing death chest. Other 2 will return the next room but random assortment of equipment...
		
		if '1' in chest_number:
			
			self.equipment()			
			
			return 'Chamber'
			
		elif '2' in chest_number:
			
			self.equipment()
			
			return 'Chamber'
			
		elif '3' in chest_number:
			print "\nOh no, as you open the chest it explodes in a ball of flames, killing you instantly!"
			return 'Death'				
		
		else:
			print "Please provide a number between 1 and 3"
		
		

class Chamber(Scene):
	
	def enter(self):		
		
				
		story = [
			"A small glint of candle light shows the way to the room beyond... you follow it with renewed hope that you can escape and learn of your true identity!",
			"But as you enter the next room you know escape is still far beyond your reach. For this room is the torture chamber!",
			"Poor, dying souls litter the room, tied to despicable contraptions that you do not even recognise. What is more, a host of Guards have seen you... do you stay and fight or create a diversion and run?\n" 
		]
		
		self.story_reader(story)
			
		action = raw_input("> ")
		
		if 'fight' in action:
			
			print "Like the brave hero you are, you decide to stand and fight. Hopefully this won't get too messy...\n"
			
			print Hero.hero_weapon
			print Hero.hero_armour				
			
			# Begin combat with Guards, level 2
			hero = Hero()
			guard = Guard(2)
		
			c = Combat(hero, guard, 4)
			result = c.fight()	
			
			# Make sure to re-set combat dialogue array
			Combat.combat_story = []
		
			if result:		
							
				
				story = [
					"\nThat's the majority of the Guards taken care of... but wait!",
					"Out of the carnage emerges a beast of a man filled with such evil and hate that your very soul reals in horror...",
					"Exhausted from your battle with the other guards you fear that this may well be your end... but from somewhere within you find the fortitude and strength to continue",
					"\n*** Health regenerated ***\n",				
					"Once more you steel yourself, ready to send this evil back to wherest it came!"
				]
				
				self.story_reader(story)
				
				Hero.hero_health = 10
				
				hero = Hero()
				boss = BigBoy() 
				
				c = Combat(hero, boss, 1)
				result = c.fight()
				
				# Make sure to re-set combat dialogue array
				Combat.combat_story = []	
				
				if result:	
					story = ["\nAnd down he goes! Good ridance as well! With that, you turn to see in the corner of the room what looks to be a sewer grate. You lift the grate with both hands, before retrieving your weapon and dropping down to the dark depths below...\n"]
					self.story_reader(story)					
					return 'Sewer'	
					
				else:
					return 'Death'			
			
			elif not result:
				return 'Death'			 			
			 
		elif 'diversion' in action:
			
			print "\nYou grab a torch hanging from the wall nearby and fling it towards the group of Guards who have seen you. They flinch and cower for just enough time to allow you to run towards what looks to be a sewer grate."
			print "You attempt to pull up the grate but it is jammed... perhaps you need more strength. Do you carry on trying to pull with one hand or drop your weapon and use all your might?\n"
			
			while True:
			
				action = raw_input("> ")
			
				while True:
					if 'one' in action:
						print "The grate just won't budge... and as you try harder and harder you are suddenly impaled by a large spear from one of the Guards behind. You die a slow and agonising death...\n"
						return 'Death'
			
					elif 'both' in action:
						print "You drop your weapon to the ground and grip the grate with both hands. With all your might you free the grate, lifting the heavy piece of metal and dropping into the darkness below."
						print "However, in your haste you leave your weapon behind... hopefully you won't need that later!"
				
						return "Sewer"
			
					else:
						print "That is not a good reaction...please try something else"
						break
			
		
		else:
			print "That is not a good reaction...please try something else"
			return self.enter()		
		
		

class Sewer(Scene):
	
	def enter(self):
				
		story = [
			"\nThe sewer is dark and rank, you can see barely an inch in front of you. But you know you have to keep moving...",
			"All the time you are aware of things moving around your feet... arrrgh rats! As you wade deeper and deeper through the foul stenching waters you become aware of a faint glimmer of light in the distance.. freedom, could it be?",
			"You edge closer and closer towards the light and the darkness of the sewer is lifted ever so slightly... but just as you are within touching distance of what is seemingly the end, a large terrifying shriek is let out!",
			"In front of you emerges a giant, fearsome beast. Half rat and half man, no doubt a result of the experiments conducted by the evil wizard that imprisoned you in this place!",
			"Hope you still have that weapon of yours...\n"
		]
		
		self.story_reader(story)
		
		if Hero.hero_weapon == 'fists':
			print "Well, bare fists will have to do!"
		
		else:
			print "Die, foul beast from the fiery pits below!"
		
		hero = Hero()
		final_boss = ManRat()
		
		c = Combat(hero, final_boss, 1)
		result = c.fight()
		
		# Make sure to re-set combat dialogue array
		Combat.combat_story = []
		
		if result:	
			print "\nThe evil ManRat has been vanguished!"	
			return 'Exit'	
			
		else:
			return 'Death'	
				
		
class Exit(Scene):
	
	def enter(self):
				
		story = [
			 "With relief you reach the light beyond... a circular exit with 4 iron bars across it blocks your way. One of the bars appears to be rusted away, and you push it aside with what strength you have left.",
			 "You crawl out into the fresh, crisp, cold air onto a marshy river bank. At last you are free! You can see the surrounding land stretches far and wide into the distance and you realise this is just the beginning of your journey.",
			 "Who are you? What is your true identity? Why did the evil wizard imprison you within his castle? So many questions fill your head... but quick, you should get moving before any of the Wizard's minions try to follow you.",
			 "With that you move swiftly onwards, ready to embrace what other perils await.",
			 "\n*** END OF PART 1 *** \n"		
		]
		
		self.story_reader(story)
		
		print "*** CLICK HERE TO BUY PART 2 NOW! ***\n"
		print "*** Limited time offer! $9.99 ***\n"
				
		exit(1)


class Death(Scene):
	
	def enter(self):
		print "\n*** Game Over! ***\n"
		exit(1)


# Game Engine
class Engine(object):
	
	# Dictionary of scenes. Public. Do we even need this? Could perhaps just return class from above methods i.e. return Exit()
	scenes = {	
		'Sewer' : Sewer(),
		'Chamber' : Chamber(),
		'Death' : Death(),
		'Armory' : Armory(),
		'Corridor' : Corridor(),
		'Exit' : Exit(),
		'Cell' : Cell()	
	}	
	
	# Initialises with first scene object
	def __init__(self, first_scene):		
		self.first_scene = first_scene	
		
		#Also initialise pygame
		pygame.init()

	# Plays scene
	def play(self):	
		
		#width = os.get_terminal_size().columns. Need to find a way to get width of terminal. Actually pretty complicated
		
		# Introduction. Ideally need to know dimensions of terminal before using center method
		print"\n"
		print "******".center(80, '*')
		print"\n"
		print "WIZARDS\n".center(80, ' ')
		print "OF\n".center(80, ' ')
		print "ALDERAN\n".center(80, ' ')
		print "PART 1 - ESCAPE FROM CASTLE BLACKMORE".center(80, ' ')
		print"\n"
		print "*******".center(80, '*')
			
			
		next_scene = self.first_scene.enter()		
	
		#print "Next scene is: %s" % next_scene
	
		# Now enter infinite loop until program exits at Death or Finished 
		while True:
						
			next_scene = Engine.scenes.get(next_scene)			
		
			next_scene = next_scene.enter() 	
		
			print next_scene
			


# Create scene object of opening scene
scenario = Armory()

game = Engine(scenario)
game.play()








		
		
		
