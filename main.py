from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import sys
import random

class Cloud:
    MAX_SPEED = 5  # Maximum speed for the clouds

    @classmethod
    def create_clouds(cls, num_clouds, width, height):
        clouds = []
        cloud_spritesheet = pygame.image.load("assets/cloudsheet.png")
        min_cloud_distance = 100  # Minimum distance between clouds

        for _ in range(num_clouds):
            x = random.randint(0, width)  # Random x position
            y = random.randint(0, height // 4)  # Random y position limited to the top quarter

            # Check if the new cloud is too close to any existing cloud
            while any(abs(cloud.x - x) < min_cloud_distance for cloud in clouds):
                x = random.randint(0, width)  # Generate a new x position

            cloud = cls(x, y, height, cloud_spritesheet)
            clouds.append(cloud)

        return clouds

    def __init__(self, x, y, height, sprite_sheet):
        self.x = x
        self.y = y
        self.sprite_sheet = sprite_sheet
        self.frame_count = random.randint(0, 21)  # Randomly pick a cloud frame
        self.frame_delay = 150  # Delay between frame updates in milliseconds
        self.last_frame_time = pygame.time.get_ticks()
        self.speed = (height - y) / height * self.MAX_SPEED / 4  # Speed based on the height of the cloud

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time >= self.frame_delay:
            self.last_frame_time = current_time

        self.x -= self.speed  # Move the cloud from right to left based on its speed

        # Check if the cloud moved off the left side of the screen
        if self.x + self.sprite_sheet.get_width() < 0:
            self.x = 1600  # Respawn on the right side
            self.frame_count = random.randint(0, 21)  # Assign a new random cloud frame
            self.y = random.randint(0, pygame.display.get_surface().get_height() // 4)  # Assign a new random y position

    def render(self, window):
        cloud_frame = (self.frame_count * 32) % self.sprite_sheet.get_width()
        cloud_image = self.sprite_sheet.subsurface(pygame.Rect(cloud_frame, 0, 32, 32))
        cloud_image = pygame.transform.scale(cloud_image, (32 * 6, 32 * 6))  # Scale the cloud image up by 4 times

        window.blit(cloud_image, (self.x, self.y))


class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
        print(f"Added item: {item}")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Removed item: {item}")
        else:
            print(f"Item {item} not found in inventory.")

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Game window dimensions
        self.WIDTH, self.HEIGHT = 1600, 1200
        self.WINDOW_SIZE = (self.WIDTH, self.HEIGHT)
        self.FPS = 60

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0,0,0)

        # Load player spritesheet
        self.player_spritesheet = pygame.image.load("assets/Cat01.png")

        # Load background image
        self.background_image = pygame.image.load("assets/sky.png")
        self.background_image = pygame.transform.scale(self.background_image, (int(self.WIDTH), int(self.HEIGHT)))
        # Player animation constants
        self.SPRITE_SIZE = 64
        self.DOWN_ROW, self.LEFT_ROW, self.RIGHT_ROW, self.UP_ROW, self.DOWNLEFT_ROW, self.DOWNRIGHT_ROW, self.UPLEFT_ROW, self.UPRIGHT_ROW = 0, 1, 2, 3, 4, 5, 6, 7
        self.NUM_FRAMES = 12
        self.SCALE = 2

        # Player animation variables
        self.current_frame = 0
        self.movement_key_pressed = False
        self.current_row = self.DOWN_ROW
        self.player_rect = pygame.Rect(0, 0, self.SPRITE_SIZE, self.SPRITE_SIZE)
        self.player_position = pygame.Vector2(0, 0)

        # Frame delay variables
        self.frame_delay = 150  # Delay between frame updates in milliseconds
        self.last_frame_time = pygame.time.get_ticks()

        # Create the game window
        self.window = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Pokemon-style Game")

        self.clock = pygame.time.Clock()

        # Create an instance of the inventory
        self.inventory = Inventory()

        # Load cloud spritesheet
        self.cloud_spritesheet = pygame.image.load("assets/cloudsheet.png")

        self.clouds = Cloud.create_clouds(10, self.WIDTH, self.HEIGHT)

        # Set up play button
        self.play_button = pygame.Rect(self.WIDTH // 2 - 50, self.HEIGHT // 2 - 25, 100, 50)
        self.playing = False


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.open_inventory()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.play_button.collidepoint(event.pos):
                        self.playing = True

        keys = pygame.key.get_pressed()
        self.movement_key_pressed = False
        new_position = self.player_position.copy()

        move_vector = pygame.Vector2(keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w])
        self.movement_key_pressed = move_vector.length_squared() > 0

        if self.movement_key_pressed:
            move_vector.scale_to_length(6) # Increase Speed
            new_position += move_vector

        if move_vector.x < 0:
            if move_vector.y < 0:
                self.current_row = self.UPLEFT_ROW
            elif move_vector.y > 0:
                self.current_row = self.DOWNLEFT_ROW
            else:
                self.current_row = self.LEFT_ROW
        elif move_vector.x > 0:
            if move_vector.y < 0:
                self.current_row = self.UPRIGHT_ROW
            elif move_vector.y > 0:
                self.current_row = self.DOWNRIGHT_ROW
            else:
                self.current_row = self.RIGHT_ROW
        elif move_vector.y < 0:
            self.current_row = self.UP_ROW
        elif move_vector.y > 0:
            self.current_row = self.DOWN_ROW

        if self.movement_key_pressed:
            self.player_position = new_position

    def open_inventory(self):
        print("Opening inventory...")
        # Perform actions related to the inventory, such as displaying it on the screen

        # Example: Adding an item to the inventory
        self.inventory.add_item("Potion")

    def update(self):
        if not self.playing:
            # Update the clouds
            for cloud in self.clouds:
                cloud.update()
        else:

            # Wrap player position around the screen
            self.player_position.x = self.player_position.x % self.WIDTH
            self.player_position.y = self.player_position.y % self.HEIGHT

            # Update the player rectangle position
            self.player_rect.topleft = self.player_position

            # Check if enough time has passed for the next frame update
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time >= self.frame_delay:
                self.last_frame_time = current_time
                self.current_frame = (self.current_frame + 1) % self.NUM_FRAMES

            if not self.movement_key_pressed:
                self.current_frame = 0  # When the player is idle, keep the first frame of the row

            # Update the clouds
            for cloud in self.clouds:
                cloud.update()

            # Create new clouds if necessary
            if len(self.clouds) < 10:
                x = random.randint(self.WIDTH, self.WIDTH + 500)  # Random x position outside the screen
                y = random.randint(0, self.HEIGHT // 4)  # Random y position limited to the top quarter

                cloud = Cloud(x, y, self.HEIGHT, self.cloud_spritesheet)

                self.clouds.append(cloud)

            # Remove clouds that moved off the screen
            self.clouds = [cloud for cloud in self.clouds if cloud.x + cloud.sprite_sheet.get_width() > 0]

    def draw(self):
        # Draw the background image
        self.window.blit(self.background_image, (0, 0))

        if not self.playing:
            # Draw play button
            pygame.draw.rect(self.window, self.WHITE, self.play_button)
            button_font = pygame.font.SysFont(None, 30)
            button_text = button_font.render("Play", True, self.BLACK)
            button_text_rect = button_text.get_rect(center=self.play_button.center)
            self.window.blit(button_text, button_text_rect)
            # Render the clouds
            for cloud in self.clouds:
                cloud.render(self.window)
            pygame.display.flip()
            return

        # Calculate the position of the player sprite in the spritesheet
        player_x = self.current_frame * self.SPRITE_SIZE
        player_y = self.current_row * self.SPRITE_SIZE

        # Make sure the subsurface rectangle is within the dimensions of the spritesheet
        player_x = player_x % self.player_spritesheet.get_width()
        player_y = player_y % self.player_spritesheet.get_height()

        # Get the player sprite from the spritesheet
        player_image = self.player_spritesheet.subsurface(pygame.Rect(player_x, player_y, self.SPRITE_SIZE, self.SPRITE_SIZE))

        # Scale the player sprite to the desired render size
        scaled_player_image = pygame.transform.scale(player_image, (self.SPRITE_SIZE * self.SCALE, self.SPRITE_SIZE * self.SCALE))

        # Calculate the position to render the scaled player sprite
        scaled_player_rect = scaled_player_image.get_rect()
        scaled_player_rect.center = self.player_rect.center

        # Render the scaled player sprite onto the game window
        self.window.blit(scaled_player_image, scaled_player_rect)

        # Update the display
        pygame.display.flip()


    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
