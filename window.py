import pygame
from sys import exit 

pygame.init()

screen = pygame.display.set_mode((800, 600), flags=pygame.SCALED, vsync=1)
pygame.display.set_caption('Jumper Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
background_color = (255, 255, 255)


#player_surface = pygame.Surface((80,80))
#player_surface.fill('Red')
#player_pos_x = 20
#player_pos_y = 370

ground_surface = pygame.Surface((800, 150))
ground_surface.fill('#805a32')

# Intro Screen

game_name = test_font.render(' Jumper Game ', False, (0, 0, 0))
game_name_rect = game_name.get_rect(center = (400, 120))

press_to_play = test_font.render(' Press c to Play ', False, (255, 0, 0))
press_to_play_rect = press_to_play.get_rect(center = (400, 450))

game_active = False
beaten_the_level = False

# End Screen
finish_level_message = test_font.render(" You beat the level!!", False, (0, 0, 0))
finish_level_message_rect = finish_level_message.get_rect(center = (400, 80))

buttowski_pic = pygame.image.load('graphics/buttowski.png').convert_alpha()
buttowski_pic = pygame.transform.scale(buttowski_pic, (int(513/2), int(538/2)))
buttowski_pic_rect = buttowski_pic.get_rect(center = (400, 260))

press_c_to_play = test_font.render("Type 'c' to play again", False, (0, 0, 0))
press_c_to_play_rect = press_c_to_play.get_rect(center = (400, 450))

press_q_to_quit = test_font.render("Type 'q' to quit playing", False, (0, 0, 0))
press_q_to_quit_rect = press_q_to_quit.get_rect(center = (400, 510))

# classes
''''''
class Player():
    
    def __init__(self, x, y, speed, color, border_color, size):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.original_color = color
        self.border_color = border_color
        
        self.size = size
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)
    
    def render(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.size, self.size), int(self.size / 15))
    
    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def up(self):
        self.y = self.y - self.speed

    def down(self):
        self.y = self.y + self.speed
    
    def left(self):
        self.x = self.x - self.speed
    
    def right(self):
        self.x = self.x + self.speed
    # Requires fixing
    def jump(self):
        self.jump_sound.play()
        self.gravity = -7
        self.y += self.gravity
        self.color = "#f5e90a"
        '''
        player.gravity = -9
        player.y += player.gravity
        '''
    def fall(self):
        self.gravity += 0.23 
        self.y += self.gravity
        if self.y >= 420:
            self.y = 420
            self.color = "#ff0000"
        '''
        player.gravity += 0.23
        player.y += player.gravity
        if player.y > 420:
            player.y = 420
        '''
            
class Ledge():
    
    def __init__(self, ledge_width, ledge_height, color, border_color, x_pos, y_pos):
        self.ledge_width = ledge_width
        self.ledge_height = ledge_height
        self.color = color
        self.border_color = border_color
        self.x_pos = x_pos
        self.y_pos = y_pos
    
    def render(self):
        pygame.draw.rect(screen, self.color, (self.x_pos, self.y_pos, self.ledge_width, self.ledge_height))
        pygame.draw.rect(screen, self.border_color, (self.x_pos, self.y_pos, self.ledge_width, self.ledge_height), 2)
    
    def rect(self):
        return pygame.Rect(self.x_pos, self.y_pos, self.ledge_width, self.ledge_height)

def player_jumps_and_falls(player, ledge_list):

    player.fall()
    collision_count = 0
    for ledge in ledge_list:
        if pygame.Rect.colliderect(player.rect(), ledge.rect()):
            collision_count += 1
            player.color = "#ff0000"
            if player.gravity > 0:
                player.y = ledge.y_pos - player.size
                player.gravity = 0
            elif player.gravity <= 0:
                player.y = ledge.y_pos + ledge.ledge_height + 4
                player.gravity = 0.5
            elif player.speed > 0:
                player.x = ledge.x_pos + ledge.ledge_width
            elif player.speed < 0:
                player.x = ledge.x_pos + ledge.ledge_width

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and (collision_count > 0 and player.gravity <= 0 or player.y >= 420):
        player.jump()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.left()
    if keys[pygame.K_RIGHT] and player.x <= 770:
        player.right()
            
def player_ledge_collision(player, ledge):
    collide = pygame.Rect.colliderect(player.rect(), ledge.rect())
    if collide:
        if player.y <= ledge.y_pos + ledge.ledge_height:
            player.y = ledge.y_pos + ledge.ledge_height
        if player.y <= ledge.y_pos:
            player.bottom = ledge.y_pos
        #if player.x + player.size >= ledge.x_pos:
            #player.x = ledge.x_pos - player.size
        #if player.x <= ledge.x_pos + ledge.ledge_width:
            #player.x = ledge.x_pos + ledge.ledge_width

# Intro Screen
            
player_on_intro_screen = Player(300, 200, 4, (255, 0, 0), "#000000", 200)
    
# game objects

player = Player(20, 420, 4, (255, 0, 0), "#000000", 30)
ledge_1 = Ledge(100, 20, "#e8521c", "#000000", 200, 350)
ledge_2 = Ledge(150, 15, "#d9876a", "#000000", 270, 200)
ledge_3 = Ledge(100, 20, "#e8521c", "#000000", 0, 275)
ledge_4 = Ledge(80, 20, "#e8521c", "#000000", 400, 110)
ledge_5 = Ledge(200, 20, "#03fc2c", "#000000", 600, 130)

ledge_list = [ledge_1, ledge_2, ledge_3, ledge_4, ledge_5]

# other game elements

sign = test_font.render(' EXIT ', False, '#000000')
sign_rect = sign.get_rect(topleft = (660, 20))

the_exit = pygame.Surface((100, 80))
the_exit.fill("#24e5f2")
the_exit_rect = the_exit.get_rect(topleft = (645, 50))

# game loop
while True:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit() # ends the game
            exit() # ends the while loop
        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                game_active = True
                beaten_the_level = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q and beaten_the_level == True:
                pygame.quit()
                exit()
                
    if game_active == True:
        screen.fill(background_color)
        screen.blit(ground_surface, (0, 450))
        ledge_1.render()  
        ledge_2.render()
        ledge_3.render()
        ledge_4.render()
        ledge_5.render()
        pygame.draw.rect(screen, "#000000", sign_rect, -1)
        screen.blit(sign, sign_rect)
        screen.blit(the_exit, (645, 50))

        #player.fall()
        #player_ledge_collision(player, ledge_1)
        #player_ledge_collision(player, ledge_2)
        #player_ledge_collision(player, ledge_3)
        #player_ledge_collision(player, ledge_4)
        #player_ledge_collision(player, ledge_5)

        player_jumps_and_falls(player, ledge_list)
        
        player.render()

        if pygame.Rect.colliderect(player.rect(), the_exit_rect):
            game_active = False
            beaten_the_level = True
    else:
        screen.fill("#62e1f5")
        if beaten_the_level == True:
            player.x = 20
            player.y = 420
            screen.blit(finish_level_message, finish_level_message_rect)
            screen.blit(buttowski_pic, buttowski_pic_rect)
            screen.blit(press_c_to_play, press_c_to_play_rect)
            screen.blit(press_q_to_quit, press_q_to_quit_rect)
        else:
            screen.blit(game_name, game_name_rect)
            player_on_intro_screen.render()
            screen.blit(press_to_play, press_to_play_rect)
        
    pygame.display.update()
    clock.tick(144)
    

