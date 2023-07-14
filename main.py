import pygame
import random
import math
from pygame import  mixer

# initialize pygame
pygame.init()
# Create Screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("background.png")

# back ground sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and display
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('gameimg1.png')
pygame.display.set_icon(icon)
# Player
playerImg = pygame.image.load('space-invader.png')
playerX = 370
playerY = 480
playerX_change = 0
# enemy
enemyImg =[]
enemyX = []
enemyY = []
enemyx_change = []
enemyy_change = []
num_of_enemy = 6


for i in range (num_of_enemy):
    enemyImg.append( pygame.image.load('ghost.png'))
    enemyX.append( random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyx_change.append(1)
    enemyy_change.append(10)

"""def enemey_speed():
    for i in range(num_of_enemy):
        enemyx_change.pop(0)
        enemyx_change.append(score/10)"""

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletx_change = 0
bullety_change = 10
# bullet state
# redy means cant be seen bullet
bullet_state = "redy"

#score vriable
score = 0
font = pygame.font.Font('freesansbold.ttf',32)
textx = 10
texty = 10

#game over text
over_front =pygame.font.Font('freesansbold.ttf',100)

def game_over_text():
    over_text = over_front.render("game over",True,(255,255,255))
    screen.blit(over_text,(170,200))

def show_score (x,y):
    scorepic =font.render("score : " + str(score),True,(200,200,200))
    screen.blit(scorepic,(x,y))

def fir_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y,i):
    screen.blit(enemyImg[i], (x, y))


def is_collition(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        collition_sound = mixer.Sound('explosion.wav')
        collition_sound.play()
        return True
    return False


# Game Loop
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))
    # backgroound image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if key stroke is presed event .get records it cheack weather iits right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                bulletX = playerX
                fir_bullet(playerX, bulletY)
                #bullet sound
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    # cheaking boundri of space ship
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    # enemey_speed()
    for i in range(num_of_enemy):

        #game over::
        if enemyY[i]>200:
            for j in range(num_of_enemy):
                enemyY[j]=2000
            game_over_text()
            break

        enemyX[i] += enemyx_change[i]
        if enemyX[i] <= 0:
            enemyx_change[i] = +4
            enemyY[i] += enemyy_change[i]
        elif enemyX[i] >= 736:
            enemyx_change[i]  = -4
            enemyY[i] += enemyy_change[i]
         # collition
        collition = is_collition(enemyX[i], enemyY[i], bulletX, bulletY)
        if collition:
            bulletY = 480
            bullet_state = "redy"
            score += 1
            print(score)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i],i)




    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "redy"
    if bullet_state is "fire":
        fir_bullet(bulletX, bulletY)
        bulletY -= bullety_change

    player(playerX, playerY)
    show_score(textx,texty)
    pygame.display.update()
