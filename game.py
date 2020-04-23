# encoding: utf-8

import os
import pygame
from random import randint
pygame.init()


'''
Game settings.
'''
screenSize = 600, 600
screen = pygame.display.set_mode(screenSize)
background = pygame.image.load(os.path.join('images/assets/gp.jpg'))
pygame.display.set_caption("@onathanbahia - github.com/nathanbahia")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 18, bold=True, italic=True)
fonteLarge = pygame.font.SysFont("gentiumbasic", 36, bold=True, italic=False)
soundTrack = pygame.mixer.Sound(os.path.join('sounds/sound-track.ogg'))


'''
Read the file score.txt to set the variable highScore.
'''
file = open('score.txt', 'r')
for i in file:
	highScore = i

class StartGame():
	def __init__(self, screen):
		'''
		Defines the frames of menu and set the variable gameStarted as False.
		'''
		self.screen = screen
		self.images = ['images/assets/frame1.jpg','images/assets/frame2.jpg']
		self.menuOption = 0
		self.background = pygame.image.load(os.path.join(self.images[self.menuOption]))
		self.gameStarted = False
		
	def select_option(self):
		'''
		Select the menu options. If menuOption is set as 1, 
		gameStarted will be changed by True and the game will start.
		'''
		if self.gameStarted == False:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
				if self.menuOption == 0:
					self.menuOption = 1
				else:
					self.menuOption = 0
			self.background = pygame.image.load(os.path.join(self.images[self.menuOption]))
			
			if self.menuOption == 0:
				if keys[pygame.K_RETURN]:
					self.gameStarted = True
			
				
	def draw(self):
		'''
		Checks if the game don't started and draw the menu screen and the high score.
		This method call select_option.
		'''
		if self.gameStarted == False:		
			self.screen.blit(self.background, (0,0))
									
			txtHighScore = fonteLarge.render(str(highScore), True, (255,255,255), None)
			self.screen.blit(txtHighScore, (180, 15))					
			
			self.select_option()
			
	
	def check_game_over(self, player):
		'''
		Method that receives as paramether the player instance
		to checks its health is less or equal zero, so this 
		method return True and stop the while loop at the end of this code.
		'''
		self.player = player
		if self.player.health <= 0:
			self.gameOverImg = pygame.image.load(os.path.join('images/assets/gameover.jpg'))
			self.screen.blit(self.gameOverImg, (0,0))				
			return True
		else:
			return False
		

class Ammo():
	def __init__(self, screen):
		self.screen = screen				
		self.image = pygame.image.load(os.path.join('images/assets//ammo.png'))		
		self.rect = self.image.get_rect()		
		self.rect.x = -100
		self.rect.y = -100
		self.min = 5
		
	def set_position(self):
		'''
		Methos used to determine a random position to the ammo' sprite ever
		when the ammount of ammo's player if less than the self.min.
		This method is called by player.get_ammo().
		'''
		self.rect.x = randint(50, 550)
		self.rect.y = randint(50, 550)
	
		
	def draw(self):
		'''
		This method is executed every time while the game is running.
		When the method set_position is activated, the sprite is drawned
		inside the scren.	
		'''
		self.screen.blit(self.image, (self.rect.x, self.rect.y))
		
				

class Shot():
	def __init__(self, screen, posX, posY):
		self.screen = screen				
		self.image = pygame.Surface([15, 8])
		self.image.fill((223,116,1))
		self.rect = self.image.get_rect()		
		self.rect.x = posX + 110
		self.rect.y = posY + 35		
		self.vel = 20
		self.screen.blit(self.image, (self.rect.x, self.rect.y))				
		
		
	def draw(self):
		'''
		Whenever the player has suficient ammo to shot, an instance of Shot() 
		is created using the paramethers posX and posY (player's position). 
		Then, it moves at screen using the self.vel.	
		'''
		self.rect.x += self.vel
		self.screen.blit(self.image, (self.rect.x, self.rect.y))				
			

class Player():
	def __init__(self, screen):
		self.screen = screen		
		self.spriteNumber = 3 # initial index to set a player's sprite
		self.spriteVel = 3	# speed of sprite's transition
		self.spriteInt = 0	# just a variable to iteration to compare with spriteVel			
		self.sprites = ['bigode0.png','bigode1.png', 'bigode2.png', 'bigode3.png'] # sprites
		self.image = pygame.image.load(os.path.join('images/player/',self.sprites[self.spriteNumber]))	# draw the sprite using the self.sprites and self.spriteNumber
		self.rect = self.image.get_rect() # get the rect of the current sprite
		self.rect.x = 150 # defines the x position
		self.rect.y = 150 #	defines the y position	
		self.vel = 5 # speed of walking		
		self.health = 10 # the ammout of health
		self.score = 0 # the current score
		self.ammo = 5 # the ammount of ammo		
		self.ammoInt = 1 # variable used to control the ammout of instances of the class Shot() has on the screen
		self.hasAmmo = True # used to define if the player can shot
		self.isWalking = False # used to define if the player is walking
		self.isShoting = False # used to define if the player is shoting
			
		
	def draw(self):
		'''
		Method used to check whether the player is walking or shooting.

		If walking, the method creates a loop using self.spriteInt in comparison
		to self.spriteVel, so that each frame loaded in self.sprites is accessed
		taking self.spriteNumber as an index. Whenever self.spriteInt == self.spriteVel,
		self.spriteNumber is increased by +1, which causes the sprites to change
		slower depending on the value passed to sels.spriteVel.

		Finally, if self.spriteNumber is equal to len (self.sprites) - 1, it returns
		to 0, returning the loop.
		'''		        						
		if self.isShoting == False:
			if self.isWalking == True:
				if self.spriteInt == self.spriteVel:
					if self.spriteNumber < len(self.sprites) - 1:		
						self.spriteNumber += 1				 							
					else:
						self.spriteNumber = 0
					self.spriteInt = 0
				self.spriteInt += 1
			else:
				self.spriteNumber = 0
				
			self.image = pygame.image.load(os.path.join('images/player/',self.sprites[self.spriteNumber]))						
			screen.blit(self.image, (self.rect.x, self.rect.y))		
		
		'''
		If the self.isShoting condition is true, a loop similar to the one above 
		is generated, but smaller, due to having to load only one sprite.
		'''	
		if self.isShoting == True:		
			self.image = pygame.image.load(os.path.join('images/player/bigode-shoting.png'))
			screen.blit(self.image, (self.rect.x, self.rect.y))				
			
			
			if self.spriteInt  < 5:										
				self.spriteInt += 1				
			else:			
				self.spriteInt = 0
				self.isShoting = False
				self.isWalking = True
					
		'''
		Plotting health and ammo parameters using the font selected at the beginning of the code
		'''
		life = fonte.render("HEALTH: "+str(self.health), True, (0,0,0), None)
		screen.blit(life, (10, 10))
		ammo = fonte.render("AMMO: "+str(self.ammo), True, (0,0,0), None)
		screen.blit(ammo, (160, 10))
		score = fonte.render("SCORE: "+str(self.score), True, (0,0,0), None)
		screen.blit(score, (290, 10))
		txtHighScore = fonte.render("HIGH SCORE: "+str(highScore), True, (0,0,0), None)
		screen.blit(txtHighScore, (440, 10))			
			
	
	def mov(self):
		'''
		Method that evaluates the player's position in relation to the screen size
		and returns movement when the given keys are pressed.
		It also defines whether the player is walking or not.
		'''

		keys = pygame.key.get_pressed()

		if self.rect.y < screenSize[1] - self.rect.h:
			if keys[pygame.K_DOWN]:					
				self.rect.y += self.vel
				self.isWalking = True
		if self.rect.y > 0:	
			if keys[pygame.K_UP]:
				self.rect.y -= self.vel
				self.isWalking = True
		if self.rect.x > 0:	
			if keys[pygame.K_LEFT]:
				self.rect.x -= int(self.vel / 1.5)
				self.isWalking = True
		
		if self.rect.x < screenSize[0] - self.rect.w:	
			if keys[pygame.K_RIGHT]:
				self.rect.x += self.vel
				self.isWalking = True
				
		if not keys[pygame.K_DOWN] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
			self.isWalking = False
			
	
	def shot(self, shots):
		'''
		Method that takes an empty dictionary as a parameter to store the instances
		of the Shot () class. Checks if the player has ammunition, if so, a new 
		instance of Shot () is created and stored in self.shot, and self.ammo
		is decreased by 1.
		'''		
		self.shots = shots
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				if self.ammo > 0:				
					self.ammo -= 1
					self.shots[str(self.ammoInt)] = Shot(self.screen, self.rect.x, self.rect.y)				
					self.ammoInt += 1
					self.isShoting = True						
					  
								
	def check_colissions(self, enemies):
		'''
		Method that receives a dictionary that must contain the instances of
		class Enemies () and checks if there was a collision between the player
		and each enemy on the screen.
		'''
		self.enemies = enemies		
		for e in self.enemies:
			if self.rect.colliderect(self.enemies[e].rect):
				self.enemies[e].rect.x = 1000
				self.health -= 1
				
		
	def get_ammo(self, extra_ammo):
		'''
		Method that takes as an parameter an instance of the Ammo () class and
		defines if the player is low on ammo, then the set.position () method of
		class Ammo () is executed, causing the sprite to be drawn in
		a random position within the screen.
		'''		
		self.extra_ammo = extra_ammo
		
		if self.ammo <= extra_ammo.min:
			if self.hasAmmo == True:
				self.hasAmmo = False
				self.extra_ammo.set_position()

		'''
		If the player collides with the ammunition, the instance is
		positioned off the screen until the condition 
		of the above is true again.
		'''
		if self.rect.colliderect(self.extra_ammo.rect):
			self.ammo += 10
			self.extra_ammo.rect.x = -100
			self.extra_ammo.rect.y = -100
			self.hasAmmo = True
			
			

class Enemies():
	def __init__(self):		
		self.image = pygame.image.load(os.path.join('images/enemies/','coronga.png'))
		self.rect = self.image.get_rect()		
		self.rect.x = randint(700,800)
		self.rect.y = randint(0, 600)
		self.vel = randint(3, 6)

	
	def draw(self, screen):
		'''
		Method that receives as paramether the screen where the sprites 
		will be drawned.
		'''
		self.screen = screen
		screen.blit(self.image, (self.rect.x, self.rect.y))		
		self.mov()						
					

	def mov(self):
		'''
		After the draw () method is executed, each instance of the class returns a
		horizontal shift to the left until its point x is <= 0,
		so the instances are relocated to a random position at the end of the screen,
		returning to move to the left.
		In order to avoid call new instances and the game gains in performance.
		'''
		self.rect.x -= self.vel
		if self.rect.x <= 0 - self.rect.w:
			self.rect.x = randint(700, 800)
			self.rect.y = randint(0, 600)
				
	
	def check_shots(self, shots, player):
		'''		
		Method that receives a dict as paramether to iteration and check if the 
		enemy collided with a instance of Shot() contained in that dict. So, the enemy
		is moved to a random position at the end of screen and return its path. The Shot()
		instance is removed.
		The paramether player is used to increase at 1 the player's score.

		'''		
		self.shots = shots
		self.player = player
			
		for s in self.shots:
			if self.rect.colliderect(self.shots[s].rect):
				self.rect.x = randint(700, 800)
				self.rect.y = randint(0, 600)			
				self.shots[s].rect.x = 1500
				self.player.score += 1				
				

#-------------------------------------------------------#

# Creating the instances of classes

menu = StartGame(screen)

player = Player(screen)

enemies = {}
for i in range(10): # (10) -> how many enemies you want at screen
	enemies[str(i)] = Enemies()
	
extra_ammo = Ammo(screen)

shots = {}
	
#-------------------------------------------------------#



while True:
	'''
	Set the volume and play the music
	'''
	soundTrack.set_volume(0.2)
	soundTrack.play(loops=0, maxtime=0, fade_ms=0)		
	
	'''
	Get the events
	'''
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

		'''
		Checks if the game ended, then restart the 
		paramether to their initial values
		'''
		if menu.check_game_over(player) == True:	
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					player.health = 10
					player.ammo = 10
					player.score = 0
					player.rect.x = 100
					player.rect.y = 100
					
					for e in enemies:
						enemies[e].rect.x = 900

			'''
			If the player.score is bigger than the value of the variable highScore,
			the value of highScore is set as player.score.
			'''
			if player.score > int(highScore):
				file = open('score.txt', 'w')
				file.write(str(player.score))			

		'''
		Checks if the player press the key SPACE and calls the shot() method.
		'''
		player.shot(shots)	
	

	'''
	Check the game status
	'''
	if menu.gameStarted == False:
		menu.draw()
		
	else:				
		#screen.blit(background, (0,0))
		screen.fill((255,255,255))
		
		'''
		If the game don't over:
		'''
		if menu.check_game_over(player) == False:
		
			for i in enemies:
				enemies[i].draw(screen)
				enemies[i].check_shots(shots, player)
				
			for i in shots:
				shots[i].draw()

			player.draw()
			player.mov()
			player.check_colissions(enemies)
			player.get_ammo(extra_ammo)
			
			extra_ammo.draw()
	
	'''
	Set the ammout of FPS and update the screen
	'''
	clock.tick(40)
	pygame.display.update()
