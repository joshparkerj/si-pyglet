import pyglet
from random import random
from random import randint

gameTime = 0
playerScore = 0
gameOn = True

window=pyglet.window.Window(500,500)

batchDraw = pyglet.graphics.Batch()

bgroup = pyglet.graphics.OrderedGroup(0)
fgroup = pyglet.graphics.OrderedGroup(1)

playerImage = pyglet.resource.image('player.png')
spaceImage = pyglet.resource.image('space.png')
bulletImage = pyglet.resource.image('bullet.png')
badImages = []
badImages.append(pyglet.resource.image('bad1.png'))
badImages.append(pyglet.resource.image('bad2.png'))
badImages.append(pyglet.resource.image('bad3.png'))
badImages.append(pyglet.resource.image('bad4.png'))
badImages.append(pyglet.resource.image('bad5.png'))

zapSound = pyglet.resource.media('zap.wav', streaming=False)
blastSound = pyglet.resource.media('blast.wav', streaming=False)

spaceMusic = pyglet.resource.media('space.wav')

scoreLabel = pyglet.text.Label(text="Score: " + str(playerScore), x=5, y=485, batch=batchDraw, group=fgroup)

musicPlayer = pyglet.media.Player()
musicPlayer.queue(spaceMusic)

kb = pyglet.window.key


playerImage.anchor_y = playerImage.height // 2

background = pyglet.sprite.Sprite(img=spaceImage, x=0, y=0, batch=batchDraw, group=bgroup)

playerSprite = pyglet.sprite.Sprite(img=playerImage, x=0, y=250, batch=batchDraw, group=fgroup)
playerSprite.motion = 0

def movePlayer():
    if playerSprite.y > 0 and playerSprite.y < 500:
        playerSprite.y += playerSprite.motion
    elif playerSprite.y <= 0:
        playerSprite.y = 1
    else:
        playerSprite.y = 499

livingBads = []
flyingBullets = []

def checkKills():
    global playerScore
    for i in range(len(flyingBullets)):
        for j in range(len(livingBads)):
            if (flyingBullets[i].x > livingBads[j].x - 20
                and flyingBullets[i].x < livingBads[j].x + livingBads[j].image.width + 20
                and flyingBullets[i].y > livingBads[j].y
                and flyingBullets[i].y < livingBads[j].y + livingBads[j].image.height):
                livingBads[j].delete()
                del livingBads[j]
                flyingBullets[i].delete()
                del flyingBullets[i]
                playerScore += 1
                scoreLabel.text="Score: " + str(playerScore)
                blastSound.play()
                return

def moveBad(bad):
    global gameOn
    bad.x -= bad.xmotion
    bad.y += bad.motion
    if bad.y > 450:
        bad.motion = -1.5 * random()
    elif bad.y < 50:
        bad.motion = 1.5 * random()
    if bad.x < 0:
        scoreLabel.width=400
        scoreLabel.multiline = True
        scoreLabel.text = "GAME OVER You scored: " + str(playerScore)
        scoreLabel.x = 100
        scoreLabel.y = 300
        scoreLabel.font_size = 40
        gameOn = False

def addBad():
    livingBads.append(pyglet.sprite.Sprite(img=badImages[randint(0,4)], x=550, y=450-randint(0,400), batch=batchDraw, group=fgroup))
    if len(livingBads) > 0:
        livingBads[-1].motion = random()*3 - 1.5
        livingBads[-1].xmotion = 0.1+random()

def moveThings(dt):
    global gameTime
    gameTime += 1
    movePlayer()
    checkKills()
    if len(livingBads) <= playerScore/10:
        addBad()
    for bad in livingBads:
        moveBad(bad)
    for i in range(len(flyingBullets)):
        flyingBullets[i].x += flyingBullets[i].motion
        if flyingBullets[i].x > 500:
            flyingBullets[i].delete()
            del flyingBullets[i]
            break

@window.event
def on_key_press(symbol, modifiers):
    if gameOn:
        if symbol == kb.W:
            playerSprite.motion = 3
        elif symbol == kb.S:
            playerSprite.motion = -3
        elif symbol == kb.F:
            b = pyglet.sprite.Sprite(img=bulletImage, x=playerSprite.x, y=playerSprite.y, batch=batchDraw, group=fgroup)
            b.motion = 20
            flyingBullets.append(b)
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
