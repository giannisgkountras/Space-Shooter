import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH = 900 
HEIGHT = 500
FPS = 60
VEL = 6
BULLET_VEL = 8
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("John's Game")

MAX_BULLETS = 3

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'bullet_hit.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'bullet_fire.mp3'))
BACKGROUND_MUSIC = pygame.mixer.Sound(os.path.join('Assets', 'music.mp3'))
GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'game_over.mp3'))



HEALTH_FONT = pygame.font.Font(os.path.join('Assets', 'font.TTF'),20)
WINNER_FONT = pygame.font.Font(os.path.join('Assets', 'winner_font.TTF'),50)
START_FONT = pygame.font.Font(os.path.join('Assets', 'winner_font.TTF'),100)


YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BORDER = pygame.Rect(WIDTH//2 -5, 0, 10, HEIGHT)

SPACESHIP_WIDTH =40
SPACESHIP_HEIGHT = 50

SPACESHIP_RED_LOST = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'spaceship_red_lost.png')), (50,65))
SPACESHIP_YELLOW_LOST = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'spaceship_yellow_lost.png')), (50,65))
ICON = pygame.image.load(os.path.join('Assets', 'icon.png'))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))
RED_BULLET_IMAGE = pygame.image.load(os.path.join('Assets', 'red_bullet.png'))
YELLOW_BULLET_IMAGE = pygame.image.load(os.path.join('Assets', 'yellow_bullet.png'))
BULLET_RED = pygame.transform.scale (RED_BULLET_IMAGE,(20,8))
BULLET_YELLOW = pygame.transform.rotate(pygame.transform.scale (YELLOW_BULLET_IMAGE,(20,8)),180)
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP, 270)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP, 90)
END = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'end.png')), (WIDTH, HEIGHT))

pygame.display.set_icon(ICON)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health , yellow_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, (10,10,10),BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health),1, (255, 255, 255))
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health),1, (255, 255, 255))
    WIN.blit(red_health_text,( WIDTH -red_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text,(10,10))

    
    WIN.blit(YELLOW_SPACESHIP,(yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x, red.y))
    for bullet_red in red_bullets:
        WIN.blit(BULLET_RED,(bullet_red.x ,bullet_red.y))
    for bullet_yellow in yellow_bullets:
        WIN.blit(BULLET_YELLOW,(bullet_yellow.x ,bullet_yellow.y))
    
   


    pygame.display.update()

def yellow_handle_movement(key_pressed , yellow):
    if key_pressed[pygame.K_a] and yellow.x -VEL > 0:                                        #YELLOW CONTROLS
        yellow.x -= VEL
    if key_pressed[pygame.K_d] and yellow.x +VEL < BORDER.x-SPACESHIP_WIDTH +5:                                       #YELLOW CONTROLS
        yellow.x += VEL
    if key_pressed[pygame.K_w] and yellow.y -VEL > 0:                                       #YELLOW CONTROLS
        yellow.y -= VEL
    if key_pressed[pygame.K_s] and yellow.y +VEL < HEIGHT-SPACESHIP_HEIGHT:                                       #YELLOW CONTROLS
        yellow.y += VEL


def red_handle_movement(key_pressed , red):
    if key_pressed[pygame.K_LEFT] and red.x -VEL> BORDER.x :                                    #RED CONTROLS
        red.x -= VEL
    if key_pressed[pygame.K_RIGHT] and red.x +VEL< WIDTH - SPACESHIP_WIDTH:                                  #RED CONTROLS
        red.x += VEL
    if key_pressed[pygame.K_UP]and red.y -VEL > 0:                                       #RED CONTROLS
        red.y -= VEL
    if key_pressed[pygame.K_DOWN]and red.y +VEL < HEIGHT-SPACESHIP_HEIGHT:                                       #RED CONTROLS
        red.y += VEL

def handle_bullets(yellow_bullets , red_bullets, yellow, red):
    for bullet_yellow in yellow_bullets:
        bullet_yellow.x += BULLET_VEL
        if red.colliderect(bullet_yellow) :
            yellow_bullets.remove(bullet_yellow)
            pygame.event.post(pygame.event.Event(RED_HIT))
            BULLET_HIT_SOUND.play()
        elif bullet_yellow.x > WIDTH:
            yellow_bullets.remove(bullet_yellow)



    for bullet_red in red_bullets:
        bullet_red.x -= BULLET_VEL
        if yellow.colliderect(bullet_red):
            red_bullets.remove(bullet_red)
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            BULLET_HIT_SOUND.play()
        elif bullet_red.x < 0:
            red_bullets.remove(bullet_red)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, (255,255,255))
    WIN.blit(draw_text,(WIDTH//2- draw_text.get_width()//2, HEIGHT//2- draw_text.get_height()//2 ))
    pygame.display.update()
    GAME_OVER_SOUND.play()
    pygame.time.delay(5000)

def end_text():
    WIN.blit(END, (0,0))
    pygame.display.update()
    pygame.time.delay(1000)

def main():
    BACKGROUND_MUSIC.play(-1)
    RED_HEALTH = 15
    YELLOW_HEALTH = 15   
    red = pygame.Rect(800,210,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(20,210,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    bullet_red = pygame.Rect(800,210,10,10)
    bullet_yellow = pygame.Rect(20,210,10,10)
    red_bullets = []
    yellow_bullets = []
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_text()
                run = False
                
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet_yellow = pygame.Rect(yellow.x+SPACESHIP_WIDTH ,yellow.y-(SPACESHIP_HEIGHT//2-42),10,10)
                    yellow_bullets.append(bullet_yellow)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS: 
                    bullet_red = pygame.Rect(red.x-SPACESHIP_WIDTH+30 ,red.y-(SPACESHIP_HEIGHT//2-42),10,10)
                    red_bullets.append(bullet_red)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                RED_HEALTH -=1
            if event.type == YELLOW_HIT:
                YELLOW_HEALTH -=1

        winner_text = ""
        if RED_HEALTH <= 0:
            winner_text = "Yellow wins!"
            WIN.blit(SPACESHIP_RED_LOST,(red.x,red.y))
            
        if YELLOW_HEALTH <=0:
            winner_text = "Red wins!"
            WIN.blit(SPACESHIP_YELLOW_LOST,(yellow.x,yellow.y))

        if winner_text != "":
            BACKGROUND_MUSIC.stop()
            draw_winner(winner_text)
            GAME_OVER_SOUND.stop()
            break


        
        handle_bullets(yellow_bullets , red_bullets, yellow, red)
        key_pressed = pygame.key.get_pressed()
        yellow_handle_movement(key_pressed, yellow)
        red_handle_movement(key_pressed, red)
        draw_window(red , yellow, red_bullets, yellow_bullets, RED_HEALTH , YELLOW_HEALTH)
    
    main()



if __name__ == "__main__":
        main()