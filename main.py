import pygame;
clock = pygame.time.Clock()
from datetime import *

pygame.init()
screen = pygame.display.set_mode([560, 360])
pygame.display.set_caption('game')
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

bg = pygame.image.load('images/fon.png').convert()
wolk_left = [
    pygame.image.load('images/player_left/player_left1.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left2.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left3.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left4.png').convert_alpha(),
]
wolk_right = [
    pygame.image.load('images/player_right/player_right1.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right2.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right3.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right4.png').convert_alpha(),
    ]

player_count = 0
bgx = 0

player_speed = 5
player_x = 150
player_y = 250

is_jump = 0
jump_count = 8

k  = 0

bgsound = pygame.mixer.Sound('sounds/1.mp3')
bgsound.play()

ghost = pygame.image.load('images/vrag.png').convert_alpha()
ghost_list_in_game = []

t = str(datetime.now().time())
s = (int(t[t.rfind(':')+1:t.find('.')])+18)%60
v = (s)
i = 1

bullet = pygame.image.load('images/2.png').convert_alpha()
bullets = []

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)
j = 0
game_play = 1

bullets_left = 5

label = pygame.font.Font('fonts/font.ttf', 40)
lose_label = label.render('Вы проиграли!', 0, (193, 196, 199))
restart_label = label.render('Играть занова', 0, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft = (160, 200))

while i:
    screen.blit(bg, [bgx, 0])
    screen.blit(bg, [bgx + 618, 0])
    
    if game_play:
        
        player_rect = wolk_left[0].get_rect(topleft = (player_x, player_y))

        for (j, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10
                if el.x < -10:
                    ghost_list_in_game.pop(j)

                if player_rect.colliderect(el):
                    game_play = 0

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            screen.blit(wolk_left[player_count], [player_x, player_y])
        else: 
            screen.blit(wolk_right[player_count], [player_x, player_y])

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 50:
            player_x -= player_speed
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < 290:
            player_x += player_speed

        t = str(datetime.now().time())
        s = int(t[t.rfind(':')+1:t.find('.')])
        
        if game_play:
            if s == v % 60 or k==1:
                k=0;v+=18;bgsound.play();print(1)
        else:bgsound.stop()

        if player_count == 3:player_count = 0
        else:
            player_count += 1

        if bgx == -618:bgx = 0
        else:bgx -=2

        if bullets:
            for (ind, ele) in enumerate(bullets):
                screen.blit(bullet, (ele.x, ele.y))
                ele.x += 4
                if ele.x > 550:
                    bullets.pop(ind)
                
                if ghost_list_in_game:    
                    for (index, ghoste) in enumerate(ghost_list_in_game):
                        if ele.colliderect(ghoste):
                            ghost_list_in_game.pop(index)
                            bullets.pop(ind)
        if not is_jump:
            if keys[pygame.K_UP] or keys[pygame.K_SPACE]:is_jump = 1
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count**2) / 2
                else:
                    player_y += (jump_count**2) / 2
                jump_count -= 1
            else:
                is_jump = 0
                jump_count = 8
    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (160, 100))
        screen.blit(restart_label, restart_label_rect)
        k = 1;keys = pygame.key.get_pressed()
        mose = pygame.mouse.get_pos()
        if (restart_label_rect.collidepoint(mose) and pygame.mouse.get_pressed()[0]) or keys[pygame.K_r]:
            game_play = 1
            player_x = 150
            bullets_left = 5
            ghost_list_in_game.clear()
            bullets.clear()
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();quit()
        
        if event.type == ghost_timer:
                ghost_list_in_game.append(ghost.get_rect(topleft = (590, 250)))
        
        if game_play and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and bullets_left != 0:
            bullets.append(bullet.get_rect(topleft = (player_x+30, player_y+10)))
            bullets_left -= 1
    
    clock.tick(15)