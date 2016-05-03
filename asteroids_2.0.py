"""

------------------ Rice Rocks (Asteroids) ----------------

How to start and stop the game:

Click the 'play' button at the top left corner of
CodeSkulptor to start the game. A popout window will appear
with a menu. Simply click the menu to begin.

To stop, exit the popout window and click the 'reset'
button (to the right of the folder icon).

Controls:

Use arrow keys to control the ship and spacebar to fire
missiles.

                       thrust
                         ^
                         |
        rotate-left <--- | ---> rotate-right
                    ___________
                   |___shoot___|


Your score will be printed to the right console after each
match. Currently there is not an in game high score label.

NOTE:
    Consider this a beta version of the game. There are
    still some small bugs to fix and the code could be
    cleaned up a bit.

Potential improvements:

- Add max score label
- Create stages with increasing levels of difficulty
- Have rocks break apart into smaller rocks
- Add some enemy AI ships
- Incorporate own artwork

For the curious:
    Feel free to skim over the code and see what's going on.
    If you'd like to change the code up be sure to save
    your work by clicking the floppy disk in the left
    corner of CodeSkulptor and then saving the url somewhere.
    This will NOT affect the version that is presented to you
    from the website.

                        Enjoy
-----------------------------------------------------------

"""

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
game_start = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 60)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image_org = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")
explosion_image_blue1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue.png")
explosion_image_blue2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue2.png")
explosion_image_alpha = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def get_radius(self):
        return self.radius

    def get_pos(self):
        return self.pos

    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        c = 0.1

        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        """
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        if self.pos[0] >= WIDTH:
            self.pos[0] = 0

        elif self.pos[0] <= 0:
            self.pos[0] = WIDTH

        elif self.pos[1] >= HEIGHT:
            self.pos[1] = 0

        elif self.pos[1] <= 0:
            self.pos[1] = HEIGHT
        """

        if self.thrust == True:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * c
            self.vel[1] += acc[1] * c

        self.vel[0] *= 0.99
        self.vel[1] *= 0.99

    def thrust(self, status):
        if status == True:
            self.thrust = status
            ship_thrust_sound.play()
            self.image_center[0] = 135
        else:
            self.thrust = status
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
            self.image_center[0] = 45

    def rotate_right(self, angle_vel):
        self.angle_vel = angle_vel
        self.angle += angle_vel

    def rotate_left(self, angle_vel):
        self.angle_vel = angle_vel
        self.angle -= angle_vel


    def shoot(self, status):
        global missile_group

        # scaling coefficient
        c = 6

        if status == True:
            acc = angle_to_vector(self.angle)

            missile_pos_x = self.pos[0] + (self.radius * math.cos(self.angle))
            missile_pos_y = self.pos[1] + (self.radius * math.sin(self.angle))
            missile_pos = [missile_pos_x, missile_pos_y]


            missile_vel_x = self.vel[0] + (acc[0] * c)
            missile_vel_y = self.vel[1] + (acc[1] * c)
            missile_vel = [missile_vel_x, missile_vel_y]

            missile_group.add(Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound))


# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()


    def get_radius(self):
        return self.radius


    def get_pos(self):
        return self.pos


    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

        if self.animated:
            step = 0
            for frame in range(self.age):
                canvas.draw_image(self.image, [self.image_center[0] + step, self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
                step += 128


    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel

        self.age += 1
        if self.age >= self.lifespan:
            return True
        else:
            return False


    def check_collision(self, other_object):
        d = dist(self.get_pos(), other_object.get_pos())
        r_sum = self.get_radius() + other_object.get_radius()
        if d <= r_sum:
            return True
        else:
            return False


def process_sprite_group(group, canvas):
        for element in set(group):
            if element.update() == False:
                element.draw(canvas)
            else:
                group.discard(element)


def check_group_collisions(group_1, group_2):
    global explosion_group
    collision = False
    for g1_element in set(group_1):
        for g2_element in set(group_2):
            if g2_element.check_collision(g1_element):
                group_2.discard(g2_element)
                group_1.discard(g1_element)
                explosion_group.add(Sprite(g2_element.get_pos(), [0, 0], 0, 0,
                                       explosion_image_org, explosion_info, explosion_sound))
                collision = True
    return collision

def check_indiv_collisions(group, other_object):
    global explosion_group

    collision = False
    for element in set(group):
        if element.check_collision(other_object):
            group.discard(element)
            explosion_group.add(Sprite(other_object.get_pos(), [0, 0], 0, 0,
                                       explosion_image_alpha, explosion_info, explosion_sound))
            explosion_group.add(Sprite(element.get_pos(), [0, 0], 0, 0,
                                       explosion_image_org, explosion_info, explosion_sound))
            other_object.pos = [WIDTH / 2, HEIGHT / 2]
            collision = True

    return collision


def reset():
    global my_ship, score, lives, game_start, rock_group
    print score
    for rock in set(rock_group):
        rock_group.discard(rock)
    my_ship.pos = [WIDTH / 2, HEIGHT / 2]
    score = 0
    lives = 3
    game_start = False

def draw(canvas):
    global time, score, lives, game_start

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)

    #check collisions between objects
    if check_indiv_collisions(rock_group, my_ship) == True:
        lives -= 1

    if check_group_collisions(rock_group, missile_group) == True:
        score += 100

    #draw text
    canvas.draw_text("Score: " + str(score), [550, 50], 32, "White")
    canvas.draw_text("Lives: " + str(lives), [50, 50], 32, "White")

    # update ship and sprites
    my_ship.update()

    #set splash screen
    if game_start == False:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(),
                          [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())

    if lives <= 0:
        reset()


# timer handler that spawns a rock
def rock_spawner():
    #initialize globals
    global rock_group, my_ship

    if game_start:
        #useful values for determining velocity, angular velocity, and position
        vel_values = [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
        upper = 0.1
        lower = -0.1

        vel = [(random.choice(vel_values)),(random.choice(vel_values))]
        angle_vel = random.random() * (upper - lower) + lower
        start_pos = [(random.randint(0, WIDTH)), (random.randint(0, HEIGHT))]

        a_rock = Sprite(start_pos, vel, 0, angle_vel, asteroid_image, asteroid_info)
        d = dist(start_pos, my_ship.get_pos())
        r_sum = (my_ship.get_radius() + a_rock.get_radius())
        if len(rock_group) < 12 and d > r_sum:
            rock_group.add(a_rock)


inputs = {"up":(Ship.thrust,True, False), "left":(Ship.rotate_left, -0.05, 0), "right":(Ship.rotate_right, 0.05, 0), "space":(Ship.shoot, True, False)}

def key_down(key):
        for i,j in inputs.items():
            if key == simplegui.KEY_MAP[i]:
                j[0](my_ship, j[1])

def key_up(key):
        for i,j in inputs.items():
            if key == simplegui.KEY_MAP[i]:
                j[0](my_ship, j[2])

def click(pos):
    global game_start, my_ship
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    splash_width = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    splash_height = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)

    if not game_start and splash_width and splash_height:
        my_ship.pos = [WIDTH / 2, HEIGHT / 2]
        my_ship.vel = [0, 0]
        game_start = True


soundtrack.play()
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

#create a group of rocks
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(2000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()