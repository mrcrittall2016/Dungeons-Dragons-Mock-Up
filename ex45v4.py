# Own game with combat system and character stats

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


# Base class
class Scene(object):
	
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
		self.weapon = Hero.attacks.get(Hero.hero_weapon)		
		self.defence = Hero.hero_defence + Hero.armour_selection.get(Hero.hero_armour).get('defence') #33% chance of hero taking damage ie through randint(1, self.defence) If you level up in the game, chance of taking damage lessens i.e. becomes randin(1,4) for example. Or if you acquire improved armour.
		self.dexterity = Hero.hero_dexterity - self.weapon.get('dexterity-modifier')
		print "Hero armour should be: %s" % Hero.hero_armour 
		self.agility = Hero.hero_agility - Hero.armour_selection.get(Hero.hero_armour).get('agility-modifier')
		print "Hero agility should be: %s" % self.agility
	
class Guard(Character):
	
	# Default guard stats
	guard_defence = 0	
	
	# Base-level ability to dodge an attack
	guard_agility = 5		
	
	def __init__(self, level):
		
		if level == 1:
			self.level = 1
			self.weapon = Guard.attacks.get('sword')
			#print "Guard weapon is: %s" % self.weapon
			self.dexterity = 5 - self.weapon.get('dexterity-modifier')
			self.health = 3
			self.defence = Guard.guard_defence + Guard.armour_selection.get('chainmail').get('defence') #50% chance of hitting Guard i.e. via randint(1,2)
			self.agility = Guard.guard_agility - Guard.armour_selection.get('chainmail').get('agility-modifier')
			
								
		elif level == 2:
			self.level = 2
			self.weapon = Guard.attacks.get('axe')
			self.dexterity = 6 - self.weapon.get('dexterity-modifier')
			self.health = 4
			self.defence = Guard.guard_defence + Guard.armour_selection.get('plate').get('defence') #50% chance of hitting Guard i.e. via randint(1,2)
			self.agility = Guard.guard_agility - Guard.armour_selection.get('plate').get('agility-modifier')
		

class BigBoy(Character):
	
	def __init__(self):
		
		self.weapon = BigBoy.attacks.get('Two-handed-sword')
		self.dexterity = 8 - self.weapon.get('dexterity-modifier')
		self.health = 6
		self.defence = 1 + BigBoy.armour_selection.get('shiny-new-plate').get('defence') #50% chance of hitting Guard i.e. via randint(1,2)
		self.agility =  7 - BigBoy.armour_selection.get('shiny-new-plate').get('agility-modifier')
		
		
	
	
#Base combat class			
class Combat(object):
	
		
	#Instance variables that methods of only this instantiation can see. Also instantiate/pass different character objects to this depending on stage of game and difficulty
	def __init__(self, hero, enemy, guards):
				
		# Hero stats. Can access instance variables directly, as everything is public in Python. If wanted to be private, then would need a public method to return the instance variables.
		#print hero.weapon.get('damage')
		self.hero_damage = hero.weapon.get('damage')		
		self.hero_defence = hero.defence
		self.hero_dexterity = hero.dexterity
		self.hero_agility = hero.agility				
				
		# Guard stats. Can access instance variables directly, as everything is public in Python. If wanted to be private, then would need a public method to return the instance variables.
		self.guard_damage = enemy.weapon.get('damage')
		self.guard_health_begin = enemy.health		
		self.guard_health = enemy.health
		self.guard_defence = enemy.defence 
		self.guard_dexterity = enemy.dexterity
		self.guard_agility = enemy.agility
		
		#Enemies to kill
		self.Guards = guards		
						
		#Initiate pygame object so as to access run_pygame method
		self.pygame = Scene()
	
	
	def fight(self):
						
		print "\n*** Click the yellow Python to ensure keystroke detection is active ***\n"
		
		print "Get ready!"
		
		print "Guard health is: %d" % self.guard_health				
			
		while True:		
					
			#Run pygame method to detect key strokes
			action = self.pygame.run_pygame()			
			
			if action == 'Space':						
										
				# To hit, compare hero dexterity vs enemy agility
				if self.hero_dexterity < self.guard_agility:					
					
					# What is the difference between the two values?
					#difference = self.guard_agility - self.hero_dexterity	
					print "Hero dexterity is: %d" % self.hero_dexterity
					print "Guard agility is: %d" % self.guard_agility									
					
					dice_roll = randint(self.hero_dexterity, self.guard_agility)#50% chance of hitting if difference is 1
					
					print "Dice roll to hit is: %d" % dice_roll
					
					if dice_roll == self.guard_agility:
						print "That's a hit!"
						
						print "Hero damage is: %d" % self.hero_damage
						print "Guard defence is: %d" % self.guard_defence
						
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
						self.guard_health = self.guard_health - damage_caused
						
						if self.guard_health > 0:
							print "Guard health is: %s" % self.guard_health
							
						elif self.guard_health <= 0:
							print "You killed the Guard!"
							self.Guards -= 1
						
							# Re-set Guard health bar.
							self.guard_health = self.guard_health_begin
					
							if self.Guards == 0:
								print "Phew! You survived this battle!"
								return True
						
							else:
								print "But there are still %s Guards remaining!... Better keep swinging!" % self.Guards	
									
					
					# If you missed...
					elif dice_roll != self.guard_agility:
						print "You missed! Watch out, the Guard is attacking!"	
						
						# Now need to compare guard dexterity against hero agility
						print "Hero agility is: %s" % self.hero_agility
						print "Guard dexterity is: %s" % self.guard_dexterity						
						
						if self.guard_dexterity < self.hero_agility:
						
							# What is the difference between the two values?
							#difference = self.hero_agility - self.guard_dexterity					
					
							dice_roll = randint(self.guard_dexterity, self.hero_agility) #50% chance of hitting if difference is 1
					
							print "Dice roll to hit is: %d" % dice_roll
							
							if dice_roll == self.hero_agility:
								print "You've been hit!"
								
								
								print "Guard damage is: %d" % self.guard_damage
								print "Hero defence is: %d" % self.hero_defence
								
								# Determine damage caused
								damage_caused = self.guard_damage - self.hero_defence
								
								if damage_caused <= 0:
									damage_caused = 1									
								
								Hero.hero_health = Hero.hero_health - damage_caused	
								
								if Hero.hero_health <= 0:
									print "Oh no, you died!"
									return False
						
								print "Your health is now: %s" % Hero.hero_health							
								
							else:
								print "Luckily the Guard missed and caused no damage!"
							
						# Automatically hit if guard is too dextrous with weapon 
						elif self.guard_dexterity >= self.hero_agility:
							print "You've been hit!"	
							
							print "Guard damage is: %d" % self.guard_damage
							print "Hero defence is: %d" % self.hero_defence
							
							# Determine damage caused
							damage_caused = self.guard_damage - self.hero_defence
							
							if damage_caused <= 0:
								damage_caused = 1								
							
							Hero.hero_health = Hero.hero_health - damage_caused	
							
							if Hero.hero_health <= 0:
								print "Oh no, you died!"
								return False
					
							print "Your health is now: %s" % Hero.hero_health				
				
				
				# Automatically hit if hero dexterity is same or equal to Guard's
				elif self.hero_dexterity >= self.guard_agility:
					print "That's a hit!"
					
					if self.guard_defence > self.hero_damage:
						print "You hardly made a scratch on this guy..."
						damage_caused = 1
					else:
						damage_caused = self.hero_damage - self.guard_defence
						
						if damage_caused == 0:
							damage_caused = 1
					
					#OK now subtract damage caused from enemy's HP
					self.guard_health = self.guard_health - damage_caused
					
					if self.guard_health > 0:
						print "Guard health is: %s" % self.guard_health
						
					elif self.guard_health <= 0:
						print "You killed the Guard!"
						self.Guards -= 1
						
						#Re-set health
						self.guard_health = self.guard_health_begin						
				
						if self.Guards == 0:
							print "Phew! You survived this battle!"
							return True
					
						else:
							print "But there are still %s Guards remaining!... Better keep swinging!" % self.Guards						
				
				
			
			else:
				print "Hit the space bar to attack!"





class Cell(Scene):	
	
	def enter(self):
	
		print "\nOur hero awakes in a cold, dark damp dungeon, imprisoned by an evil Wizard against his will."
		print "Through the darkness all he can make out is a long wooden mop pole in a bucket outside the bars of his cell."
		print "Perhaps he can use the pole to fish the keys to his cell from the sleeping guard standing nearby...\n"
		print "Help the hero using the arrow keys of your keyboard to fish the cell keys away."
		print "Press the keypad in the correct order to retrieve the keys to the hero's cell.\nBut beware if the guard awakes, then severe punishment or death awaits...\n" 
		
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
		
		print "\nYou manage to sneak past the sleeping guard into the outside corridor.\n"
		print "The corridor is dark, lit only by candlelight. You know to have any hope of escape you must find a weapon to defend yourself."
		print "If only you can find the armory...\n "
		print "Sneak along the corridor to the end doorway, hiding in the shadows to avoid detection. Use the up arrow key to progress forward."
		print "If you are spotted by a guard, use the left or right arrows to dive into the shadows. But don't dwell too long for risk of being caught!"
				
		steps = 0 
		guards_silenced = 0
		
		#progress_message = ["That's it... keep moving", "Easy does it...", "Careful, slowly now", "The guards are watching...keep going"]
		
		movement_directions = ['Left', 'Right', 'Up', 'Down']
		
		# Randomly generate spawn time		
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
				print "\nOh no! The guard has caught you!\n"
				
				# Begin combat with Guard. Base class (level 1)
				hero = Hero()
				guard = Guard(1)
				
				c = Combat(hero, guard, 1)
				result = c.fight()	
				
				if result:
				
					guards_silenced += 1
					
					if guards_silenced + steps == 3:
						print '\nPhew! You made it to the end of the corridor... looks like this could be promising!\n'
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
		
		print "Oh what's this? You have found a %s and %s armour.\n" % (Hero.hero_weapon, Hero.hero_armour)
			
		print "*** The %s confers an attack bonus of %d to your character, while %s armour provides a defence bonus of %d. Maybe things aren't so bad after all!***\n" % (Hero.hero_weapon, Hero.attacks.get(Hero.hero_weapon).get('damage'), Hero.hero_armour, Hero.armour_selection.get(Hero.hero_armour).get('defence'))
			
		print "Let's get moving!"		
	
	
	def enter(self):
		
		print "So promising in fact that you managed to find the Castle Armoury! Time to acquire some useful stuff so that you can make a decent fight of this!\n"
		print "Seems like everything is stored away in chests though! There are 3 in front of you, which one should you open?\n"
		
		print "Your health is currently: %s" % Hero.hero_health
		
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
		
		print "\nA small glint of candle light shows the way to the room beyond... you follow it with renewed hope that you can escape and learn of your true identity!\n"
		print "But as you enter the next room you know escape is still far beyond your reach. For the this room is the torture chamber!\n"
		print "Poor, dying souls litter the room, tied to despicable contraptions that you do not even recognise. What is more, a host of Guards have seen you... do you stay and fight or create a diversion and run?\n" 
				
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
		
			if result:		
				
				print "\nThat's the majority of the Guards taken care of... but wait!"
				print "Out of the carnage emerges a beast of a man filled with evil and hate..."
				print "Exhausted from your battle with the other guards you fear that this may well be your end... but from somewhere within you find the fortitude and strength to continue"
				print "\n*** Health regenerated ***\n"
				Hero.hero_health = 10
				print "Once more you steel yourself, ready to send this evil back to wherest it came!"
				
				hero = Hero()
				boss = BigBoy() 
				
				c = Combat(hero, boss, 1)
				result = c.fight()	
				
				if result:	
					print "\nAnd down he goes! Good ridance as well! With that, you turn to see in the corner of the room what looks to be a sewer grate. You lift the grate with both hands, before retrieving your weapon and dropping down to the dark depths below...\n"	
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
		return 'Exit'
		
class Exit(Scene):
	
	def enter(self):
		print 'Game finished!'
		exit(1)


class Death(Scene):
	
	def enter(self):
		print "\nGame Over!\n"
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








		
		
		
