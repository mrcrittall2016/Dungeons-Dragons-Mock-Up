# Own game

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
#from datetime import time
import datetime

# Apparently can use signal library to one out of code at any point i.e. if you of time: https://stackoverflow.com/questions/26002497/how-to-run-a-background-timer-in-python
#import signal

# Alternatively, can use Threading to make two things happen in parallel
from threading import Thread


'''
# Initialise pygame
pygame.init()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit(1)
			
		# If a key is pressed instead... (can also use pygame.key.get_pressed() which generates a list of the pressed key)
		if event.type == pygame.KEYDOWN:
			if (event.key == pygame.K_LEFT):
				print "Left key pressed"
			elif (event.key == pygame.K_RIGHT):
				print "Right key pressed"
			elif (event.key == pygame.K_UP):
				print "Up key pressed"
			elif (event.key == pygame.K_DOWN):
				print "Down key pressed"
			elif (event.key == pygame.K_SPACE):
				print "Space bar pressed"
		
# Note that the above seems to work! 

'''
	


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


#Base combat class			
class Combat(object):
	
	#Ideally need to keep track of hero_health throughout game. By setting as class attribute acts as like a global variable. Safer than using actual globals. 
	#Believe this is like a public variable in other programming languages like Java or C#. All instances of this class share this variable and can see it. 
	hero_health = 10
	
	#Private variables that methods of only this instantiation can see.
	def __init__(self):
		
		# Hero stats		
		self.hero_defence = 3 #33% chance of hero taking damage. If you level up in the game, chance of taking damage lessens i.e. becomes randin(1,4) for example. Or if you acquire improved armour.
				
		# Gothon stats
		self.gothon_health = 3
		self.gothon_defence = 2 #50% chance of hitting Gothon i.e. via randint(1,2)
		
		#Gothons to kill
		self.Gothons = 2
			
		# Note: Could include other stats such as initiative that determine whether Gothon or player attacks first
					
		#Also initiate pygame object
		self.pygame = Scene()
	
	def fight(self):
		
		print "Better start shooting that laser gun of yours!"
			
		while True:					
			#Hit return to shoot	
			#action = raw_input(">")			
			#print action
			action = self.pygame.run_pygame()			
			
			if action == 'Space':
				shot = 1 # If gun does hit, this is how many HPs is taken. If the gun can be upgraded, then it will remove more HPs. If number is greater than number generated by defence of Gothon, then automatically hits. Gun is too powerful
				
				# Now compare against dice roll for gothon_defence
				dice_roll = randint(1, self.gothon_defence)	#50% chance of hitting	
				
				#print "Hero dice roll is: %s" % dice_roll		
				#print "Number of Gothons still alive: %s" % self.Gothons					
				
				if shot == dice_roll:
					print "Gothon hit!"
					self.gothon_health = self.gothon_health - shot	
					
					if self.gothon_health > 0:
						print "Gothon health is: %s" % self.gothon_health			
					
					if self.gothon_health <= 0:
						print "You killed a Gothon!"
						self.Gothons -= 1
						
						# Re-set Gothon health bar.
						self.gothon_health = 3
					
						if self.Gothons == 0:
							print "Phew! All the Gothons in this room are Dead...but oh wait there is a locked door ahead!"
							return True
						
						else:
							print "But there are still %s Gothons remaining!... Better keep shooting!" % self.Gothons				
					
				elif shot != dice_roll:
					print "You missed! Watch out, the Gothon is attacking!"					
					
					# Here give Gothon chance to attack
					claw_attack = 2
					
					# Now compare against dice roll for hero_defence
					dice_roll = randint(1, self.hero_defence)
					
					#print "Gothon dice roll is: %s" % dice_roll
					
					if claw_attack == dice_roll:
						print "You've been hit!"
						Combat.hero_health = Combat.hero_health - claw_attack			
									
						if Combat.hero_health <= 0:
							print "Oh no, you died!"
							return False
							
						print "Your health is now: %s" % Combat.hero_health
						
					else:
						print "Luckily the Gothon missed and caused no damage!"
			
			else:
				print "Hit the space bar only to shoot your gun!"





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
	
	def time_delay(self):
		
		#t = 5
		
		#while t:
			
			# divmod takes two (non complex) numbers as arguments and return a pair of numbers consisting of their quotient and remainder.
			# quotient: result of a remainder where the digits after the decimal point are removed
			# the result is the same as (a // b, a % b) i.e. if t = 5, then 5//60 = 0.08 which is equal to 0 as quotient. 5 % 60 = 5
	
			#mins, secs = divmod(t, 60)				
			#print mins, secs				
			#timeformat = '{:02d}:{:02d}'.format(mins, secs)
			#timeformat = '%s:%s' % (mins, secs)
			#print timeformat
			#print t
			#time.sleep(1)				
			#t-=1
		
		for i in range(45):
			time.sleep(1)   #waits 45 seconds
		sys.exit() #stops program after timer runs out, you could also have it print something or keep the user from attempting to answer any longer
		
		
	def enter(self):
		
		print "\nYou manage to sneak past the sleeping guard into the outside corridor.\n"
		print "The corridor is dark, lit only by candlelight. You know to have any hope of escape you must find a weapon to defend yourself."
		print "If only you can find the armory...\n "
		print "Sneak along the corridor to the end doorway, hiding in the shadows to avoid detection. Use the up arrow key to progress forward."
		print "If you are spotted by a guard, use the left or right arrows to dive into the shadows. But don't dwell too long for risk of being caught!"
				
		steps = 0 
		
		progress_message = ["That's it... keep moving", "Easy does it...", "Careful, slowly now", "The guards are watching...keep going"]
					
		t = randint(2,5)			
		key_pressed = self.run_pygame()			
			
		if key_pressed == 'Up':			
			
			
			# Keep time loop running forever	
			while True:
	
				# Time loop
				while t:
		
					print '.'
					time.sleep(1)
					t-=1			
									
				
				print "A guard has appeared! Dive for cover"
				#print_message = False
				# Generate random time delay
				t = randint(2, 5)
				
				key_pressed = self.run_pygame()
				
				if key_pressed == 'Left' or key_pressed == 'Right':
					steps += 1
					print "\n" + progress_message[randint(0, (len(progress_message) - 1))] 
						
					if steps == 5:
						print 'Phew! You made it to the end of the corridor... looks like this could be promising!'
						return 'Armory'
						
					continue
				else:
					print "\nOh no! A guard has caught you\n"
					
					# Begin combat with Gothons. Base class (level 1)
					c = Combat()
					result = c.fight()	
					
					if result:
						return 'Armory'
			
					elif not result:
						return 'death'
					
				break
				
		else:
			print "\nOh no! A guard has caught you\n"
			return 'Death'
		

class Chamber(Scene):
	
	def enter(self):		
		return "Sewer"

class Sewer(Scene):
	
	def enter(self):
		return 'Exit'		

class Armory(Scene):
	
	def enter(self):
		return 'Chamber'


class Death(Scene):
	
	def enter(self):
		print "\nGame Over!\n"
		exit(1)


class Exit(Scene):
	
	def enter(self):
		print 'Game finished!'
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
		
		print "Next scene is: %s" % next_scene
		
		# Now enter infinite loop until program exits at Death or Finished 
		while True:
		
			next_scene = Engine.scenes.get(next_scene)			
			
			next_scene = next_scene.enter() 	
			
			print next_scene
			
			
		
		
		
		
		

# Create scene object of opening scene
scenario = Corridor()

game = Engine(scenario)
game.play()








		
		
		
