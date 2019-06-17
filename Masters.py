'''
-----------------------------------------------------------------------------------------------------------------------
Name: FinalProject.py

Description: Tappy Tunnel, a version of the very famous game flappy bird

Author: Mathieu Li

Date: June 2019
-----------------------------------------------------------------------------------------------------------------------
'''

import arcade
import random
import os

class State():
    MAIN_MENU = 1
    PLAYING = 2
    GAME_OVER = 3


# List of different pipe images (Green / Red) (Choose one)
birds = ["Objects" + os.sep + "sprites" + os.sep + "yellowbird-downflap.png"]
# Image of the base floor
ground = "Objects" + os.sep + "sprites" + os.sep + "base.png"
# List of different background images (Day / Night) (Choose one)
play = "Objects" + os.sep + "sprites" + os.sep + "play.png"
background = ["Objects" + os.sep + "sprites" + os.sep + "background-night.png","Objects" + os.sep + "sprites" + os.sep + "neon.jpg"
               ,"Objects" + os.sep + "sprites" + os.sep + "background 1.jpg","Objects" + os.sep + "sprites" + os.sep + "cloudsky.jpg"]
# Dict holding the animation images for different birds colors (Choose one)
pipes = ["Objects" + os.sep + "sprites" + os.sep + "pipe-green.png"]

# Start screen (Tap tap!)
ready = "Objects" + os.sep + "sprites" + os.sep + "presspace.png"
ready_message = "Objects" + os.sep + "sprites" + os.sep + "Readymessage.png"
volume = "Objects" + os.sep + "sprites" + os.sep + "soundup.png"

highscore = "Objects" + os.sep + "sprites" + os.sep + "highscore.png"
# Game over logo
gameover = "Objects" + os.sep + "sprites" + os.sep + "gameover2.png"
# dict mapping sound name to arcade sound object
sounds = {'jump': arcade.load_sound("Objects" + os.sep + "audio" + os.sep + "jump.wav"),
          'die': arcade.load_sound("Objects" + os.sep + "audio" + os.sep + "die.wav"),
          'hit': arcade.load_sound("Objects" + os.sep + "audio" + os.sep + "hit.wav"),
          'point': arcade.load_sound("Objects" + os.sep + "audio" + os.sep + "point.wav"),
          'zombie': arcade.load_sound("Objects" + os.sep + "audio" + os.sep + "pain.wav"),
          'coin': arcade.load_sound("Objects" + os.sep + "audio" + os.sep + "coin.wav")}

SCORE = {
    '0': 'Objects' + os.sep + 'sprites' + os.sep + '0.png',
    '1': 'Objects' + os.sep + 'sprites' + os.sep + '1.png',
    '2': 'Objects' + os.sep + 'sprites' + os.sep + '2.png',
    '3': 'Objects' + os.sep + 'sprites' + os.sep + '3.png',
    '4': 'Objects' + os.sep + 'sprites' + os.sep + '4.png',
    '5': 'Objects' + os.sep + 'sprites' + os.sep + '5.png',
    '6': 'Objects' + os.sep + 'sprites' + os.sep + '6.png',
    '7': 'Objects' + os.sep + 'sprites' + os.sep + '7.png',
    '8': 'Objects' + os.sep + 'sprites' + os.sep + '8.png',
    '9': 'Objects' + os.sep + 'sprites' + os.sep + '9.png',}


bird = random.choice(birds)

# Minimum height for a pipe
min_height = 50
# Minimum gap between two pipes (The gap that a bird can go through)


gap_size = 150

# Minimum height for a pipe

# Minimum gap between two pipes (The gap that a bird can go through)
# MIN_GAP = 100

# How many pixels per jump
JUMP_DY = 60
# How many pixels per frame
JUMP_STEP = 6

# Gravity pixels
Gravity = 2

class Pipes (arcade.AnimatedTimeSprite):

    def __init__(self, center_x, center_y, death_height):
        super().__init__(center_x=center_x, center_y=center_y)
        self.score = 0
        self.textures = []


        self.textures.append(arcade.load_texture(pipes[0], 0, 0, 0, 0, False, False, 0.5))


        self.vel = 0
        self.dy = 0
        self.death_height = death_height
        self.dead = False

    def set_velocity(self, velocity):
        self.vel = velocity

    def update(self, dt=0):
        if self.dead:
            self.angle = -180
            if self.center_y > self.death_height + self.height//2:
                self.center_y -= 4
            return

        if self.vel > 0:
            # self.center_y += (1 - math.cos((JUMP_DY - self.vel) * math.pi)) * JUMP_STEP
            self.center_y += 2
            # self.center_y += self.vel
            # self.vel = 0
            self.vel -= 2
            if self.angle < -50:
                self.angle = -80

        else:
            if self.angle > -90:
                self.angle = -100
            self.center_y -= Gravity

    def jump(self):
        self.vel = JUMP_DY

    def die(self):
        self.dead = True
        arcade.play_sound(sounds['zombie'])

class Bird(arcade.Sprite):

    def __init__(self, image, scale=1):
        """
        Initializer for the pipe object, it's not really correct to call this Pipe since this class is responsible of
        creating two pipes as an obstacle for the bird.
        """
        super().__init__(image, scale)
        # the amount of pixels the pipe move each frame.
        self.horizontal_speed = -1.8
        # Just a boolean to check if the bird passed this pipe successfully.
        self.scored = False

    @classmethod
    def random_bird_obstacle(cls, sprites, height):

        # top_pipe.bottom = random.randrange(bottom_pipe.top + MIN_GAP, height - MIN_HEIGHT)
        bottom_bird = cls(bird)
        bottom_bird.top = random.randrange(sprites['base'].height + min_height, height - gap_size - min_height)
        bottom_bird.left = 288

        top_bird = cls(bird)
        top_bird.angle = 180
        top_bird.left = 288
        top_bird.bottom = bottom_bird.top + gap_size


        return bottom_bird, top_bird

    def update(self):
        # Move each frame in the negative x direction.
        self.center_x += self.horizontal_speed

class Game(arcade.Window):

    def __init__(self, width, height):

        """
        Initializer for the game window, note that we need to call setup() on the game object.
        """
        super().__init__(width, height, title= "Tappy Tunnel!")
        self.background = None
        # Base texture
        self.base = None
        # List of birds, even though we've only one bird, it's better to draw a SpriteList than to draw a Sprite
        self.pipe_list = None
        self.sprites = None
        self.bird_sprites = None
        self.pipe = None
        # Background texture

        # Score texture
        self.score_board = None
        #highscore
        self.highscore = None
        self.new_highscore = None
        # A boolean to check if the user tapped
        self.jump = False
        # initial score
        self.score = None
        # Initial state of the game
        self.state = State.MAIN_MENU
        # The texture for the start and game over screens.
        self.menus = {'start': arcade.load_texture(ready),
                      'ready': arcade.load_texture(ready_message),
                      'gameover': arcade.load_texture(gameover),
                      'play': arcade.load_texture(play),
                      'highscore': arcade.load_texture(highscore),
                      'volume': arcade.load_texture(volume)}

    def setup(self):
        self.highscore = None
        self.score = 0
        self.score_board = arcade.SpriteList()
        self.background = arcade.load_texture(random.choice(background))
        self.base = arcade.load_texture(ground)
        self.bird_sprites = arcade.SpriteList()
        self.pipe_list = arcade.SpriteList()
        # A dict holding sprites of static stuff like background & base
        # A dict holding a reference to the textures
        self.sprites = dict()
        self.sprites['background'] = self.background
        self.sprites['base'] = self.base
        # The bird object itself.
        # The AnimatedTimeSprite makes an animated sprite that animates over time.
        # Create a random pipe (Obstacle) to start with.
        start_bird1 = Bird.random_bird_obstacle(self.sprites, self.height)
        self.bird_sprites.append(start_bird1[0])
        self.bird_sprites.append(start_bird1[1])
        self.pipe = Pipes(55, self.height//2, self.base.height)
        self.pipe_list.append(self.pipe)

    def draw_score_board(self):
        """
        Draws the score board
        """
        self.score_board.draw()

    def draw_background(self):
        """
        Draws the background.
        """
        arcade.draw_texture_rectangle(self.width // 2, self.height // 2, self.background.width, self.background.height,
                                      self.background, 0)

    def draw_base(self):
        """
        Bet you expected what this does. :)
        """
        arcade.draw_texture_rectangle(self.width//2, self.base.height//2, self.base.width, self.base.height, self.base, 0)

    def on_draw(self):

        """
        This is the method called when the drawing time comes.
        """
        # Start rendering and draw all the objects
        arcade.start_render()
        # Calling "draw()" on a SpriteList object will call it on each child in the list.

        # Whatever the state, we need to draw background, then pipes on top, then base, then bird.
        self.draw_background()
        self.bird_sprites.draw()
        self.draw_base()
        self.pipe_list.draw()

        if self.state == State.MAIN_MENU:
            # Show the main menu
            texture = self.menus['start']
            arcade.draw_texture_rectangle(self.width//2, self.height//2 + 50, 250, 50, texture, 0)
            texture = self.menus['ready']
            arcade.draw_texture_rectangle(self.width//2,self.height//2 +100,250,200,texture,0)
            texture = self.menus['volume']
            arcade.draw_texture_rectangle(self.width//2,self.height//2 - 50,100,100,texture,0)

        elif self.state == State.PLAYING:
            # Draw the score board when the player start playing.
            self.draw_score_board()

        elif self.state == State.GAME_OVER:
            # Draw the game over menu if the player lost + draw the score board.
            texture = self.menus['gameover']
            arcade.draw_texture_rectangle(self.width//2, self.height//2 + 50, 200, 100, texture, 0)
            texture = self.menus['play']
            arcade.draw_texture_rectangle(self.width//2, self.height//2 - 100, texture.width, texture.height,texture, 0)

            if self.new_highscore == True:
                texture = self.menus['highscore']
                arcade.draw_texture_rectangle(self.width // 2, self.height // 2 - 50, 100, 200, texture, 0)

            arcade.draw_text("Your score is",self.width//2 - 115,self.height//2 + 175,arcade.color.WHITE,25,200,0,'Calibri')


            self.draw_score_board()

    def on_key_release(self, key, modifiers):

        if key == arcade.key.SPACE and self.state == State.MAIN_MENU:
            # If the game is starting, just change the state and return
            self.state = State.PLAYING
            return
        if key == arcade.key.SPACE:
            self.jump = True

    def on_mouse_press(self, x, y, button, modifiers):

        if self.state == State.GAME_OVER:
            texture = self.menus['play']
            w = self.width//2
            h = self.height//2 - 100
            if w - texture.width//2 <= x <= w + texture.width//2:
                if h - texture.height//2 <= y <= h + texture.height//2:
                    self.setup()
                    self.state = State.MAIN_MENU
                    arcade.play_sound(sounds['coin'])


    def scoreboard(self):

        center = 230
        self.score_board = arcade.SpriteList()

        for num in str(self.score):
            self.score_board.append(arcade.Sprite(SCORE[num], 1, center_x= center , center_y=440))
            center += 24


    def on_update(self, delta_time):

        """
        This is the method called each frame to update objects (Like their position, angle, etc..) before drawing them.
        """
        # print(delta_time)
        # Whatever the state, update the bird animation (as in advance the animation to the next frame)
        self.pipe_list.update_animation()

        if self.state == State.PLAYING:

            # If the player pressed space, let the bird fly higher
            if self.jump:
                arcade.play_sound(sounds['jump'])
                self.pipe.jump()
                self.jump = False

            # Check if bird is too low
            if self.pipe.bottom <= self.base.height:
                if self.pipe.change_y < 0:
                    self.pipe.change_y = 0
                self.pipe.bottom = self.base.height

            # Check if bird is too high
            if self.pipe.top > self.height:
                self.pipe.top = self.height

            new_bird = None

            # Kill pipes that are no longer shown on the screen as they're useless and live in ram and create a new pipe
            # when needed. (If the center_x of the closest pipe to the bird passed the middle of the screen)
            for bird in self.bird_sprites:
                if bird.right <= 0:
                    bird.kill()
                elif len(self.bird_sprites) == 2 and bird.right <= random.randrange(self.width // 2, self.width // 2 + 15):
                    new_bird = Bird.random_bird_obstacle(self.sprites, self.height)

            if new_bird:
                self.bird_sprites.append(new_bird[0])
                self.bird_sprites.append(new_bird[1])

            # This calls "update()" Method on each object in the SpriteList
            self.pipe.update(delta_time)
            self.pipe_list.update()
            self.bird_sprites.update()


            # If the bird passed the center of the pipe safely, count it as a point.
            # Hard coding.. :)
            if self.pipe.center_x >= self.bird_sprites[0].center_x and not self.bird_sprites[0].scored:
                arcade.play_sound(sounds['point'])
                self.score += 1
                # Well, since each "obstacle" is a two pipe system, we gotta count them both as scored.
                self.bird_sprites[0].scored = True
                self.bird_sprites[1].scored = True
                print(self.score)


            # Check if the bird collided with any of the pipes
            hit = arcade.check_for_collision_with_list(self.pipe, self.bird_sprites)

            if any(hit):
                arcade.play_sound(sounds['hit'])

                self.state = State.GAME_OVER
                self.pipe.die()

        elif self.state == State.GAME_OVER:
            # We need to keep updating the bird in the game over scene so it can still "die"
            self.pipe.update()

            self.scoreboard()

def main():
    game = Game(288, 512)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
