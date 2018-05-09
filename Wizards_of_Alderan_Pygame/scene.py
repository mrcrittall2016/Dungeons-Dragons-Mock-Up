'''			
	Documentation:
	
		Scene class methods:
			
			def enter(self, screen)
				
				Every room of the game is accessed via the "enter" method. When the outcome of the room is resolved, i.e. death or progression to the next room, either 'Death' or 'Room name' is returned.
				This is used to retrieve the reference to the class associated with the next room (from a dictionary) i.e. Chamber(). In turn, a new instance of this class is created. The "enter" method is called on this instance to run the code and hence game play associated with this room.
				This process continues (as per the While True loop) until exit(1) is reached either within the "enter" method of the Death class or the Exit class.			
				Note that the enter method takes "screen" as a parameter. This is the display surface object returned from "pygame.display.set_mode" This is required by other methods to determine height and width parameters so as to calculate where to position text on the screen. 
			
			def run_pygame(self, screen):
				
				This method enables users to interact with the pygame window using the keyboard. Keys are divided into two lists. There are "action_keys", whereby the identity of the key is returned immediately from this method to determine the in-game action.
				The other list is termed "letters", whereby if a user hits any of these keys their descriptor is continually appended to the "word" list. When the user hits the "enter" key, this word list is joined to form a "printed_word" string. The latter string variable is passed to the "print_to_screen" method which displays the word on the pygame window. 
				The printed_word is also returned to determine further in-game actions.
				
			def press_space(self):
				
				This method mimics, using the pynput module, the pressing and depressing of the spacebar by a user.
			
			
			def print_to_screen(self, string, screen, mode):
				
				This method prints a string to the screen display. There are 3 modes of printing, being "story", where lines only get printed to the screen when the user presses the space-bar, "simple", where the line is instantly printed to the screen regardless of length 
				and "timed_scroll" which prints content to the screen with a defined time delay between each. 
				
			def content_builder(self, story, screen):	
				
				This method breaks up a story string into a series of lines (or dictionaries) that fit the width of the screen.
				A dictionary "template" is used to construct each dictionary which is in turn appended to the list "next_lines".
				First the "story" string is split based on space to form a new list called "word_array". This list is iterated over and each word appended to another list termed "story_array".
				If the length of this "story_array" (once joined to become a string again) becomes longer than the width of the screen, then the last word is popped from this list and the list joined as a string and added to the template as "template[string]".
				This template is then added to the "next_lines" list as a complete line or dictionary. The story_array is then reset to empty and the popped word added to it to signal the start of the next new line. 
				This process continues until the end of the word_array or "story" for that section is reached. 
				This list of dictionaries (or lines) for the current section is returned to be further manipulated by the "print_type" method.
				
				Further details on this method:
				This method takes a long string in the form of "story" and splits it on space to provide a list of words stored in "word_array".
				The word_array is then parsed and each word added to another list termed "story_array". If the length of this list (or array) exceeds that of the width of the Pygame window
				then the array is re-joined to form a string which is stored in the dictionary line template ("template"). In turn, this is appended to the "next_lines" list.
				The story array is then emptied awaiting formation of the next line. 
				Note that lines are also determined/created based on the full-stop character.
				Once all lines objects/dictionaries have been created and appended to the next_lines list, the property 'section' for the first of these lines is set to True so as to provide the neccessary spacing between story sections.
				This list of dictionaries (or lines) is then returned and ultimately passed to the "process_new_lines" method.
				
			def print_type(self, next_lines, screen, method):
				
				This method manipulates the list of lines for that section in different ways depending on the mode specified. For example, if "story" mode is specified
				then the newly created list of line dictionaries (from the content_builder method) is parsed using a while loop, only exiting if the value of index exceeds the length of the lines list.
				Another while loop is nested within this outer loop, continually (for as long as "inner" is set to True) listening for what key the user presses on their keyboard. 
				If 'space' is pressed, then a line dictionary is appended to the class variable Scene.lines. Through the method "position_and_write" this newly appended line is printed (or blit) to the screen.
				In contrast, if the user hits any other key other than 'space' a single-line statment of ""*** Please press the space-bar to continue the story ***" is first passed to the method "content_builder" which builds the required line object or dictionary.
				This in turn is printed to the screen using the method "simple_print". The variable "missed" is set to True following this, which enables on the next iteration the subsequent following line's 'section' property to be set to True. This enables it to be spaced apart. 
				
				"Simple" mode does not wait for the user to press any key and instead appends all lines from the "next_lines" list immediately to the Scene.lines global variable and prints them to the screen again through use of the "position_and_write" method.
				
				The "timed_scroll" mode mimics the user pressing the space-bar of the keyboard, appending and printing a new line to the screen after a specified time-delay. This helps to create a sense of suspense within the gameplay
				
			
			def def position_and_write(self, screen, lines, current_position):
				
				This method takes the current set of lines and determines if they will all fit on the pygame screen based on the current_position global variable which tracks the last known y-coordinate of the furthest positioned line. This is tested with a parameter of "initial" being passed to the "font_position" method.
				If "font_position" returns True then the method "font_write" ultimately blits the text to the screen. If the method returns False, then font_postion is recalled in this case with the parameter "re_position".
				This ensures that all lines are shifted up to create the neccessary space at he base of the screen. Once returned True, font_write is again called to enable printing to the screen.	
			
			def font_position(self, screen, lines, current_position)
				
				This method takes the screen object (set during initialisation of the Engine object), the current list of line objects (usually Scene.lines) and the current_positon (y-coord) of the furtherst down-shifted line object. Initally this is Scene.current_position, but often changes to Scene.lines[len(Scene.lines) - 1]
				First, the screen background colour is set and filled to white. This has to be done to re-set the canvas prior to positioning or writing any text
				In order to center text, the screen object is used to calculate the width and hence center point of the screen
				The method then loops through each line object (also referred to as a dictionary), sets the fontsize based on line[index]['fontsize'] and renders the font based on the string provided as line[index]['string']
				If the line has not been previously positioned and thus has no y-coordinates, line[index]['positioned'] will be set to False. If this is the case then font_position will calculate y-coordinates and determine where the line should be positioned in the window.
				If the 'section' property of the line is set to True, then extra spacing (40px) will be created to space the line further away from the previously placed line.
				Depending on the the value of the 'type' property, the text associated with the line will be spaced out differently i.e. if set to 'header' the line will be further spaced out than if say 'type' is set to 'prose'.
				y-coordinates for header are defined as: posy = current_position + (index*15) + (index*36)
				y-coordinates for prose are defined as: posy = current_position + (marker*15) + (marker*10)
				In both case, posx and posy (in pixels) are used to calculate a position reference object via text.get_rect(center=(posx, posy)) which is assigned to:  lines[index]['position']
				Only once this position object has been assigned as well as the y-coord (posy) in pixels has been assigned to line[index]['y-coord'] is line[index]['positioned'] set to True.
				If this line is found to be the last line object in the Scene.lines list, then the y-coord of this line is remembered and assigned to the global (class) variable Scene.current_position. 
				The number of positioned lines set to True is monitored with the variable line_count. Once this is equivalent to the length of the Scene.lines array (i.e. all line y-coordinates have been calculated) then the method is free to return True.
				
				Of important note, all calculated line y-coordinates are passed to the method "text_too_far" for testing against the height of the screen window. If this method returns False, then that line will not fit on the screen and all preceding lines will need to be re-positioned to make the neccessary room (see re_position method). 
			
			def text_too_far(self, text_pos, lines, index, screen_height)
				
				This method takes the calculated y-coordinate (text_pos) for a given line (and its index) and tests this value against the screen height as follows:
				text_pos + lines[index]['fontsize'] >= screen_height
				If found to exceed the screen_height, the entire Scene.lines class variable is parsed and the y-coordinates of all lines reduced by 100px (arbritarily assigned). 
				Note that this action is only performed for lines which already possess a y-coordinate. The line which exceeds the window height is popped off into a "missing_list" and the Scene.current_position value re-set to the last line with an assigned y-coordinate.
				In turn, this "missing_list" is parsed and y-coordinates calculated for the "popped" line dictionaries. Once done, these popped lines are re-appended to the Scene.lines global and the Scene.current_position re-set to the y-coordinate of the last member of this list.
				Note if all lines have to be re-positioned in this way then the method returns True. Returning True in turn causes the method "font_position" to return False. 
				If lines do not have to be re-positioned then "text_too_far" returns False.
			
			def re_position(self, screen)
			
				If the method "font_position" returns False as a result of 'text_too_far" returning True, then the method re_position is ultimately called. 
				This takes the re-calculated y-coordinates (or posy values) from "text_too_far" and converts them back into an object that can be referenced by Pygame for text positioning. 
				This is a much simplified version of font_position, and does not discriminate based on 'type' of line. 
				Instead the method only looks at the re-calculated y-coords from "text_too_far" and creates a new position for the text using:
				text.get_rect(center=(posx, posy))
				Once done, the line's 'positioned' property is re-set to True and the line_count variable incremented.
				When the number of lines re-positioned matches that of the length of the Scene.lines only then does the method return True. 
				
			
			def font_write(self, screen, lines, posy)
				
				Once either the "font_position" or "re_position" methods have returned True, font_write is called to "print" or rather blit the text to the Pygame window.
				Put simply, this method iterates through all lines in the Scene.lines class variable. If the line possesses a y-coordinate of greater than 0, the line is blitted to the screen as follows:
				if lines[index]['y-coord'] > 0:	
					screen.blit(text, lines[index]['position'])	
				
				Note that lines[index]['position'] refers to the position object calculated in either font_position or re_position.			 	
			
				
'''


# Try and experiment with pygame for key detection
import pygame
if not pygame.font: print 'Warning, fonts disabled'
import time

# To install pynput using pip: https://stackoverflow.com/questions/44919679/pynput-installation-failing-in-python-2-7
from pynput.keyboard import Key, Controller
keyboard = Controller()
					

# Base or Parent class
class Scene(object):	
	
	# Class variable for keeping updated on where text is on pygame window
	current_position = 0
	
	# Class variable for determining amount of space between sections
	section_divider = 30			
	
	# Class variable for story to pass to font-render
	lines = [
		{'string' : "*", 'fontsize' : 36, 'type' : 'header', 'positioned' : False},
		{'string' : "WIZARDS", 'fontsize' : 36, 'type' : 'header', 'positioned' : False},
		{'string' : "OF", 'fontsize' : 36, 'type' : 'header', 'positioned' : False},
		{'string' : "ALDERAN", 'fontsize' : 36, 'type' : 'header', 'positioned' : False},
		{'string' : "PART 1 - ESCAPE FROM CASTLE BLACKMORE", 'fontsize' : 20, 'type' : 'header', 'positioned' : False},		
		{'string' : "*", 'fontsize' : 36, 'type' : 'header', 'positioned' : False}			
	]		
	
	# Method for building list of dictionaries for each room's story. Constructs separate strings from parent story string based on width of screen and then stores as key-value pair of dictionary based on pre-existing template
	def content_builder(self, story, screen):		
				
		template = {'fontsize' : 20, 'type' : 'prose', 'positioned' : False}
				
		next_lines = []
						
		# Build Dictionary - Determine length of strings based on screen width		
		myFont = pygame.font.Font("ostrich-sans/OstrichSans-Black.otf", template['fontsize'])	
		padding = 50 # Provide padding for Pygame window 		
		screen_width = pygame.Surface(screen.get_size()).get_width() - padding
		
		story_array = []
		word_array = story.split() # Take long string provided as argument and create a list from it (splitting on space)		
		
		
		# Note that appending a dictionary to a list is not as simple as one might think: https://stackoverflow.com/questions/5244810/python-appending-a-dictionary-to-a-list-i-see-a-pointer-like-behavior. Actually behaves like a pointer, changes to template['string'] affect all dictionaries within the list...
		for index, word in enumerate(word_array, 0): 
			
			# Append each word to story_array but also remove the words from the word_array
			story_array.append(word)			
			
			# If come across full-stop or *, want to actually split string on this. This is a way of ensuring a new line starts after each full-stop
			if '.' in ' '.join(story_array):
								
				# Split string at first occurrence of character
				x = ' '.join(story_array).split(".", 1)				
				
				# Analyse other fragment of string and fill in missing characters accordingly
				if '..' in x[1]:														
					template['string'] = x[0] + '.'+  x[1]
					
				
				elif x[1] == '':					
					template['string'] = x[0] + '.'
					
				else:
					template['string'] = x[0]
															
				next_lines.append(template.copy())
				
				# Empty list again
				story_array = []		
												
									
			# If text width gets longer than screen width...pop off last word, then create dictionary entry and then carry on
			elif myFont.size(' '.join(story_array))[0] >= screen_width:				
												
				# First pop off last entry so shorter than screen_width (in theory)
				popped_word = story_array.pop(len(story_array)-1)
												
				# Now insert new dictionary entry
				template['string'] = ' '.join(story_array)																
				next_lines.append(template.copy())
				
				# Empty list and append with popped word
				story_array = []
				story_array.append(popped_word)
			
			# If have reached end of list, create final dictionary entry. Note, added function to split lines based on new-line
			elif len(word_array) - 1 == index:									
				template['string'] = ' '.join(story_array)				
				next_lines.append(template.copy())
				
		# Add new scene marker
		next_lines[0]['section'] = True
		
		return next_lines
	
	
	# Calculate line positions and blit to Pygame screen. Re-position all lines if next line does not fit
	def position_and_write(self, screen, lines, current_position):
		
		# Check position and write 
		if self.font_position(screen, lines, current_position, "initial"):						
			self.font_write(screen, lines)						
			
	
		# Else if self.font_position returns False, remove all new lines added, re-position old text and re-calculate
		else:	
			# If False is returned from font_position above, want to re-position text but do not want to re-calculate posy with index... write another function called re-position for now
			# Once have re-positioned existing text, want to re-append next_lines and go through as normal
			if self.font_position(screen, lines, current_position, "re_position"):																
				self.font_write(screen, lines)
	
		
	# Method to process new story lines - includes appending new lines to current class (global) variable of lines, assessing position of all lines on the Pygame screen and re-positioning if necessary. 
	def print_type(self, next_lines, screen, method):		
		
		# Maybe within this method have different modes i.e. story mode (using the for/while loops and one line appearing at a time)
		# Then another mode which just prints simply to the screen with space above and below the line (simple_print)
		if method == "story":		
		
			index = 0		
		
			# This logic gate allows space to be added to line immediately following "Please press space bar to continue"
			missed = False		
		
			while index < len(next_lines):		
			
				inner = True					
			
				while inner:			
					
					#print "\nInside inner while loop\n"
					
					key_pressed = self.run_pygame(screen)	
				
					if key_pressed == 'space':						
						
						#print "SPACE pressed"
																				
						# If user did not press Space bar...
						if missed == True:						
							next_lines[index]['section'] = True
							missed = False
						
						#print "\nCurrent index is: \n", index
						
						Scene.lines.append(next_lines[index])
						#print "\nLine to print is: \n", Scene.lines[len(Scene.lines)-1]			
						
											
						# Calculate line position and blit to screen
						self.position_and_write(screen, Scene.lines, Scene.current_position)
											
						index += 1
						#print "\nIndex check is: \n", index
						#print "\nLength of next_lines is: ", len(next_lines)
											
														
						inner = False		
				
				
					else:					
					
						statement = "*** Please press the space-bar to continue the story ***"
						new_line = self.content_builder(statement, screen)									
						self.print_type(new_line, screen, "simple")				
						missed = True															
						inner = False
			
					
		
		elif method == "simple":		
			
			# Append new statement
			for line in next_lines: Scene.lines.append(line)			
			
			# Calculate line position and blit to screen
			self.position_and_write(screen, Scene.lines, Scene.current_position)
		
		
		elif method == "timed_scroll":								
			
			#print "\nInside timed_scroll method\n"
			
			index = 0
			
			#print "\nNext lines is currently: \n", next_lines	
			
			self.press_space()					
			
			while True:			
				
				self.press_space()	
				
				#print "\nInside inner while loop\n"
				
				key_pressed = self.run_pygame(screen)			
				
				
				if key_pressed == 'space':						
					
					print "SPACE pressed"
				
					self.press_space()		
					
					Scene.lines.append(next_lines[index])
					self.position_and_write(screen, Scene.lines, Scene.current_position)
					time.sleep(0.75)
				
					index += 1			
		
					if index == len(next_lines):
						break		
		
				
	# Method to check if text position has gone beyond the height of the user window. If it has, text y-coordinates is re-adjusted
	def text_too_far(self, text_pos, lines, index, screen_height):
				
		# Need to figure out how many lines to re-position... should be only those with y-coords already set
		number_of_lines_for_reposition = 0
		
		# text_pos represents the y-coord of the furthest positioned line. If this exceeds the window height then we need to re-position everything
		if text_pos + lines[index]['fontsize'] >= screen_height:
						
			# Deduct appropriate value from all y-coord positions
			for mark, line in enumerate(lines, 0):
				
				#print "\nChecking line to re-position: \n", lines[mark]
				
				# Perhaps if y-coord has not been assigned to line, discount this line. Deduct values from existing y-coord lines then send back to font_position method? 
				if 'y-coord' in line:
					
					#print "Line prior to deduction is: %s" % lines[mark]['y-coord']
					lines[mark]['y-coord'] = lines[mark]['y-coord'] - 100
										
					# Need to also re-set all line positioned flags to False again so re-positioned when sent to re_position method
					lines[mark]['positioned'] = False
					
					# Mark this line for re-positioning
					number_of_lines_for_reposition += 1
				
				# Else for those lines that have not yet been assigned y-coords
				else:
					
					#print "\nFull Scenes list is prior to popping\n", lines
					#print "\nLine to currently pop off is: \n", lines[mark]
					
					missing_list = []				
					missing = lines.pop(mark)								
					missing_list.append(missing)					
					
			
			# Get last index position
			point = len(lines)-1
			# Once all lines without y-coords have been assigned to missing_list, re-set y-coord to last known value. Mop up any lines without y-coords that have somehow been missed by scrolling backwards though lines list
			while point > 0:				
				#print "Current line in while loop for assessment is:", lines[point]
				if 'y-coord' in lines[point]:
					Scene.current_position = lines[point]['y-coord']
					break
				else:
					missing = lines.pop(point)								
					missing_list.append(missing)
					point -= 1				
			
			#print "\nMissing list is now: \n", missing_list
			
			# Calculate new y-coords for missing lines						
			for index_missed, missed in enumerate(missing_list, 1): 						
				
				#print "\nCurrent index is: \n", index_missed
				#print"\nLine to calculate new co-ords for is: \n", missed
				#print "\nCurrent y-coord is: \n", Scene.current_position
				
				missed['y-coord'] = Scene.current_position + (index_missed*15) + (index_missed*15) # So when index_missed = 1, missed['y-coord'] = 15 + 15 i.e. 30
				if 'section' in missing_list[0] and missing_list[0]['section'] == True: missed['y-coord'] += 40	# If the first line of the missing_list has a new section, tag adjust all line spacings by the same amount						
				
				#print "\nNew y-coords are: \n", missed
				
				lines.append(missed)	
			
			# Update y-coord again
			Scene.current_position = lines[len(lines)-1]['y-coord']							
												
			return True			
				
		else:
			return False
		
						
	# Method for actually printing (blitting) text to the Pygame screen. Note how lines is an array of dictionaries. Hence index
	# refers to which line or dictionary we are referring to, and fontsize, string and position are keys.
	# (0, 0, 0) refers to the color of the font in rgba, in this case black.			
	def font_write(self, screen, lines):
		
		#print "\nWriting now...\n"
		
		for index, line in enumerate(lines, 0):
			text = pygame.font.Font("ostrich-sans/OstrichSans-Black.otf", lines[index]['fontsize']).render(lines[index]['string'], 1, (0, 0, 0))
			
			#print "Line to print after y coords calculated: ", Scene.lines
								
			if lines[index]['y-coord'] > 0:	
				screen.blit(text, lines[index]['position'])			
		
		pygame.display.flip()
	
	
	# Method to figure out where on the screen the lines from Screen.lines should go... once all lines are positioned the
	# method will return True after which "font_write" is called. 
	def font_position(self, screen, lines, current_position, position_method):
						
		# Set background colour and fill screen with this colour. This needs to be set before positioning or writing any font every time (i.e. the screen has to be set every time).		
		white = [255, 255, 255]
		screen.fill(white)			
	
		# Get horizontal centre of Pygame screen
		screen_width = pygame.Surface(screen.get_size()).get_width()		
		posx = screen_width/2	
	
		#Height of pygame window
		window_height = screen.get_height()	
	
		# Set line_count. Only increment if line has been positioned and [index]['positioned'] set to True
		line_count = 0			
	
		# Text-position marker
		marker = 0				
		
		if position_method == "initial":
			
			# Add separator to lasty coord to create separation between text
			current_position = current_position + Scene.section_divider				
						
			if pygame.font:
						
				# https://stackoverflow.com/questions/32590131/pygame-blitting-text-with-an-escape-character-or-newline
				# Obtain text coordinates first to assess position in window.. then adjust if necessary. 	
									
				# Parse through each of line of text (dictionary) in story lines passed for that particular room				
				for index, line in enumerate(lines, 0):					
					if lines[index]['string'] == "*":								
						lines[index]['string'] = lines[index]['string'] * screen_width									
								
					# Provide absolute path to desired font type and render		
					text = pygame.font.Font("ostrich-sans/OstrichSans-Black.otf", lines[index]['fontsize']).render(lines[index]['string'], 1, (0, 0, 0))
								
					# If lines are not already positioned from previous calls to this function, position them here
					if lines[index]['positioned'] == False:				
					
						# If line contains new_section flag, then push current y-coord on by set value to create space
						if 'section' in line and lines[index]['section']:						
							# Update current position
							current_position = current_position + 40				
					
						if lines[index]['type'] == "header":	
				
							#print "\nIn header section\n"
							posy = current_position + (index*15) + (index*36)					
										
							lines[index]['position'] = text.get_rect(center=(posx, posy))
					
							# Keep track of real y-coord so that can remove earlier lines as scroll window up i.e. if y-coord becomes a negative number or is equal to 0
							lines[index]['y-coord'] = posy
					
							# Mark this line as positioned
							lines[index]['positioned'] = True				
					
							line_count += 1					
					
							# Update ycoord to be last line of text if reached end of list.
							if index == len(lines) - 1:							
								Scene.current_position = posy													
						
			
						elif lines[index]['type'] == "prose":																	
						
							posy = current_position + (marker*15) + (marker*10)									
					
							# Check that text_position will not move the line further than the height of the user window. If ok, then can assign value to line
							if self.text_too_far(posy, lines, index, window_height):							
								return False						
																	
							lines[index]['position'] = text.get_rect(center=(posx, posy))
							lines[index]['y-coord'] = posy
							lines[index]['positioned'] = True																			
					
							# Increment line counts only if text has not gone too far							
							line_count += 1												
					
							# Update ycoord to be last line of text
							if index == len(lines) - 1:
								Scene.current_position = posy							
								
					
						#print "\nText add is: %s for iteration %s\n" % (text_pos, index)
						marker += 1
						
					# Else if lines are set to True then must be already positioned, so increment total_line_count accordingly. Note, do not increment new_line counter as only want this to increment for positioned False lines
					else:
						line_count += 1
													
			
				# Only once have positioned all lines from that scene and adjusted position of lines from previous scene do we return True and allow lines to be printed to the screen.			
				if line_count == len(lines):							
					return True
		
		# Need to re_position lines after adjusting y-coordinates in "text_too_far"
		elif position_method == "re_position":		
		
			for index, line in enumerate(lines, 0):			
									
				text = pygame.font.Font("ostrich-sans/OstrichSans-Black.otf", lines[index]['fontsize']).render(lines[index]['string'], 1, (0, 0, 0))
								
				# y-coord for this line
				posy = Scene.lines[index]['y-coord']		
		
				# If lines are not already positioned from previous calls to this function, position them here
				if lines[index]['positioned'] == False:			
						
					lines[index]['position'] = text.get_rect(center=(posx, posy))					
					lines[index]['positioned'] = True											
				
					# Increment line count only if text has not gone too far							
					line_count += 1	
				
						
				# Else if lines are set to True then must be already positioned, so increment line_count accordingly	
				else:
					line_count += 1										
		
			# Only once have positioned all lines from that scene and adjusted position of lines from previous scene do we return True and allow lines to be printed to the screen.		
			if line_count == len(Scene.lines):		
				return True
	
	
	# Method to print strings to the Pygame window. Not really sure need room argument at all
	def print_to_screen(self, string, screen, mode):
		
		# Return dictionary of lines
		next_lines = self.content_builder(string, screen)
		
		# Blit to screen in one of three modes: story, simple or scroll?
		self.print_type(next_lines, screen, mode)
		
	
	# Method to simulate space-bar press
	def press_space(self):		
		# Press and release space
		keyboard.press(Key.space)
		keyboard.release(Key.space)
	
	
	# Method to detect which keys are pressed on the keyboard. Note, have extended key detection ability so as to try and detect sentences
	def run_pygame(self, screen):		
						
		# Method variable
		word = []	
		
		# Lists for action_keys (returned immediately) and letters (appended to word list to construct sentences)
		action_keys = ["left", "right", "up", "down", "1", "2", "3", "space", "escape"]	
		
		letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "return"]
				
		while True:			
		
			for event in pygame.event.get():
												
				if event.type == pygame.KEYDOWN:					
					
					# First is the key pressed and action key or a letter key. Depending on which, either return (if len(word) is 1) or continue to append and print word when user hits enter key					
					if pygame.key.name(event.key) in action_keys: 
						
						word.append(action_keys[action_keys.index(pygame.key.name(event.key))])
						
						# As long as only one word is appended to word, return
						if len(word) == 1:
													
							# If user has hit escape key, then game ends							
							if pygame.key.name(event.key) == "escape":
								exit(1)
							
							# Return action_key unless is "escape"
							return action_keys[action_keys.index(pygame.key.name(event.key))]
						
					
					elif pygame.key.name(event.key) in letters:
						
						# Append letter to word list
						word.append(letters[letters.index(pygame.key.name(event.key))])	
						
						# Notify users that they need to hit the return key to reveal what they have typed, but only for first letter
						if pygame.key.name(event.key) != 'return' and len(word) == 1:
							statement = "*** Please hit the enter key to reveal what you have typed! ***"
							self.print_to_screen(statement, screen, "simple")											
						
						# If user hits the return button
						if event.key == pygame.K_RETURN:
							
							#print event.key
							
							# Remove return string and caps lock string from word if there. Replace 'space' with ' '
							words_to_remove = ['return', 'caps lock']
													
							for w in words_to_remove: 
								while w in word: word.remove(w)
																			
							word = [w.replace('space', ' ') for w in word]
						
							# Print and return												
							printed_word = ''.join(word)								
							self.print_to_screen(printed_word, screen, "simple")								
						
							# Re-set word array and return printed_word
							word = []	
							return printed_word	
					
	
	# Enter Scene 
	def enter(self, screen):
		pass
	
	
	
	
	
	
	
							