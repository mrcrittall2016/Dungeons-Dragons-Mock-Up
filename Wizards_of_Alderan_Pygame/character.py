'''
	This file contains the Character and Combat classes. These are responsible for implementation of the game's combat engine.

'''



from scene import *
from random import randint


# Base character class
class Character(object):
	
	#Below are examples of class variables. All derivatives (or children) of this class have access to these.
	
	# Attack attributes accessible to all instances of Character class. Note need to have chance-to-hit stat associated with each weapon
	attacks = {
		'fists' : {'damage' : 1, 'dexterity-modifier' : 1, 'armour-penetration' : 0},
		'sword' : {'damage' : 3, 'dexterity-modifier' : 2, 'armour-penetration' : 1},
		'axe' : {'damage' : 4, 'dexterity-modifier' : 3, 'armour-penetration' : 2},
		'mace' : {'damage' : 5, 'dexterity-modifier' : 4, 'armour-penetration' : 3},
		'Two-handed-sword' : {'damage' : 6, 'dexterity-modifier' : 5, 'armour-penetration' : 4},
		'claw-attack' : {'damage' : 3, 'dexterity-modifier' : 0, 'armour-penetration' : 1}
	}
	
	# Could also have stats for armour as well. Also initiative in sub-classes to determine who attacks first. 
	armour_selection = {
		'leather' : {'defence' : 0, 'agility-modifier' : 0, 'armour-quality' : 2},
		'chainmail' : {'defence' : 1, 'agility-modifier' : 1, 'armour-quality' : 3},
		'plate': {'defence' : 2, 'agility-modifier' : 2, 'armour-quality' : 4},
		'shiny-new-plate' : {'defence' : 3, 'agility-modifier' : 3, 'armour-quality' : 5},	
	}
	
	

# Hero and Guard classes
class Hero(Character):
	
	name = "Hero"
	
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
			
		# What stats does our hero have?		
		self.weapon = Hero.hero_weapon		
		self.damage = Hero.attacks.get(self.weapon).get('damage')
		self.penetration = Hero.attacks.get(self.weapon).get('armour-penetration')		
		self.defence = Hero.hero_defence + Hero.armour_selection.get(Hero.hero_armour).get('defence') #33% chance of hero taking damage ie through randint(1, self.defence) If you level up in the game, chance of taking damage lessens i.e. becomes randin(1,4) for example. Or if you acquire improved armour.
		self.save = Hero.armour_selection.get(Hero.hero_armour).get('armour-quality')
		self.dexterity = Hero.hero_dexterity - Hero.attacks.get(self.weapon).get('dexterity-modifier')		
		self.agility = Hero.hero_agility - Hero.armour_selection.get(Hero.hero_armour).get('agility-modifier')
		
	
class Guard(Character):
	
	# Enemy name
	name = 'Guard'	
	
	# Default guard stats
	guard_defence = 0	
	
	# Base-level ability to dodge an attack
	guard_agility = 5		
	
	def __init__(self, level):		
		
		if level == 1:		
		
			self.health = 3	
			self.weapon = 'sword'			
			self.damage = Guard.attacks.get(self.weapon).get('damage')
			self.penetration = Guard.attacks.get(self.weapon).get('armour-penetration')
			self.dexterity = 5 - Guard.attacks.get(self.weapon).get('dexterity-modifier')			
			self.defence = Guard.guard_defence + Guard.armour_selection.get('chainmail').get('defence') #50% chance of hitting Guard i.e. via randint(1,2)
			self.save = Guard.armour_selection.get('chainmail').get('armour-quality')
			self.agility = Guard.guard_agility - Guard.armour_selection.get('chainmail').get('agility-modifier')
			
								
		elif level == 2:
						
			self.health = 4	
			self.weapon = 'axe'
			#print Guard.attacks.get(self.weapon).get('dexterity-modifier')
			self.damage = Guard.attacks.get(self.weapon).get('damage')
			self.penetration = Guard.attacks.get(self.weapon).get('armour-penetration')
			self.dexterity = 6 - Guard.attacks.get(self.weapon).get('dexterity-modifier')						
			self.defence = Guard.guard_defence + Guard.armour_selection.get('plate').get('defence') #50% chance of hitting Guard i.e. via randint(1,2)
			self.save = Guard.armour_selection.get('plate').get('armour-quality')
			self.agility = Guard.guard_agility - Guard.armour_selection.get('plate').get('agility-modifier')
		

# Do we need instance variables if not passing any arguments to class?
class BigBoy(Character):
	
	# Enemy name
	name = 'BigBoy'	
	
	def __init__(self):
		
		self.health = 6
		self.weapon = 'Two-handed-sword'
		self.damage = BigBoy.attacks.get(self.weapon).get('damage')
		self.penetration = BigBoy.attacks.get(self.weapon).get('armour-penetration')
		self.dexterity = 8 - BigBoy.attacks.get(self.weapon).get('dexterity-modifier')		
		self.defence = 1 + BigBoy.armour_selection.get('shiny-new-plate').get('defence') #50% chance of hitting Guard i.e. via randint(1,2)
		self.save = BigBoy.armour_selection.get('shiny-new-plate').get('armour-quality')
		self.agility =  7 - BigBoy.armour_selection.get('shiny-new-plate').get('agility-modifier')

	
class ManRat(Character):
			
	# Enemy name
	name = 'ManRat'
	
	def __init__(self):
		
		# Claw attack
		self.health = 20
		self.weapon = 'claw-attack'
		self.damage = ManRat.attacks.get(self.weapon).get('damage')	
		self.penetration = ManRat.attacks.get(self.weapon).get('armour-penetration')		
		self.dexterity = 4		
		self.defence = 1
		self.save = 4		
		self.agility = 4


#Base combat class			
class Combat(object):	
		
	
	# Class variable to hold combat story
	combat_story = []
	
	# Health summaries
	hero_health_summary = True
	enemy_health_summary = True
	
	# Instance variables that methods of only this instantiation can see. Also instantiate/pass different character objects to this depending on stage of game and difficulty
	def __init__(self, hero, enemy, guards, screen):
				
		# Hero stats. 
		self.hero = hero					
				
		# Enemy stats. 
		self.enemy = enemy
		self.enemy_health_initial = enemy.health		
		
		#Enemies to kill
		self.Guards = guards		
						
		#Initiate pygame object so as to access run_pygame method
		#self.pygame = Pygame()
		
		# Also create instance of Scene object so as to gain access to print methods
		self.scene = Scene()
		
		# Get screen dimensions for passing to scene print methods
		self.screen = screen
		
	
	# Runs scrolling story of battle
	def combat_dialogue(self):		
		
		index = 0		
		
		# Make sure combat_story list actually has something in it		
		if len(Combat.combat_story) > 0:
				
			# Time loop
			while True:
				
				# This print statement tells the entire history of the combat 	
				#print Combat.combat_story[index]
				
				print "\nAbout to invoke timed scroll method\n"
				self.scene.print_to_screen(Combat.combat_story[index], self.screen, "timed_scroll")
				
				
				#time.sleep(0.5)
				#t-=1	
				index += 1
				#print index
			
				if index == len(Combat.combat_story):
					break
	
	# Chance to not take any damage, even if hit - depends on weapon's armour penetration
	def armour_save(self, defender, attacker):
		
		#print "Character defence is: %d" % defender.save
		#print "Attack weapon is: %s" % attacker.penetration
				
		modifier = defender.save - attacker.penetration
		
		#print "Modifier is: %d" % modifier
		#Combat.combat_story.append("Modifier to damage is: %d" % modifier)
		
		if modifier <= 0:
			# Weapon is too strong
			Combat.combat_story.append("The %s's %s is powerful against %s's armour!" % (attacker.name, attacker.weapon, defender.name))
			return True		
		
		cause_damage = randint(1, modifier)
		#Combat.combat_story.append("Cause damage roll is: %d" % cause_damage)
		
		#print "Cause damage roll is: %d" % cause_damage
		
		if cause_damage == modifier:
			return True		
		
		return False
	
	# Player damage calculator
	def player_damage_calculator(self):
		
		Combat.enemy_health_summary = True
		
		# Ok so you've hit your target, how much damage have you caused? Damage is determined by weapon 'damage' value and armour 'defence' value
		# The greater the defence of the defender the less damage caused
		if self.enemy.defence > self.hero.damage:
			#print "You hardly made a scratch on this guy though..."
			if self.armour_save(self.enemy, self.hero):
				damage_caused = 1
				
			else:
				Combat.combat_story.append("But the %s's armour is too strong!" % self.enemy.name)
				damage_caused = 0
			
		else:									
			if self.armour_save(self.enemy, self.hero):
			
				damage_caused = self.hero.damage - self.enemy.defence
				
				if damage_caused == 0:
					damage_caused = 1
			
			else:
				Combat.combat_story.append("But the %s's armour is too strong!" % self.enemy.name)
				damage_caused = 0
				Combat.combat_story.append("\nThe %s counter-attacks!" % self.enemy.name)				
				self.attack('Enemy')
				
				
		
		
		#OK now subtract damage caused from enemy's HP
		#print "Damage caused is: %d" % damage_caused
		if damage_caused > 0:
			Combat.combat_story.append("Damage caused is: %d" % damage_caused)
		
		self.enemy.health = self.enemy.health - damage_caused
		
		if self.enemy.health > 0:
			#print "%s health is: %s\n" % (self.enemy_name, self.guard_health)
			if Combat.enemy_health_summary and self.Guards != 0:
				Combat.combat_story.append("%s health is: %s\n" % (self.enemy.name, self.enemy.health))	
				Combat.enemy_health_summary = False		
			
		elif self.enemy.health <= 0:
			#print "You killed the %s!" % self.enemy_name
			
			Combat.combat_story.append("You killed the %s!" % self.enemy.name)
			
			self.Guards -= 1
		
			# Re-set Guard health bar.
			self.enemy.health = self.enemy_health_initial
	
			if self.Guards == 0:
				#print "Phew! You survived this battle!"
				#print "Reached end of combat"
				Combat.combat_story.append("Phew! You survived this battle!")					
				return True
		
			else:
				#print "But there are still %s %s remaining!... Better keep swinging!\n" % (self.Guards, self.enemy_name)	
				Combat.combat_story.append("But there are still %s %s remaining!... Better keep swinging your %s!\n" % (self.Guards, self.enemy.name, self.hero.weapon))
				
	
	# Enemy damage calculator
	def enemy_damage_calculator(self):
		
		#Re-set health statement
		Combat.hero_health_summary = True
		
		if self.hero.defence > self.enemy.damage:
			#print "You hardly made a scratch on this guy though..."
			if self.armour_save(self.hero, self.enemy):
				damage_caused = 1
			else:
				Combat.combat_story.append("But the %s's armour is too strong!" % self.hero.name)
				damage_caused = 0
		else:
			
			if self.armour_save(self.hero, self.enemy):
			
				damage_caused = self.enemy.damage - self.hero.defence
			
				if damage_caused == 0:
					damage_caused = 1
			
			else:
				Combat.combat_story.append("But the %s's armour is too strong!" % self.hero.name)
				damage_caused = 0
				# Call attack method here with player attacking first - allow to counter-attack
				# Player has chance to counter-attack
				Combat.combat_story.append("\nThe %s counter-attacks!" % self.hero.name)
				
				self.attack('Hero')
				
				#print "Checking return_value 1: %s" % return_value
					
												
		if damage_caused > 0:
			Combat.combat_story.append("Damage caused is: %d" % damage_caused)
			
		Hero.hero_health = Hero.hero_health - damage_caused	
		
		if Hero.hero_health <= 0:
			#print "Oh no, you died!"
			Combat.combat_story.append("Oh no, you died!\n")		
			return False
		
		# Ensure health summary is only provided once in each round
		if Combat.hero_health_summary and self.Guards != 0:
			#print "Your health is now: %s\n" % Hero.hero_health	
			Combat.combat_story.append("%s health is: %s\n" % (Hero.name, Hero.hero_health))
			Combat.hero_health_summary = False
	
	
	# Keep rolling dice until either player or enemy gets the magic_number to attack first
	def initiative_test(self, winner, loser, winner_tuple, loser_tuple):
		
		magic_number = 10
		
		# Keep rolling dice until get a winner
		while True:
		
			# Both players have 50% chance of striking first
			winner_roll = {winner : randint(*winner_tuple)}
			loser_roll = {loser : randint(*loser_tuple)}
			
			#print "Winning dice roll is: %d" % winner_roll.get(winner)
			#print "Losing dice roll is: %d" % loser_roll.get(loser)
			
			if winner_roll.get(winner) == magic_number:
				#print "returning %s" % winner
				return winner
		
			elif loser_roll.get(loser) == magic_number:
				#print "returning %s" % loser
				return loser
				
			else:
				continue
		
	
	# Method to determine who attacks first
	def who_attacks_first(self):
		
		# How to determine who strikes first? Compare characters' agilities? If same, or different by only 1 then each has 50% chance of who attacks first.
		# If 2, then each has 25% chance of attacking first. 
		#print "Player agility is: %s" % self.hero_agility
		#print "Enemy agility is: %s" % self.guard_agility		
		
		# Highest agiity
		agilities = {self.hero.name : self.hero.agility, self.enemy.name : self.enemy.agility}
		winner = max(agilities, key=agilities.get)
		loser = min(agilities, key=agilities.get)
		
		#print "%s has the highest agility of %d" % (winner, agilities.get(winner))
		#print "%s has the lowest agility of %d" % (loser, agilities.get(loser))
		
		# Magic number to score against
		magic_number = 10				
		
		# If agilities are the same
		if agilities.get(winner) == agilities.get(loser):
			#print "Agilities are the same"
			
			# Use tuples to store odds to unpack in randint function
			winner_tuple = (9, 10)
			loser_tuple = (9, 10)
			
			result = self.initiative_test(winner, loser, winner_tuple, loser_tuple)
			return result
			
		
		else:
			difference = agilities.get(winner) - agilities.get(loser)
			#print "%s wins by %d" % (winner, difference)
			
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
		
		if who_attacks == 'Hero':			
			
			#print "In player attack loop"
			
			#print "Hero dexterity is: %d" % self.hero_dexterity			
			#print "%s agility is: %d" % (self.enemy_name, self.guard_agility)
			
			# To hit, compare hero dexterity vs enemy agility
			if self.hero.dexterity < self.enemy.agility:			
				
				#print "In outer loop 1"	
				#print "Hero dexterity is: %d" % self.hero_dexterity
				#print "%s agility is: %d" % (self.enemy_name, self.guard_agility)									
			
				dice_roll = randint(self.hero.dexterity, self.enemy.agility)
			
				#print "Dice roll to hit is: %d" % dice_roll
			
				if dice_roll == self.enemy.agility:
				
					#print "Inside inner loop 1"
					#print "That's a hit!"
					Combat.combat_story.append("You hit the %s!" % self.enemy.name)						
					#print "Hero damage is: %d" % self.hero_damage
					#print "%s defence is: %d" % (self.enemy_name, self.guard_defence)
				
					# Player hit, so attacks
					if self.player_damage_calculator():	
						#print "Reached end of combat 1"
						return True		
				
				# If you missed...enemy attacks
				elif dice_roll != self.enemy.agility:
					#print "You missed! Watch out, the %s is attacking with a %s!" % (self.enemy_name, self.enemy_weapon)
					Combat.combat_story.append("You missed! Watch out, the %s is attacking with a %s!" % (self.enemy.name, self.enemy.weapon))	
					# Now need to compare guard dexterity against hero agility
					#print "Hero agility is: %s" % self.hero_agility
					#print "Guard dexterity is: %s" % self.guard_dexterity						
				
					if self.enemy.dexterity < self.hero.agility:											
			
						dice_roll = randint(self.enemy.dexterity, self.hero.agility) #50% chance of hitting if difference is 1
			
						#print "Dice roll to hit is: %d" % dice_roll
					
						if dice_roll == self.hero.agility:
						
							#print "Inside inner loop 2"
							#print "You've been hit!"
							Combat.combat_story.append("You've been hit!")						
							#print "Guard damage is: %d" % self.guard_damage
							#print "Hero defence is: %d" % self.hero_defence
						
							return_value = self.enemy_damage_calculator()								
						
							if return_value == False:
								return False													
						
						else:
							#print "Luckily the %s missed and caused no damage!\n" % self.enemy_name
							Combat.combat_story.append("Luckily the %s missed and caused no damage!" % self.enemy.name)
					
					# Automatically hit if guard is too dextrous with weapon 
					elif self.enemy.dexterity >= self.hero.agility:
					
						#print "Inside inner loop 3"
						#print "You've been hit!"							
						Combat.combat_story.append("You've been hit!")	
						#print "%s damage is: %d" % (self.enemy_name, self.guard_damage)
						#print "Hero defence is: %d" % self.hero_defence
					
						return_value = self.enemy_damage_calculator()
					
						if return_value == False:
							return False				
				
			# if hero dexterity is same or equal to Guard's
			elif self.hero.dexterity >= self.enemy.agility:
		
				#print "Inside inner loop 4"
				#print "That's a hit!"		
				Combat.combat_story.append("You hit the %s!" % self.enemy.name)			
							
				if self.player_damage_calculator():
					return True							
		
		# If enemy attacks first
		else:
			
			#print "In enemy attack loop\n"
						
			if self.enemy.dexterity < self.hero.agility:											
				
				# Now need to compare guard dexterity against hero agility
				#print "Hero agility is: %s" % self.hero_agility
				#print "Guard dexterity is: %s" % self.guard_dexterity	
				
				dice_roll = randint(self.enemy.dexterity, self.hero.agility) #50% chance of hitting if difference is 1
	
				#print "Dice roll to hit is: %d" % dice_roll
			
				if dice_roll == self.hero.agility:
				
					#print "Inside inner loop 2"
					#print "You've been hit!"	
					Combat.combat_story.append("You've been hit!")								
					#print "Guard damage is: %d" % self.guard_damage
					#print "Hero defence is: %d" % self.hero_defence
				
					return_value = self.enemy_damage_calculator()								
				
					if return_value == False:						
						return False													
				
				else:
					#print "Luckily the %s missed and caused no damage!\n" % self.enemy_name
					Combat.combat_story.append("Luckily the %s missed and caused no damage!" % self.enemy.name)
					
					# Player has chance to counter-attack
					Combat.combat_story.append("\nThe %s counter-attacks!" % self.hero.name)
					# Recursion. Function calls itself until base case of Guards = 0 is met.
					self.attack('Hero')					
					
			
			# Automatically hit if guard is too dextrous with weapon 
			elif self.enemy.dexterity >= self.hero.agility:
			
				#print "Inside inner loop 3"
				#print "You've been hit!"
				Combat.combat_story.append("You've been hit!")							
				#print "%s damage is: %d" % (self.enemy_name, self.guard_damage)
				#print "Hero defence is: %d" % self.hero_defence
			
				return_value = self.enemy_damage_calculator()
			
				if return_value == False:
					return False
		
	
	# Main method to orchestrate turn-based combat
	def fight(self):
						
		print "\n*** Click the yellow Python to ensure keystroke detection is active ***\n"
		
		print "Get ready!"					
			
		while True:		
			
			#print "Checking combat story: %s" % Combat.combat_story
			
			# Are there still enemies to kill?
			if self.Guards <= 0:
				Combat.combat_story = []
				return True
			
			# Are you already dead?
			if Hero.hero_health <=0:
				Combat.combat_story = []
				return False
			
			message = "*** Hit the space-bar to attack! ***"
			self.scene.print_to_screen(message, self.screen, "story")
			
			#Run pygame method to detect key strokes
			action = self.scene.run_pygame(self.screen)				
			
			if action == 'space':
				
				print "\nSpace has been pressed following 'hit-space bar' message\n"				
						
				# Who attacks first
				who_attacks = self.who_attacks_first()
								
				#print "Return from who_attacks is: %s" % who_attacks
				
				if who_attacks == 'Hero':
									
					Combat.combat_story.append("%s attacks first" % who_attacks)	
					Combat.combat_story.append("%s is attacking with %s" % (who_attacks, self.hero.weapon))				
					value_return = self.attack(who_attacks)					
					
					# Only enters True or False loop when combat is fully resolved			
					if value_return == True:
						# Tell story of fight before returning to scene
						#print "Getting inside value_return loop"
						self.combat_dialogue()
						return True
						
					elif value_return == False:						
						# Tell story of fight before die
						#print "Getting inside value_return loop 2"
						self.combat_dialogue()						
						return False					
				
				else:						
				
					Combat.combat_story.append("%s attacks first" % who_attacks)
					Combat.combat_story.append("%s is attacking with %s" % (who_attacks, self.enemy.weapon))
					value_return = self.attack(who_attacks)
					
					# Only enters True or False loop when combat is fully resolved	
					if value_return == True:
						# Tell story of fight before returning to scene
						#print "Getting inside value_return loop 3"
						self.combat_dialogue()
						return True
						
					elif value_return == False:					
						# Tell story of fight before die
						#print "Getting inside value_return loop 4"
						self.combat_dialogue()						
						return False
					
				# Tell story of fight
				self.combat_dialogue()
		
				# Re-set array
				Combat.combat_story = []
				
			else:
				print "Hit the space bar to attack!\n"
			
