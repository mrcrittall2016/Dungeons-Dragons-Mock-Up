'''
	This is the main game file containing the code to be run for each room. Each room inherits from the Scene class, as imported from scene.py
	The combat engine is imported from character.py
'''


from sys import exit
from scene import *
from character import *


# First scene
class Cell(Scene):
	
	def enter(self, screen):						
		
		# First room, so set initial text using the below functions
		if self.font_position(screen, Scene.lines, Scene.current_position, "initial"):
			self.font_write(screen, Scene.lines)				
		
		# Introduction to game
		story = "In the mystical land of Alderan far far away, it is a time of darkness and oppression.\nThe land has been subjected to the will of a dark and evil Wizard whose identity is a mystery to all...\nOnly a force of good and highest purity can purge the evil from this land...\na force that lies within the heart of a young man imprisoned by the evil Wizard.\nCan you help our young hero escape from the evil Wizard's castle and help save the realm from the cruel fate that besets it?"			
		self.print_to_screen(story, screen, "story")
		
		instructions = "*** Press the space-bar to continue ***"
		self.print_to_screen(instructions, screen, "story")		
		
		story = "You awake in a cold, dark damp dungeon. You have no memory of how you got here or why you were imprisoned...only that an evil wizard is somehow responsible. Through the darkness all you can make out is a long wooden mop pole in a bucket outside the bars of your cell. A Guard sits in slumber nearby and you notice a set of keys hangs from his side. Perhaps you can use the pole to fish the keys from the sleeping guard... "		
		self.print_to_screen(story, screen, "story")
		
		instructions = "*** Use the arrow keys on your keyboard to retrieve the keys from the guard. But beware! You must press the keys in the correct order or risk that the guard awakes! ***"
		self.print_to_screen(instructions, screen, "simple")
		
		# Key_order to be pressed to retrieve keys from cell guard. May choose to randomly generate - harder the game mode, the longer the list to guess. 
		key_order = ['left', 'up', 'right', 'down']
		
		correct = 0
		wrong = 0
		
		for key in key_order:
		
			#Call keystroke detection from pygame for game-play
			while True:
				
				key_pressed = self.run_pygame(screen)					
							
				if key_pressed == key:					
					story = "Almost there..."
					self.print_to_screen(story, screen, "simple")				
					correct += 1
					
					if correct == len(key_order):						
						story = "Nice! You successfully retrieved the keys and have opened your cell without the guard noticing!"
						self.print_to_screen(story, screen, "simple")						
						return 'Corridor'
					
					break
			
				else:					 
					story = "Careful, you poked the guard and he has stirred from his slumber!"
					self.print_to_screen(story, screen, "simple")		
					wrong += 1
					
					if wrong == len(key_order):						
						story = "Alas, you have awoken the guard and he shows you no mercy, impaling you with his sword!"						
						self.print_to_screen(story, screen, "simple")
						return 'Death'
		
		

# Next scene
class Corridor(Scene):
	
	def enter(self, screen):				
		
		story = "You manage to sneak past the sleeping guard into the outside corridor. The corridor is dark, lit only by candlelight. You know to have any hope of escape you must find a weapon to defend yourself. If only you can find the castle armory... You start to sneak along the corridor to the end doorway. You know for now you must hide in the shadows to avoid detection and certain death."		
		self.print_to_screen(story, screen, "story")
		
		instructions = "*** Help the hero as he sneaks along the corridor. Use the left or right arrow keys when a guard appears to dive into the shadows! ***"
		self.print_to_screen(instructions, screen, "simple")
		
		steps = 0 
		guards_silenced = 0
			
		movement_directions = ['left', 'right', 'up', 'down']	
	
	
		# Keep time loop running forever	
		while True:				
			
			# Randomly generate time to finish loop	
			t = randint(2,6)
			print "At top of while loop again"
									
		 	while t:
		 		self.press_space()
		 		self.print_to_screen('..sneaking..', screen, "story")
		 		self.press_space()	
				time.sleep(1)
				t-=1						
			
			time.sleep(1.5)
			message = "A guard has appeared! Which direction should you turn?"
			self.print_to_screen(message, screen, "story")		
				
			key_pressed = self.run_pygame(screen)
		
			print "\nKey pressed in Corridor scene\n ", key_pressed
		
			comparison = movement_directions[randint(0, (len(movement_directions) - 1))]
			#print comparison
		
			# Randomly select direction from array.. if matches, then carry on, if not .. battle guard. Basically 25% chance of getting correct
			if key_pressed == 'left': #comparison
				steps += 1
				message = "That was lucky...let's carry on"				
				self.print_to_screen(message, screen, "simple")				
			
				# Get 4 correct guesses or kill/silence 4 guards 
				if steps + guards_silenced == 3:
					message = "Phew! You made it to the end of the corridor...and open the wooden door that awaits there..."
					self.print_to_screen(message, screen, "story")
					return 'Armory'
				
				continue
			
			else:
				message = "Oh no! The guard has caught you! There's no escape without a fight!"
				self.print_to_screen(message, screen, "simple")
			
				# Begin combat with Guard. Base class (level 1)
				hero = Hero()
				guard = Guard(1)
			
				c = Combat(hero, guard, 1, screen)
				result = c.fight()	
			
				# Make sure to re-set combat dialogue array
				Combat.combat_story = []
			
				if result:
			
					guards_silenced += 1
				
					if guards_silenced + steps == 3:
						message = "You make it to the end of the corridor...and open the wooden door that awaits there..."
						self.print_to_screen(message, screen, "simple")
						return 'Armory'
				
					continue
	
				elif not result:
					return 'Death'		
				

class Armory(Scene):	
	
	def equipment(self, screen):
		
		weapons = ['sword', 'axe', 'mace', 'Two-handed-sword']
		armour = ['chainmail', 'plate', 'shiny-new-plate']
		
		# Modify hero class variable with this? so that everytime hero class is instantiated this is kept track of
		Hero.hero_weapon = weapons[randint(0, (len(weapons)-1))]
		Hero.hero_armour = armour[randint(0, (len(armour)-1))]			
		
		message = "Contained within the chest are some very useful items indeed! You have found a %s and %s armour." % (Hero.hero_weapon, Hero.hero_armour)
		self.print_to_screen(message, screen, "simple")
			
		message = "*** The %s confers an attack bonus of %d to your character, while %s armour provides a defence bonus of %d ***" % (Hero.hero_weapon, Hero.attacks.get(Hero.hero_weapon).get('damage'), Hero.hero_armour, Hero.armour_selection.get(Hero.hero_armour).get('defence'))
		self.print_to_screen(message, screen, "simple")		
	
	
	def enter(self, screen):		
			
		story = "Beyond lies a large room, littered with an array of weaponry and armour. Likely this is indeed the Castle Armoury. Your attention is drawn immediately to 3 very conveniently placed chests that lie in the centre of the room. You know their being there is likely all part of some sadistic game orchestrated by the evil wizard who imprisoned you here. However, you can't resist opening one of the chests all the same. Which chest should you open?"
		self.print_to_screen(story, screen, "story")		
		
		while True:				
									
			key_pressed = self.run_pygame(screen)	
			
			if key_pressed == '1' or key_pressed == '2' or key_pressed == '3':				
				
				print "\nKey pressed is: \n", key_pressed
				
				# Cycle the players choice
				chest_number = str(randint(1,3))
		
				# Create random outcomes below i.e. 1 in 3 chance of choosing death chest. Other 2 will return the next room but random assortment of equipment...
		
				if '1' in chest_number:					
					
					self.equipment(screen)	
					return 'Chamber'
			
				elif '2' in chest_number:
			
					self.equipment(screen)			
					return 'Chamber'
			
				elif '3' in chest_number:
					
					message = "Oh no, as you open the chest it explodes in a ball of flames, killing you instantly!"
					self.print_to_screen(message, screen, "simple")
					return 'Death'				
		
			else:				
				message = "Please provide a number between 1 and 3"
				self.print_to_screen(message, screen, "simple")



class Chamber(Scene):
	
	def enter(self, screen):
		
		weapons = ['sword', 'axe', 'mace', 'Two-handed-sword']
		armour = ['chainmail', 'plate', 'shiny-new-plate']
		
		Hero.hero_weapon = weapons[randint(0, (len(weapons)-1))]
		Hero.hero_armour = armour[randint(0, (len(armour)-1))]				
						
		
		story = "A small glint of candle light shows the way to the room beyond... you follow it with renewed hope that you can escape and learn of your true identity! But as you enter the next room you know escape is still far beyond your reach. For this room is the torture chamber! Poor, dying souls litter the room, tied to despicable contraptions that you do not even recognise. What is more, a host of Guards have seen you... do you stay and fight or create a diversion and run?" 
		self.print_to_screen(story, screen, "story")		
		
		
		while True:
			
			key_pressed = self.run_pygame(screen)
			
			if 'fight' in key_pressed:
			
				message = "Like the brave hero you are, you decide to stand and fight. Hopefully this won't get too messy..."				
				self.print_to_screen(message, screen, "simple")					
			
				# Begin combat with Guards, level 2
				hero = Hero()
				guard = Guard(2)
		
				c = Combat(hero, guard, 2, screen)
				result = c.fight()	
			
				# Make sure to re-set combat dialogue array
				Combat.combat_story = []
		
				if result:							
				
					story = "That's the majority of the Guards taken care of... but wait! Out of the carnage emerges a beast of a man filled with such evil and hate that your very soul reals in horror... Exhausted from your battle with the other guards you fear that this may well be your end... but from somewhere within you find the fortitude and strength to continue"
					self.print_to_screen(story, screen, "story")
					
					update = "*** Health regenerated ***"
					self.print_to_screen(update, screen, "simple")
					
					story = "Once more you steel yourself, ready to send this evil back to wherest it came!"	
					self.print_to_screen(story, screen, "story")
				
					Hero.hero_health = 10
				
					hero = Hero()
					boss = BigBoy() 
				
					c = Combat(hero, boss, 1, screen)
					result = c.fight()
				
					# Make sure to re-set combat dialogue array
					Combat.combat_story = []	
				
					if result:	
						story = "And down he goes! Good ridance as well! With that, you turn to see in the corner of the room what looks to be a sewer grate. You lift the grate with both hands, before retrieving your weapon and dropping down to the dark depths below..."
						self.print_to_screen(message, story, "story")					
						return 'Chamber'	
					
					else:
						return 'Death'			
			
				elif not result:
					return 'Death'			 			
			 
			elif 'diversion' in key_pressed: 
				
				self.press_space()
				story = "You grab a torch hanging from the wall nearby and fling it towards the group of Guards who have seen you. They flinch and cower for just enough time to allow you to run towards what looks to be a sewer grate. You attempt to pull up the grate but it is jammed... perhaps you need more strength. Do you carry on trying to pull with one hand or drop your weapon and use all your might?"								
				self.print_to_screen(story, screen, "story")	
				
				while True:			
					
					key_pressed = self.run_pygame(screen)					
			
					while True:
						if 'one' in key_pressed:
							self.press_space()
							story = "The grate just won't budge... and as you try harder and harder you are suddenly impaled by a large spear from one of the Guards behind. You die a slow and agonising death..."
							self.print_to_screen(story, screen, "story")
							return 'Death'
			
						elif 'both' in key_pressed:
							self.press_space()
							story = "You drop your weapon to the ground and grip the grate with both hands. With all your might you free the grate, lifting the heavy piece of metal and dropping into the darkness below. However, in your haste you leave your weapon behind... hopefully you won't need that later!"
							self.print_to_screen(story, screen, "story")							
							return "Sewer"
			
						else:
							message = "That is not a good reaction...please try something else"
							self.print_to_screen(message, screen, "simple")
							break
			
		
			else:
				#print "That is not a good reaction...please try something else\n"
				message = "That is not a good reaction...please try something else"
				self.print_to_screen(message, screen, "simple")
				continue


# Final boss scene
class Sewer(Scene):
	
	def enter(self, screen):
				
		story = "The sewer is dark and rank, you can see barely an inch in front of you. But you know you have to keep moving...All the time you are aware of things moving around your feet... arrrgh rats! As you wade deeper and deeper through the foul stenching waters you become aware of a faint glimmer of light in the distance.. freedom, could it be? You edge closer and closer towards the light and the darkness of the sewer is lifted ever so slightly... but just as you are within touching distance of what is seemingly the end, a large terrifying shriek is let out! In front of you emerges a giant, fearsome beast. Half rat and half man, no doubt a result of the experiments conducted by the evil wizard that imprisoned you in this place! Hope you still have that weapon of yours..."
		self.print_to_screen(story, screen, "story")	
		
		if Hero.hero_weapon == 'fists':
			message = "Well, bare fists will have to do!"
			self.print_to_screen(message, screen, "simple")	
		
		else:
			message = "Die, foul beast from the fiery pits below!"			
			self.print_to_screen(message, screen, "simple")
		
		hero = Hero()
		final_boss = ManRat()
		
		c = Combat(hero, final_boss, 1, screen)
		result = c.fight()
		
		# Make sure to re-set combat dialogue array
		Combat.combat_story = []
		
		if result:	
			message = "The evil ManRat has been vanguished!"	
			self.print_to_screen(message, screen, "simple")
			
		else:
			return 'Death'



# End of the game in most often cases - i.e. Death
class Death(Scene):
	
	def enter(self, screen):
		message = "*** GAME OVER ***"
		self.print_to_screen(message, screen, "story")
		message = "*** Please press the space bar to exit ***"
		self.print_to_screen(message, screen, "simple")
		
		while True:				
									
			key_pressed = self.run_pygame(screen)	
			
			if "space" in key_pressed:
				exit(1)
				
			else:
				message = "*** Please press the space bar to exit ***"
				self.print_to_screen(message, screen, "simple")
				continue

# If you win the game	
class Exit(Scene):
	
	def enter(self, screen):
				
		story = "With relief you reach the light beyond... a circular exit with 4 iron bars across it blocks your way. One of the bars appears to be rusted away, and you push it aside with what strength you have left. You crawl out into the fresh, crisp, cold air onto a marshy river bank. At last you are free! You can see the surrounding land stretches far and wide into the distance and you realise this is just the beginning of your journey. Who are you? What is your true identity? Why did the evil wizard imprison you within his castle? So many questions fill your head... but quick, you should get moving before any of the Wizard's minions try to follow you. With that you move swiftly onwards, ready to embrace what other perils await."
		self.print_to_screen(story, screen, "story")
		
		message = "*** END OF PART 1 ***"
		self.print_to_screen(message, screen, "story")
		
		message = "*** CLICK HERE TO BUY PART 2 NOW! ***"
		self.print_to_screen(message, screen, "simple")
		
		message = "*** Limited time offer! Just $10! ***"
		self.print_to_screen(message, screen, "simple")
				
		while True:				
									
			key_pressed = self.run_pygame(screen)	
			
			if "space" in key_pressed:
				exit(1)
				
			else:
				message = "*** Please press the space bar to exit ***"
				self.print_to_screen(message, screen, "simple")
				continue


# Game Engine
class Engine(object):
	
	# Dictionary of scenes. Do we even need this? Could perhaps just return class from above methods i.e. return Exit()
	scenes = {	
		'Sewer' : Sewer(),
		'Chamber' : Chamber(),
		'Death' : Death(),
		'Armory' : Armory(),
		'Corridor' : Corridor(),
		'Exit' : Exit(),
		'Cell' : Cell()	
	}		
		
	
	# Initialises with first scene object. So Cell() object and width/height of Pygame screen
	def __init__(self, width, height, first_scene):	
		
		self.first_scene = first_scene			
		
		#Also initialise pygame
		pygame.init()
		
		self.width = width
		self.height = height
		
		# Display screen of set dimensions. Other parameters that can be sent to display.set_mode method
		'''
			pygame.FULLSCREEN    create a fullscreen display
			pygame.DOUBLEBUF     recommended for HWSURFACE or OPENGL
			pygame.HWSURFACE     hardware accelerated, only in FULLSCREEN
			pygame.OPENGL        create an OpenGL-renderable display
			pygame.RESIZABLE     display window should be sizeable
			pygame.NOFRAME       display window will have no border or controls
		'''
		self.screen = pygame.display.set_mode((self.width, self.height))
		#self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)			
		

	# Plays scene
	def play(self):	
		
		# So essentially is calling enter method of Cell object for example	
		next_scene = self.first_scene.enter(self.screen)
			
		# Now enter infinite loop until program exits at Death or Finished 
		while True:			
			
			next_scene = Engine.scenes.get(next_scene)	
			#print "Next scene is: %s" % next_scene				
			
			next_scene = next_scene.enter(self.screen) 	
			

		
# Create scene object of opening scene
scenario = Cell()

game = Engine(800, 500, scenario)
game.play()




		
		
		
