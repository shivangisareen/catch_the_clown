import pygame, random

#initialize pygame
pygame.init()

#create the display surface
WINDOW_WIDTH = 945
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Catch the Clown")

# Set FPS and clock 
FPS = 60
clock = pygame.time.Clock()

# Set game values 
PLAYER_STARTING_LIVES = 3
CLOWN_STARTING_VELOCITY = 3
CLOWN_ACCELERATION = 1

player_lives = PLAYER_STARTING_LIVES
score = 0
clown_velocity = CLOWN_STARTING_VELOCITY
#keep track of the direction in which the clown is moving
clown_dx = random.choice([-1, 1])
clown_dy = random.choice([-1, 1])


# Set colours 
BLUE = (1, 175, 209)
YELLOW = (248, 231, 28)

# Set fonts 
font = pygame.font.Font("./catch_the_clown/assets/Franxurter.ttf", 32)

# Set text 
title_text = font.render("Catch the Clown", True, BLUE)
title_rect = title_text.get_rect()
title_rect.topleft = (50,10)

score_text = font.render("Score: " + str(score), True, YELLOW)
score_rect = score_text.get_rect()
score_rect.topright = (WINDOW_WIDTH-50, 10)

lives_text = font.render("Lives: "+ str(player_lives), True, YELLOW)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 50, 50)

game_over_text = font.render("Game Over", True, BLUE, YELLOW)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Click Anywhere to Play Again", True, YELLOW, BLUE)
continue_rect = continue_text.get_rect()
continue_rect.centerx = WINDOW_WIDTH//2
continue_rect.centery = WINDOW_HEIGHT//2 + 50

# Set sound and music 
click_sound = pygame.mixer.Sound("./catch_the_clown/assets/click_sound.wav")
miss_sound = pygame.mixer.Sound("./catch_the_clown/assets/miss_sound.wav")
pygame.mixer.music.load("./catch_the_clown/assets/ctc_background_music.wav")

# Set images
background_image = pygame.image.load("./catch_the_clown/assets/background.png")
background_rect = background_image.get_rect()
background_rect.topleft = (0,0)

clown_image = pygame.image.load("./catch_the_clown/assets/clown.png")
clown_rect = clown_image.get_rect()
clown_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

# main game loop
pygame.mixer.music.play(-1, 0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # if a button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]

            # if the clown was clicked
            if clown_rect.collidepoint(mouse_x, mouse_y):
                score += 1
                click_sound.play()
                clown_velocity += CLOWN_ACCELERATION

                # move the clown in a new direction
                previous_dx = clown_dx
                previous_dy = clown_dy
                while previous_dx == clown_dx and previous_dy == clown_dy:
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])

            # we missed the clown
            else:
                player_lives -= 1
                miss_sound.play()



    # move the clown
    clown_rect.x += clown_dx * clown_velocity
    clown_rect.y += clown_dy * clown_velocity
    
    # bounce the clown off the edges of the display
    if clown_rect.left <= 0 or clown_rect.right >= WINDOW_WIDTH:
        clown_dx = clown_dx * -1
    if clown_rect.top <= 0 or clown_rect.bottom >= WINDOW_HEIGHT:
        clown_dy = clown_dy * -1
    

    # clearing the screen
    display_surface.fill((0,0,0))

    # update the HUD
    score_text = font.render("Score: " + str(score), True, YELLOW)
    lives_text = font.render("Lives: "+ str(player_lives), True, YELLOW)

    # check for game over
    if player_lives == 0:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()
        # pause the game until the player clicks and reset the game
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            # does the player want to play again
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player_lives = PLAYER_STARTING_LIVES
                    score = 0

                    clown_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
                    clown_velocity = CLOWN_STARTING_VELOCITY
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])

                    pygame.mixer.music.play(-1, 0)
                    is_paused = False
                
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False


    # blit the background 
    display_surface.blit(background_image, background_rect)

    # blit the HUD
    display_surface.blit(title_text, title_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(lives_text, lives_rect)

    # blit assets
    display_surface.blit(clown_image, clown_rect)

    pygame.display.update()


    clock.tick()


# end the game
pygame.quit()