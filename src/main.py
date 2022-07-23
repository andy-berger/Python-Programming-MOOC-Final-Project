import pygame
from random import randint

class Game:
    def __init__(self):
        pygame.init()
        
        self.width = 640
        self.height = 480
        
        self.window = pygame.display.set_mode((self.width, self.height))
       
        pygame.display.set_caption("Coin Collect Game!")

        self.doorPic = pygame.image.load("door.png")
        self.doorLeft = Object(0, self.height - self.doorPic.get_height(), self.doorPic)
        self.doorRight = Object(self.width - self.doorPic.get_width(), self.height - self.doorPic.get_height(), self.doorPic)

        self.robotPic = pygame.image.load("robot.png")
        self.robot = Object(self.width / 2 - self.robotPic.get_width() / 2, self.height - self.robotPic.get_height(), self.robotPic)

        self.coinPic = pygame.image.load("coin.png")
        self.coin = Object(0, 0, self.coinPic)

        self.monsterPic = pygame.image.load("monster.png")
        self.monster = Object(0, 0, self.monsterPic)

        self.robot_to_right = False
        self.robot_to_left = False

        self.coin_number = 5
        self.coin_positions = []
        for i in range(self.coin_number):
            self.coin_positions.append([randint(0 + self.doorPic.get_width(), self.width - self.coinPic.get_width()) - self.doorPic.get_width(), -randint(100,1000)])
        
        self.monster_number = 3
        self.monster_positions = []
        for i in range(self.monster_number):
            self.monster_positions.append([randint(0 + self.doorPic.get_width(), self.width - self.monsterPic.get_width()) - self.doorPic.get_width(), -randint(100,1000)])

        self.coins_collected = 0
        self.coins_lost = 0

        self.bullets = []

        self.clock = pygame.time.Clock()

        self.bigfont = pygame.font.SysFont("Arial", 24)

        self.smallfont = pygame.font.SysFont("Arial", 12)
       
        self.main_loop()
    
    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.robot_to_left = True
                if event.key == pygame.K_RIGHT:
                    self.robot_to_right = True
                if event.key == pygame.K_SPACE and len(self.bullets) < 3:
                    self.bullet = pygame.Rect(int(self.robot.x + (self.robotPic.get_width() - 5) / 2), int(self.robot.y), 5, 10)
                    self.bullets.append(self.bullet)
        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.robot_to_left = False
                if event.key == pygame.K_RIGHT:
                    self.robot_to_right = False        

            if event.type == pygame.QUIT:
                exit()
        
        if self.robot_to_right:
            self.robot_move_right()
        if self.robot_to_left:
            self.robot_move_left()
        
        self.clock.tick(60)
    
    def draw_window(self):
        self.window.fill((123, 123, 123))
        self.draw_doors()
        self.draw_robot()
        self.coin_rain()
        self.monster_rain()
        self.handle_bullets()
        self.draw_text()

        pygame.display.flip()
    
    def draw_doors(self):
        self.window.blit(self.doorPic, (self.doorLeft.x, self.doorLeft.y))
        self.window.blit(self.doorPic, (self.doorRight.x, self.doorRight.y))

    def draw_robot(self):
        self.window.blit(self.robot.image, (int(self.robot.x), int(self.robot.y)))
        
    def coin_rain(self):
        for i in range(self.coin_number):
            self.coin_positions[i][1] += 1
            if self.coin_positions[i][1] + self.coinPic.get_height() >= self.height:
                # game ends
                self.draw_game_over()
                exit()
            if self.coin_positions[i][1] + self.coinPic.get_height() >= self.robot.y:
                robot_middle = self.robot.x + self.robotPic.get_width() / 2
                coin_middle = self.coin_positions[i][0] + self.coinPic.get_width() / 2
                if abs(robot_middle - coin_middle) <= (self.robotPic.get_width() + self.coinPic.get_width()) / 2:
                    # the robot caught a coin
                    self.coin_positions[i][0] = randint(0 + self.doorPic.get_width(), self.width - self.coinPic.get_width() - self.doorPic.get_width())
                    self.coin_positions[i][1] = -randint(100,1000)
                    self.coins_collected += 1
        
        for i in range(self.coin_number):
            self.window.blit(self.coin.image, (self.coin_positions[i][0], self.coin_positions[i][1]))
    
    def monster_rain(self):
        for i in range(self.monster_number):
            self.monster_positions[i][1] += 1
            if self.monster_positions[i][1] + self.monsterPic.get_height() >= self.robot.y:
                robot_middle = self.robot.x + self.robotPic.get_width() / 2
                monster_middle = self.monster_positions[i][0] + self.monsterPic.get_width() / 2
                if abs(robot_middle - monster_middle) <= (self.robotPic.get_width() + self.monsterPic.get_width()) / 2:
                    # a monster caught the robot
                    self.monster_positions[i][0] = randint(0 + self.doorPic.get_width(), self.width - self.monsterPic.get_width() - self.doorPic.get_width())
                    self.monster_positions[i][1] = -randint(100,1000)
                    if not self.coins_collected <= 0:
                        self.coins_collected -= 1
                        self.coins_lost += 1
        
        for i in range(self.monster_number):
            self.window.blit(self.monster.image, (self.monster_positions[i][0], self.monster_positions[i][1]))

    def robot_move_left(self):
        if not self.robot.x <= 0 + self.doorPic.get_width() / 4:
            self.robot.x -= 3
        # if entering left door, appear at the right side:
        else:
            self.robot.x = self.width - self.doorPic.get_width() - self.robotPic.get_width() / 4
    
    def robot_move_right(self):
        if not self.robot.x >= self.width - self.doorPic.get_width() - self.robotPic.get_width() / 4:
            self.robot.x += 3
        # if entering right door, appear at the left side:
        else:
            self.robot.x = 0 + self.robotPic.get_width() / 4
    
    def handle_bullets(self):
        for bullet in self.bullets:
            pygame.draw.rect(self.window, (255, 255, 0), bullet)
            bullet.y -= 7
            for monster in self.monster_positions:
                if bullet.x >= monster[0] and bullet.x <= monster[0] + self.monsterPic.get_width():
                    if bullet.y >= monster[1] and bullet.y <= monster[1] + self.monsterPic.get_height():
                        self.bullets.remove(bullet)
                        monster[1] -= self.height

            if bullet.y <= 0:
                self.bullets.remove(bullet)
    
    def draw_text(self):
        self.text_bigfont_color = (240, 94, 35)
        self.text_smallfont_color = (0, 0, 0)
        self.text_top_left1 = self.bigfont.render(f"Coins collected: {self.coins_collected}", True, self.text_bigfont_color)
        self.text_top_left2 = self.bigfont.render(f"Coins lost: {self.coins_lost}", True, self.text_bigfont_color)
        self.text_top_right1 = self.smallfont.render("Controls:", True, self.text_smallfont_color)
        self.text_top_right2 = self.smallfont.render("LEFT ARROW = Left", True, self.text_smallfont_color)
        self.text_top_right3 = self.smallfont.render("RIGHT ARROW = Right", True, self.text_smallfont_color)
        self.text_top_right4 = self.smallfont.render("SPACE = Shoot", True, self.text_smallfont_color)
        self.window.blit(self.text_top_left1, (10, 10))
        self.window.blit(self.text_top_left2, (10, 40))
        self.window.blit(self.text_top_right1, (500, 10))
        self.window.blit(self.text_top_right2, (500, 25))
        self.window.blit(self.text_top_right3, (500, 40))
        self.window.blit(self.text_top_right4, (500, 55))
    
    def draw_game_over(self):
        self.text_bigfont_color = (255, 0, 0)
        self.text_game_over = self.bigfont.render("GAME OVER", True, self.text_bigfont_color)
        self.window.blit(self.text_game_over, (self.width / 2 - self.text_game_over.get_width() / 2, self.height / 2 - self.text_game_over.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(5000)

class Object():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

if __name__ == "__main__":
    Game()