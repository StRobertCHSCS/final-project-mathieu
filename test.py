"""
----------------------------------------------------------------------------------
Name: Finalproject.py

Description: Flappy bird

Author: Mathieu Li

Date: June 2019
----------------------------------------------------------------------------------
"""
import random
import arcade

#Screen Height and Width
WIDTH = 300
HEIGHT = 480

player_x = WIDTH/2
player_y = HEIGHT/2

# Variables to record if certain keys are being pressed.
up_pressed = False
down_pressed = False
left_pressed = False
right_pressed = False
up_released = False

my_button = [150,240, 150, 50]  # x, y, width, height

angle = 0

# first set up empty lists
tunnelx_positions = []
tunnely_positions = []

tunnel_x_positions = []
tunnel_y_positions = []

#menu box


def on_draw_2():

    arcade.start_render()

    # Draw in here...
    arcade.draw_xywh_rectangle_filled(my_button[0],
                                      my_button[1],
                                      my_button[2],
                                      my_button[3],
                                      arcade.color.WHITE)

#for loop to generate random y values
for _ in range(0, 100, 30):
    y = random.randrange(-50,0)

for x in range(0,50,50):
    tunnel_x_positions.append(x)
    tunnel_y_positions.append(y)

# loop 100 times
for _ in range(0, 200, 30):
    # generate random x and y values
    y = random.randrange(HEIGHT, HEIGHT + 50)

for x in range(0,50,50):
    # append the x and y values to the appropriate list
    tunnelx_positions.append(x)
    tunnely_positions.append(y)


def main():
    window = arcade.get_window()


    window.on_draw = on_draw
    arcade.schedule(update, 1 / 60)
    # Override arcade window methods


    window.on_key_press = on_key_press
    window.on_key_release = on_key_release

    arcade.run()

#moving obstacles and player
def update(delta_time):
    for index in range(len(tunnelx_positions)):
        tunnelx_positions[index] -= 3

        if tunnelx_positions[index] < 0:
            tunnely_positions[index] = random.randrange(HEIGHT, HEIGHT + 70,50)
            tunnelx_positions[index] = WIDTH + 35

    for index in range(len(tunnel_x_positions)):
        tunnel_x_positions[index] -= 3

        if tunnel_x_positions[index] < 0:
            tunnel_y_positions[index] = random.randrange(-70,50,50)
            tunnel_x_positions[index] = WIDTH + 35

    global up_pressed, player_y, player_x,down_pressed,right_pressed,left_pressed,up_released
    if up_pressed:
        player_y += 8
    if up_released:
        player_y -= 2.5
    if down_pressed:
        player_y -= 5
    if right_pressed:
        player_x += 5
    if left_pressed:
        player_x -= 5
    if player_y >= HEIGHT:
        player_y = HEIGHT
    if player_y <= 0:
        player_y = 0


# draw objects on screen
def on_draw():
    arcade.start_render()


    texture_3 = arcade.load_texture("Image/background.jpg")
    arcade.draw_texture_rectangle(150, 230, WIDTH, HEIGHT+50, texture_3)
    # Draw in here...
    for x, y in zip(tunnelx_positions, tunnely_positions):
        texture = arcade.load_texture("Image/tunneldown.png")
        arcade.draw_texture_rectangle(x,y,30,400,texture)

    for x, y in zip(tunnel_x_positions, tunnel_y_positions):
        texture = arcade.load_texture("Image/tunnelup.png")
        arcade.draw_texture_rectangle(x, y, 30, 400, texture)


    global player_x, player_y
    texture_2 = arcade.load_texture("Image/character.png")
    arcade.draw_texture_rectangle(player_x, player_y, 25, 25, texture_2,angle)

    if player_y <= 0 or player_y >= HEIGHT:
        arcade.draw_text("GAME OVER",120,420,arcade.color.WHITE,20)


# Key press on keyboard to move player around
def on_key_press(key, modifiers):
    global up_pressed,down_pressed,right_pressed,left_pressed,angle
    if key == arcade.key.SPACE:
        up_pressed = True
        angle = 0
    if key == arcade.key.S:
        down_pressed = True
    if key == arcade.key.D:
        right_pressed = True
    if key == arcade.key.A:
        left_pressed = True


def on_key_release(key, modifiers):
    global up_pressed,down_pressed,right_pressed,left_pressed,up_released,angle
    if key == arcade.key.SPACE:
        up_pressed = False
        up_released = True
        angle -= 30
    if key == arcade.key.S:
        down_pressed = False
    if key == arcade.key.D:
        right_pressed = False
    if key == arcade.key.A:
        left_pressed = False


#mouse press to start the game
def on_mouse_press(x, y, button, modifiers):

    # unpack the button list into readable? variables.
    my_button_x, my_button_y, my_button_w, my_button_h = my_button

    # Need to check all four limits of the button.
    if (x > my_button_x and x < my_button_x + my_button_w and
            y > my_button_y and y < my_button_y + my_button_h):
        main()
    else:
        main()

def setup():
    arcade.open_window(WIDTH, HEIGHT, "FLAPPY BIRD")
    arcade.set_background_color(arcade.color.WHITE)
    window = arcade.get_window()

    window.on_mouse_press = on_mouse_press

    arcade.run()

if __name__ == '__main__':
    setup()

