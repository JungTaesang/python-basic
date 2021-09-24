#https://www.youtube.com/watch?v=Dkx8Pl6QKW0
import pygame
import random

pygame.init()

#화면크기
screen_width = 480 #가로
screen_height = 640 #세로
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀
pygame.display.set_caption("Quiz")

#FPS
clock = pygame.time.Clock()

#배경이미지
background = pygame.image.load("C:/Users/user1/taesang/python-basic/pygame_basic/background.png")

#캐릭터 
character = pygame.image.load("C:/Users/user1/taesang/python-basic/pygame_basic/character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height

to_x = 0
character_speed = 10

game_font = pygame.font.Font(None, 40)

score = 0

#적 캐릭터
enemy = pygame.image.load("C:/Users/user1/taesang/python-basic/pygame_basic/enemy.png")
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = random.randint(0, screen_width-enemy_height)
enemy_y_pos = 0
enemy_speed = 10

a = pygame.image.load("C:/Users/user1/taesang/python-basic/pygame_basic/a.png")
a_size = a.get_rect().size
a_width = a_size[0]
a_height = a_size[1]
a_x_pos = random.randint(0, screen_width-enemy_height)
a_y_pos = 0
a_speed = 10


#이벤트 루프
running = True
while running:
    dt = clock.tick(30) # 초당 프레임 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #키보드이벤트
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

    character_x_pos += to_x
    
    if character_x_pos <0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    
    enemy_y_pos += enemy_speed 

    if enemy_y_pos > screen_height:
        enemy_y_pos = 0
        enemy_x_pos = random.randint(0, screen_width-enemy_height)
    
    a_y_pos += a_speed

    if a_y_pos > screen_height:
        a_y_pos = 0
        a_x_pos = random.randint(0, screen_width-enemy_height)

    #충돌 처리를 위한 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    a_rect = a.get_rect()
    a_rect.left = a_x_pos
    a_rect.top = a_y_pos

    #충돌 체크
    if character_rect.colliderect(enemy_rect):
        print("충돌했어요")
        running = False
        
    elif character_rect.colliderect(a_rect):
         score += 100
         a_y_pos = 0
         a_x_pos = random.randint(0, screen_width-a_height)

    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
    screen.blit(a, (a_x_pos,a_y_pos))
        

    Scoreboard = game_font.render(str(int(score)), True, (255,255,255))

    screen.blit(Scoreboard, (10, 10))
    pygame.display.update()

pygame.time.delay(2000)
pygame.quit()  