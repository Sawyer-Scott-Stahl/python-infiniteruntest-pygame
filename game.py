import pygame
import sys
import random

pygame.init()

win_w = 575
win_h = 575

botbar = 50

fillcolor = [75, 75, 75]
linecolor = [0, 175, 0]
botcolor = [0, 0, 0]
playercolor = [0, 0, 175]
enemycolor = [175, 0, 0]
scorecolor = [255, 255, 255]
pointcolor = [255, 100, 255]

pointslimit = 1
startspeed = 10
speed_mult = .1
pointsbuffer = 20
pointgain = 1
pointloss = 1
levelchange = 10
maxlevel = 20

enemies = []
points = []

level_speeds = [startspeed, startspeed]
s = startspeed

for i in range(1, maxlevel + 1):
    s = s + (s * speed_mult)
    level_speeds.append(s)

win = pygame.display.set_mode([win_w, win_h])
pygame.display.set_caption("Infinite Run Test")
clock = pygame.time.Clock()


class Player:
    def __init__(self):
        self.radius = 20
        self.x = 287
        self.y = int(win_h - botbar - 150)
        self.lane = 3
        self.score = 0
        self.dead = 0


player = Player()


class Enemy:
    def __init__(self, lane):

        self.lane = lane

        self.h = 40
        self.speed = startspeed

        self.y = -1 - self.h
        self.w = 101

        if lane == 1:
            self.x = 11
        if lane == 2:
            self.x = 124
        if lane == 3:
            self.x = 237
        if lane == 4:
            self.x = 350
        if lane == 5:
            self.x = 463


class Points:
    def __init__(self, lane):

        self.lane = lane

        self.radius = 10
        self.speed = startspeed

        self.y = -1 - self.radius

        if lane == 1:
            self.x = 287 - 113 - 113
        if lane == 2:
            self.x = 287 - 113
        if lane == 3:
            self.x = 287
        if lane == 4:
            self.x = 287 + 113
        if lane == 5:
            self.x = 287 + 113 + 113


def game():
    global enemies
    global points
    spawncount = 0
    player.level = 1
    while 1:
        clock.tick(30)
        drawgame()

        speed = int(level_speeds[player.level])

        spawn = 100 / speed

        if player.dead == 1:
            pygame.mouse.set_visible(True)
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (win_w / 2 - 75 <= mouse[0] <= win_w / 2 - 75 + 150 and
                            (win_h - botbar) / 2 + 20 <= mouse[1] <= (win_h - botbar) / 2 + 20 + 50):
                        enemies = []
                        points = []
                        player.score = 0
                        player.level = 1
                        player.lane = 3
                        player.x = 287
                        player.dead = 0
                        game()

        else:
            pygame.mouse.set_visible(False)
            if player.score > 0:
                if player.score >= maxlevel * levelchange:
                    player.level = maxlevel
                else:
                    player.level = (player.score // levelchange) + 1
            else:
                player.level = 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if player.lane != 1:
                            player.x = player.x - 113
                            player.lane -= 1
                        else:
                            player.x = player.x + 452
                            player.lane = 5
                    if event.key == pygame.K_RIGHT:
                        if player.lane != 5:
                            player.x = player.x + 113
                            player.lane += 1
                        else:
                            player.x = player.x - 452
                            player.lane = 1

            if spawncount >= spawn:
                spawncount = 0
                rand = random.randint(1, 5)
                if len(enemies) > 0:
                    if enemies[-1].lane == rand:
                        spawncount = spawn
                    elif len(points) > 0:
                        if points[-1].y <= pointsbuffer and points[-1].lane == rand:
                            spawncount = spawn
                        else:
                            enemies.append(Enemy(rand))
                    else:
                        enemies.append(Enemy(rand))
                else:
                    enemies.append(Enemy(rand))
            else:
                spawncount += 1

            for enemy in enemies:
                enemy.speed = speed
                enemy.y += enemy.speed
                if enemy.y > win_h:
                    enemies.pop(enemies.index(enemy))
                elif enemy.lane == player.lane:
                    if player.y - player.radius <= enemy.y <= player.y + player.radius or \
                            player.y - player.radius <= enemy.y + enemy.h <= player.y + player.radius:
                        player.dead = 1

            if len(points) < pointslimit:
                rand = random.randint(1, 5)
                if len(enemies) > 0:
                    if rand != enemies[-1].lane:
                        points.append(Points(rand))
                else:
                    points.append(Points(rand))

            for point in points:
                point.speed = speed
                point.y += point.speed
                if point.y - point.radius > win_h:
                    player.score -= pointloss
                    points.pop(points.index(point))
                elif point.lane == player.lane:
                    if player.y - player.radius <= point.y - point.radius <= player.y + player.radius or \
                            player.y - player.radius <= point.y + point.radius <= player.y + player.radius:
                        points.pop(points.index(point))
                        player.score += pointgain


def drawgame():
    win.fill(fillcolor)

    pygame.draw.rect(win, linecolor, [0, 0, 10, win_h])
    pygame.draw.rect(win, linecolor, [113, 0, 10, win_h])
    pygame.draw.rect(win, linecolor, [226, 0, 10, win_h])
    pygame.draw.rect(win, linecolor, [339, 0, 10, win_h])
    pygame.draw.rect(win, linecolor, [452, 0, 10, win_h])
    pygame.draw.rect(win, linecolor, [565, 0, 10, win_h])

    pygame.draw.circle(win, playercolor, [player.x, player.y], player.radius)

    for point in points:
        pygame.draw.circle(win, pointcolor, [point.x, point.y], point.radius)

    for enemy in enemies:
        pygame.draw.rect(win, enemycolor, [enemy.x, enemy.y, enemy.w, enemy.h])

    pygame.draw.rect(win, botcolor, [0, win_h - botbar, win_w, botbar])
    scorefont = pygame.font.Font("opensans.ttf", 20)
    scoretext = scorefont.render("Score: " + str(player.score), 1, scorecolor)
    win.blit(scoretext, [win_w - scoretext.get_rect()[2] - 20,
                         win_h - scoretext.get_rect()[3] - scoretext.get_rect()[3] / 2])
    levelfont = pygame.font.Font("opensans.ttf", 30)
    leveltext = levelfont.render("Level: " + str(int(player.level)), 1, scorecolor)
    win.blit(leveltext, [20, win_h - leveltext.get_rect()[3] - leveltext.get_rect()[3] / 6])

    if player.dead == 1:
        mouse = pygame.mouse.get_pos()
        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 200, (win_h - botbar) / 2 - 100, 400, 200])
        pygame.draw.rect(win, [150, 150, 150], [win_w / 2 - 190, (win_h - botbar) / 2 - 90, 380, 180])
        deadfont = pygame.font.Font("Chunkfive.otf", 50)
        deadtext = deadfont.render("You Died", 1, [0, 0, 0])
        win.blit(deadtext, [win_w / 2 - deadtext.get_rect()[2] / 2, (win_h - botbar) / 2 - 90 + 50])
        pygame.draw.rect(win, [0, 0, 0], [win_w / 2 - 75, (win_h - botbar) / 2 + 20, 150, 50])
        if (win_w / 2 - 75 <= mouse[0] <= win_w / 2 - 75 + 150 and
                (win_h - botbar) / 2 + 20 <= mouse[1] <= (win_h - botbar) / 2 + 20 + 50):
            pygame.draw.rect(win, [200, 200, 50], [win_w / 2 - 70, (win_h - botbar) / 2 + 25, 140, 40])
        else:
            pygame.draw.rect(win, [245, 245, 50], [win_w / 2 - 70, (win_h - botbar) / 2 + 25, 140, 40])
        restartfont = pygame.font.Font("Chunkfive.otf", 30)
        restarttext = restartfont.render("Restart", 1, [0, 0, 0])
        win.blit(restarttext, [(win_w / 2 - 70) + (70 - restarttext.get_rect()[2] / 2), (win_h - botbar) / 2 + 32])

    pygame.display.update()


if __name__ == '__main__':
    game()
