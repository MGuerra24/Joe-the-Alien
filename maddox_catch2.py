import pygame, simpleGE, random

class Star(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("star.png")
        self.setSize(25,25)
        self.minSpeed = 3
        self.maxSpeed = 8
        self.reset()
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(self.minSpeed, self.maxSpeed)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()

class Asteroid(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("asteroid.png")
        self.setSize(25,25)
        self.minSpeed = -8
        self.maxSpeed = -3
        self.reset()
        
    def reset(self):
        self.y = 500
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(self.minSpeed, self.maxSpeed)
        
    def checkBounds(self):
        if self.bottom < 0:
            self.reset()

class Alien(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("alien.png")
        self.setSize(80,40)
        self.position = (320,200)
        self.moveSpeed = 5
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
        if self.isKeyPressed(pygame.K_UP):
            self.y -= self.moveSpeed
        if self.isKeyPressed(pygame.K_DOWN):
            self.y += self.moveSpeed
          
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score : 0"
        self.center = (100,30)

class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time left : 0"
        self.center = (500,30)

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("space.png")
        
        self.sndStar = simpleGE.Sound("starCollectSound.mp3")
        self.numStars = 10
        
        self.sndAsteroid = simpleGE.Sound("asteroidCollectSound.ogg")
        self.numAsteroids = 5
        
        self.score = 0
        self.lblScore = LblScore()
        
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 30
        self.lblTime = LblTime()
        
        self.alien = Alien(self)
        self.star = Star(self)
        self.asteroid = Asteroid(self)
        
        self.stars = []
        for i in range(self.numStars):
            self.stars.append(Star(self))
            
        self.asteroids = []
        for i in range(self.numAsteroids):
            self.asteroids.append(Asteroid(self))
        
        self.sprites = [self.alien,
                        self.stars,
                        self.asteroids,
                        self.lblScore,
                        self.lblTime]
        
    def process(self):
        for star in self.stars:
            if star.collidesWith(self.alien):
                star.reset()
                self.sndStar.play()
                self.score += 1
                self.lblScore.text = f"Score : {self.score}"
                
        for asteroid in self.asteroids:
            if asteroid.collidesWith(self.alien):
                asteroid.reset()
                self.sndAsteroid.play()
                self.score -= 1
                self.lblScore.text = f"Score : {self.score}"
        
        self.lblTime.text = f"Time Left : {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() < 0:
            print(f"Score : {self.score}")
            self.stop()
            
class Instructions(simpleGE.Scene):
    def __init__(self, prevScore):
        super().__init__()
        self.prevScore = prevScore
        self.setImage("space.png")
        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
            "You are Joe the Alien",
            "Move the ship with the arrow keys",
            "Collect as many stars as possible in 30 seconds",
            "Avoid asteroids",
            "Hit Play to begin",
            "Hit Quit to exit the game",
            ]
        self.directions.center = (320,240)
        self.directions.size = (500,250)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (100,400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540,400)
        
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Last score : 0"
        self.lblScore.center = (320,400)
        self.lblScore.text = f"Last score : {self.prevScore}"
        
        self.sprites = [self.directions,
                        self.btnPlay,
                        self.btnQuit,
                        self.lblScore]
        
    def process(self):
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()
                
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
        
def main():
   keepGoing = True
   lastScore = 0
   
   while keepGoing:
        instructions = Instructions(lastScore)
        instructions.start()
        if instructions.response == "Play":
           game = Game()
           game.start()
           lastScore = game.score
        else:
            keepGoing = False
    
if __name__ == "__main__":
    main()