import pygame
import random
import math
from pygame import mixer
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Donald the Killer")
icon = pygame.image.load("iconfinder_trump_president_avatar_male_4043269.png")
pygame.display.set_icon(icon)

background = pygame.image.load("mexican.png")

bgm = "Resilience.ogg"
mixer.music.load(bgm)
mixer.music.play(-1)

playerimage = pygame.image.load("donaldtrump.png")
playerX = 370
playerY = 480
playerX_change = 0

enemyImageList = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_counter = 6
enemyImageList.append(pygame.image.load('united-states.png'))
enemyImageList.append(pygame.image.load('virus.png'))
enemyImageList.append(pygame.image.load('001-mexico.png'))

for i in range(enemy_counter):
    enemyImageList.append(random.choice(enemyImageList))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

bulletimage = pygame.image.load("002-mariachi.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerimage, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImageList[i], (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimage, (x+16, y+10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2))+(math.pow(enemyY-bulletY, 2)))
    if distance < 35:
        return True
    else:
        return False


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    over_text2 = over_font.render("Your score: " + str(score_value), True, (255, 0, 0))
    screen.blit(over_text, (200, 250))
    screen.blit(over_text2, (200, 300))



running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_SPACE:

                if bullet_state is "ready":
                    sound1 = mixer.Sound("trump-Losers.wav")
                    sound1.play()
                    bulletX = playerX
                    fire(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 735

    for i in range(enemy_counter):
        if enemyY[i] > 400:
            for j in range(enemy_counter):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            sound2 = mixer.Sound("boom.aiff")
            sound2.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            display_number = enemyImageList[random.randint(0, 2)]

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()