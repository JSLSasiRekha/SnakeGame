import pygame
from pygame.locals import *
import time
import random
from PIL import Image, ImageDraw

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)
class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.fruit_images = ["apple.jpg", "banana.jpg", "grapes.jpg", "orange.jpg", "mango.jpg"]
        self.image = None
        self.x = 120
        self.y = 120
        self.load_image()

    def load_image(self):
        fruit_image_path = random.choice(self.fruit_images)
        image = Image.open("resources/" + fruit_image_path).convert("RGBA")
        image = image.resize((SIZE, SIZE))
        # Remove background (assuming it's white)
        image_data = image.getdata()
        transparent_pixels = [(r, g, b, 0) if r > 200 and g > 200 and b > 200 else (r, g, b, 255) for (r, g, b, a) in image_data]
        image.putdata(transparent_pixels)
        self.image = pygame.image.fromstring(image.tobytes(), image.size, image.mode).convert_alpha()

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.load_image()
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE



class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = Image.open("resources/circular_block.png").convert("RGBA")
        self.direction = 'down'
        self.snake_speed = 0.4  # Initial speed of the snake
        self.default_snake_speed = 0.4

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
       
        speed_factor = self.snake_speed
        print(speed_factor)
        time.sleep(speed_factor)
        self.draw()

    def draw(self):
        for i in range(self.length):
            pygame_surface = pygame.image.fromstring(self.image.tobytes(), self.image.size, self.image.mode).convert_alpha()
            self.parent_screen.blit(pygame_surface, (self.x[i], self.y[i]))

            # Add eyes to the snake's head
            if i == 0:
                eye_position_left = (self.x[i] + SIZE // 6, self.y[i] + SIZE // 4)
                eye_position_right = (self.x[i] + 3 * SIZE // 6, self.y[i] + SIZE // 4)

                # Adjust eye positions based on direction
                if self.direction == 'left':
                    eye_position_left = (self.x[i] + SIZE // 6, self.y[i] + SIZE // 4)
                    eye_position_right = (self.x[i] + 3 * SIZE // 6, self.y[i] + SIZE // 4)
                elif self.direction == 'right':
                    eye_position_left = (self.x[i] + SIZE // 2, self.y[i] + SIZE // 4)
                    eye_position_right = (self.x[i] + 5 * SIZE // 6, self.y[i] + SIZE // 4)
                elif self.direction == 'up':
                    eye_position_left = (self.x[i] + SIZE // 4, self.y[i] + SIZE // 6)
                    eye_position_right = (self.x[i] + 3 * SIZE // 4, self.y[i] + SIZE // 6)
                elif self.direction == 'down':
                    eye_position_left = (self.x[i] + SIZE // 4, self.y[i] + SIZE // 2)
                    eye_position_right = (self.x[i] + 3 * SIZE // 4, self.y[i] + SIZE // 2)

                pygame.draw.circle(self.parent_screen, (0, 0, 0), eye_position_left, SIZE // 15)  # Left eye
                pygame.draw.circle(self.parent_screen, (0, 0, 0), eye_position_right, SIZE // 15)  # Right eye

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    def increase_speed(self):
     # Adjust the threshold as needed
            self.snake_speed -= 0.03

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Codebasics Snake And Apple Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/ding.mp3")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 <= x2 + SIZE:
            if y1 >= y2 and y1 <= y2 + SIZE:
                return True
        return False

    def render_background(self):
         self.surface.fill((255, 255, 255))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                self.play_sound("ding")
                self.snake.increase_length()
                self.snake.increase_speed()
                self.apple.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"

        # snake colliding with the boundaries of the window
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.play_sound('crash')
            raise "Hit the boundary error"

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (0, 0,0))
        self.surface.blit(score, (850, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (0,0,0))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (0,0,0))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.1)

if __name__ == '__main__':
    game = Game()
    game.run()



    
