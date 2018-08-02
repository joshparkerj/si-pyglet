import pyglet
from random import random
from random import randint

playerScore = 0
gameOn = True

window = pyglet.window.Window(500,500)

batchDraw = pyglet.graphics.Batch()

bgroup = pyglet.graphics.OrderedGroup(0)
fgroup = pyglet.graphics.OrderedGroup(1)

img = pyglet.resource.image

playerImage = img('player.png')
spaceImage = img('space.png')
bulletImage = img('bullet.png')
badImages = [img('bad1.png'),img('bad2.png'),img('bad3.png'),img('bad4.png'),img('bad5.png'),]

med = pyglet.resource.media

zapSound = med('zap.wav', streaming=False)
blastSound = med('blast.wav', streaming=False)

spaceMusic = med('space.wav')

scoreLabel = pyglet.text.Label(text="Score: " + str(playerScore), x=5, y=485, batch=batchDraw, group=fgroup)

musicPlayer = pyglet.media.Player()
musicPlayer.queue(spaceMusic)

kb = pyglet.window.key


Spr = pyglet.sprite.Sprite

background = Spr(img=spaceImage, x=0, y=0, batch=batchDraw, group=bgroup)

playerImage.anchor_y = playerImage.height // 2
bulletImage.anchor_y = bulletImage.height // 2

playerSprite = Spr(img=playerImage, x=0, y=250, batch=batchDraw, group=fgroup)

playerSprite.motion = 0

activeBads = []
activeBullets = []

def movePlayer():
 if playerSprite.y < 0:
  playerSprite.y = 0
 elif playerSprite.y > 500:
  playerSprite.y = 500
 playerSprite.y += playerSprite.motion

def addBad():
 newBad = Spr(img=badImages[randint(0,4)], x=500, y=randint(50,450), batch = batchDraw, group = fgroup)
 newBad.xmotion = -0.1 - random()
 newBad.ymotion = random() * 3 - 1.5
 activeBads.append(newBad)

def moveBad(bad):
 bad.x += bad.xmotion
 bad.y += bad.ymotion
 if bad.y > (500 - bad.height):
  bad.ymotion = -1.5 * random()
 elif bad.y < 0:
  bad.ymotion = 1.5 * random()
 if bad.x < 0:
  gameOver()

def gameOver():
 global gameOn
 scoreLabel.width=400
 scoreLabel.multiline = True
 scoreLabel.text = "GAME OVER You scored: " + str(playerScore)
 scoreLabel.x = 100
 scoreLabel.y = 300
 scoreLabel.font_size = 40
 gameOn = False

def checkKills():
    global playerScore
    for i in range(len(activeBullets)):
        for j in range(len(activeBads)):
            if (activeBullets[i].x > activeBads[j].x - 20
                and activeBullets[i].x < activeBads[j].x + activeBads[j].image.width + 20
                and activeBullets[i].y > activeBads[j].y
                and activeBullets[i].y < activeBads[j].y + activeBads[j].image.height):
                activeBads[j].delete()
                del activeBads[j]
                activeBullets[i].delete()
                del activeBullets[i]
                playerScore += 1
                scoreLabel.text="Score: " + str(playerScore)
                blastSound.play()
                return

def moveThings(dt):
    movePlayer()
    checkKills()
    if len(activeBads) <= playerScore/10:
        addBad()
    for bad in activeBads:
        moveBad(bad)
    for i in range(len(activeBullets)):
        activeBullets[i].x += activeBullets[i].motion
        if activeBullets[i].x > 500:
            activeBullets[i].delete()
            del activeBullets[i]
            break

@window.event
def on_key_press(symbol, modifiers):
    if gameOn:
        if symbol == kb.W:
            playerSprite.motion = 3
        elif symbol == kb.S:
            playerSprite.motion = -3
        elif symbol == kb.F:
            b = Spr(img=bulletImage, x=playerSprite.x, y=playerSprite.y, batch=batchDraw, group=fgroup)
            b.motion = 20
            activeBullets.append(b)
            zapSound.play()

@window.event
def on_key_release(symbol, modifiers):
    if (symbol == kb.W and playerSprite.motion == 3
        or symbol == kb.S and playerSprite.motion == -3):
        playerSprite.motion = 0

@window.event
def on_draw():
    batchDraw.draw()

@window.event
def on_close():
    musicPlayer.pause()

pyglet.clock.schedule_interval(moveThings, 1/120.0)
musicPlayer.play()
pyglet.app.run()
