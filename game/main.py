# Crimson Sane
# Ping pong written using pygame

import pygame

SCREEN_SIZE = (1600,900)
PY_CLOCK = pygame.time.Clock()
FPS = 30
BALL_SPD = 15
BALL_SIZE = (25,25)
HITTER_SPD = 50
HITTER_SIZE = (15, 105)
BACKGROUND_COLOR = (0,0,0) #(61,80,33) Really nice green color
OBJECT_COLOR = (255,255,255)

pygame.init()
pygame.font.init()
FONT = pygame.font.Font('Pixeled.ttf', 24)
display = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
pygame.display.set_caption("Pyng Pong")

class Ball():
    def __init__(self, size, pos, spd):
        self.dir = [1,1]
        self.pos = pos
        self.x, self.y = pos
        self.size = size
        self.w, self.h = size
        self.spd = spd
        
        self.rect = pygame.Rect(pos, size)
        
    def update(self):
        self.rect.move_ip(self.dir[0]*self.spd, self.dir[1]*self.spd)
        self.x = self.rect.x
        self.y = self.rect.y
    
    def bounce(self, direction):
        if direction[0] >= 1:
            self.dir[0] = -1
        elif direction[0] <= -1:
            self.dir[0] = 1
        
        if direction[1] >= 1:
            self.dir[1] = -1
        elif direction[1] <= -1:
            self.dir[1] = 1
    
    def reset(self, pos):
        self.rect = pygame.Rect(pos, self.size)
    
    def draw(self, surface):
        pygame.draw.rect(surface, OBJECT_COLOR, self.rect)

class Hitter():
    def __init__(self, size, pos, spd, ball, player_id=1):
        self.player_id = player_id
        self.ball = ball
        self.pos = pos
        self.x, self.y = pos
        self.size = size
        self.w, self.h = size
        self.spd = spd
        
        self.rect = pygame.Rect(pos, size)
        
    def update(self, player_input):
        if self.player_id == 1:
            if "UP_1" in player_input and self.y > 0:
                self.rect.move_ip(0, -self.spd)
            if "DOWN_1" in player_input and self.y < (SCREEN_SIZE[1] - self.h):
                self.rect.move_ip(0, self.spd)
        if self.player_id == 2:
            if "UP_2" in player_input and self.y > 0:
                self.rect.move_ip(0, -self.spd)
            if "DOWN_2" in player_input and self.y < (SCREEN_SIZE[1] - self.h):
                self.rect.move_ip(0, self.spd)
        
        ball_x2 = self.ball.x + self.ball.w
        ball_y2 = self.ball.y + self.ball.h
        
        self_x2 = self.x + self.w
        self_y2 = self.y + self.h
        
        """
self(x,y)______                   ball x must be less than self x2
   ball(x,y) __|_                 AND 
        |   |    |                ball x2 must be greater than self x
        |   |    |                AND
        |___|____| <-ball(x2,y2)  ball 
               ^
               |
        self(x2,y2)
        """
        
        if self.rect.colliderect(self.ball.rect):
            self.ball.bounce((self.x - self.ball.x, (self.y + self.w)/2 - self.ball.y))
        
        self.x = self.rect.x
        self.y = self.rect.y
    
    def draw(self, surface):
        pygame.draw.rect(surface, OBJECT_COLOR, self.rect)

def get_user_keys():
    """Gets the user's input"""
    key_butn = ''
    
    for event in pygame.event.get():
        # Allows the user to close the game
        if event.type == pygame.QUIT:
            print("User quit the game.")
            key_butn = "QUIT"
    
    if pygame.key.get_pressed()[pygame.K_ESCAPE]: key_butn += "QUIT"
    if pygame.key.get_pressed()[pygame.K_w]: key_butn += "UP_1"
    if pygame.key.get_pressed()[pygame.K_s]: key_butn += "DOWN_1"
    if pygame.key.get_pressed()[pygame.K_UP]: key_butn += "UP_2"
    if pygame.key.get_pressed()[pygame.K_DOWN]: key_butn += "DOWN_2"
    
    return key_butn

def draw_dash_lines():
    """Draws dash lines"""
    for i in range(0, SCREEN_SIZE[1], 25):
        SIZE = 10
        start_point = (SCREEN_SIZE[0] // 2, 0+i)
        end_point = (SCREEN_SIZE[0] // 2, SIZE+i)
        pygame.draw.line(display, OBJECT_COLOR, start_point, end_point, 5)

def main():
    """Main function"""
    run = True
    
    DEFAULT_BALL_POS = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
    
    ball = Ball(BALL_SIZE, DEFAULT_BALL_POS, BALL_SPD)
    hitter_plyer1 = Hitter(HITTER_SIZE, (HITTER_SIZE[0], SCREEN_SIZE[1] / 2), HITTER_SPD, ball)
    hitter_plyer2 = Hitter(HITTER_SIZE, (SCREEN_SIZE[0] - (HITTER_SIZE[0] * 2), SCREEN_SIZE[1] / 2), HITTER_SPD, ball, player_id=2)
    scores = {1:0, 2:0}
    
    # Game loop
    while run:
        pygame.display.update()
        PY_CLOCK.tick(FPS)
        
        # Get the user input
        user_keys = get_user_keys()
        
        ball.update()
        hitter_plyer1.update(user_keys)
        hitter_plyer2.update(user_keys)
        plyer1_score = FONT.render(str(scores[1]), False, OBJECT_COLOR)
        plyer2_score = FONT.render(str(scores[2]), False, OBJECT_COLOR)
        
        # If ball hits the top or bottom screen
        if ball.y > (SCREEN_SIZE[1] - ball.h) or ball.y < 0:
            ball.bounce((0,ball.y))
        
        # If ball reaches past player two's zone
        if ball.x > SCREEN_SIZE[0]:
            scores[1] += 1
            ball.reset(DEFAULT_BALL_POS)
            ball.dir[0] = 1
        
        # If ball reaches past player one's zone
        elif ball.x < -ball.w:
            scores[2] += 1
            ball.reset(DEFAULT_BALL_POS)
            ball.dir[0] = -1
        
        # Drawing
        display.fill(BACKGROUND_COLOR)
        draw_dash_lines()
        display.blit(plyer1_score, plyer1_score.get_rect(midright = ((SCREEN_SIZE[0] // 2)-5,50)))
        display.blit(plyer2_score, plyer2_score.get_rect(midleft = ((SCREEN_SIZE[0] // 2)+10,50)))
        ball.draw(display)
        hitter_plyer1.draw(display)
        hitter_plyer2.draw(display)
        
        # Do something with the key presses
        if "QUIT" in user_keys:
            run = False
    
    pygame.quit()

if __name__ == "__main__":
    main()