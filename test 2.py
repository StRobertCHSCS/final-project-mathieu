"""
-------------------------------------------------------------------------
Name: Finalproject.py

Description: Flappy Bird

Author: Mathieu Li

Date: June
--------------------------------------------------------------------------
"""

import random
import arcade
import os

SPRITE_SCALING = 0.01
SPRITE_SCALING_2 = 0.2

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
SCREEN_TITLE = "FLAPPY BIRD"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 40

MOVEMENT_SPEED = 5


my_button = [250,250, 500, 500]  # x, y, width, height


def on_update(delta_time):
    pass


def on_draw():


    arcade.start_render()
    # Draw in here...
    arcade.draw_xywh_rectangle_filled(my_button[0],
                                      my_button[1],
                                      my_button[2],
                                      my_button[3],
                                      arcade.color.BLACK)


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sprite lists
        self.player_list = None
        self.coin_list = None

        # Set up the player
        self.player_sprite = None
        self.wall_list = None
        self.physics_engine = None
        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite("Image/character.png", 0.05)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 270
        self.player_list.append(self.player_sprite)

        # -- Set up several columns of walls
        for x in range(200, 30000, 200):
            for y in range(0, 601, 300):
                # Randomly skip a box so the player can find a way through
                if random.randrange(10) > 1:
                    wall = arcade.Sprite("Image/tunnel.png", 0.1)
                    wall.center_x = 350
                    wall.center_y = y
                    self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # Set the background color
        arcade.set_background_color(arcade.color.WHITE)

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.wall_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.SPACE:
            self.player_sprite.change_y = MOVEMENT_SPEED


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.SPACE:
            self.player_sprite.change_y = -6


    def update(self, delta_time):
        """ Movement and game logic """

        self.wall_list.change_x -= 1


        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_bndry = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.bottom
            changed = True

        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


def on_mouse_press(x, y, button, modifiers):
    # unpack the button list into readable? variables.
    my_button_x, my_button_y, my_button_w, my_button_h = my_button

    # Need to check all four limits of the button.
    if (x > my_button_x and x < my_button_x + my_button_w and
            y > my_button_y and y < my_button_y + my_button_h):
        window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        window.setup()
        arcade.run()

    else:
        print("not clicked")


def setup():
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "My Arcade Game")
    arcade.set_background_color(arcade.color.WHITE)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw

    window.on_mouse_press = on_mouse_press

    arcade.finish_render()

    arcade.run()


setup()