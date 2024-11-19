from OpenGL.GL import *
from OpenGL.GLU import *
from src.collision import Collision
from src.cube import Cube
from src.generator import Generator
from src.input import Input
from src.map import Map
from src.movement import Movement
from src.plane import Plane
from src.sprite import Sprite
from src.texture import Texture
import argparse
import sdl2
import sdl2.ext

# Constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

# Globals
cube_size = 2.0
collision_padding = 0.25
camera_pos = [-8.0, 0.0, -38.0]
camera_rot = 0.0
rotate_angle = 1

collision = Collision()
input = Input()
movement = Movement()
map = []

# Textures
ceiling_texture = None
floor_texture = None
wall_textures = []
object_textures = []
objects = []

def initGL(Width, Height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def drawScene():
    global camera_pos

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    cube = Cube()
    plane = Plane()
    sprite = Sprite()

    # Set up the current maze view.
    glTranslatef(0.0, 0.0, 0.0)
    glRotatef(camera_rot, 0.0, 1.0, 0.0)
    glTranslatef(camera_pos[0], camera_pos[1], camera_pos[2])

    # Draw floor
    glPushMatrix()
    glTranslatef(0.0, -2.0, 0.0)
    glScalef(30.0, 1.0, 30.0)
    plane.drawplane(floor_texture, 10.0)
    glPopMatrix()

    # Draw ceiling
    glPushMatrix()
    glTranslatef(0.0, 2.0, 0.0)
    glRotatef(180.0, 0.0, 0.0, 1.0)
    glScalef(30.0, 1.0, 30.0)
    plane.drawplane(ceiling_texture, 10.0)
    glPopMatrix()

    # Draw maze and objects
    row_count = 0
    column_count = 0
    objects = []

    for i in map:
        for j in i:
            if 0 < j < 10:
                cube.drawcube(wall_textures[int(j) - 1], 1.0)
            if 9 < j < 20:
                objects.append([column_count, row_count, j])
            glTranslatef(cube_size, 0.0, 0.0)
            column_count += 1

        glTranslatef(-cube_size * column_count, 0.0, cube_size)
        row_count += 1
        column_count = 0

    glTranslatef(0.0, 0.0, -cube_size * row_count)

    # Draw objects
    for obj in objects:
        glPushMatrix()
        glTranslatef(obj[0] * cube_size, 0.0, obj[1] * cube_size)
        glRotatef(90.0, 1.0, 0.0, 0.0)
        glRotatef(camera_rot, 0.0, 0.0, 1.0)
        glScalef(1.0, 0.0, 1.0)
        sprite.drawSprite(object_textures[int(obj[2]) - 10])
        glPopMatrix()

def handleInput(event):
    global input, camera_pos, camera_rot, collision, map, movement, cube_size, collision_padding, rotate_angle

    # Check for key events
    if event.type == sdl2.SDL_KEYDOWN:
        key = event.key.keysym.sym
        
        # Escape key - exit the game
        if key == sdl2.SDLK_ESCAPE:
            return False
        
        # Rotation keys (left/right)
        elif key == sdl2.SDLK_LEFT:
            camera_rot -= rotate_angle
        elif key == sdl2.SDLK_RIGHT:
            camera_rot += rotate_angle

        # Movement keys (forward/backward)
        elif key == sdl2.SDLK_w or key == sdl2.SDLK_s:
            modifier = 1 if key == sdl2.SDLK_w else -1
            intended_pos = movement.getIntendedPosition(camera_rot, camera_pos[0], camera_pos[2], 90, modifier)
            
            # Check for collision before updating position
            intended_x = intended_pos[0]
            intended_z = intended_pos[2]
            
            if not collision.testCollision(cube_size=cube_size, map=map, x=intended_x, z=intended_z, padding=collision_padding):
                camera_pos[0], camera_pos[2] = intended_x, intended_z
        
        # Strafing keys (left/right)
        elif key == sdl2.SDLK_a or key == sdl2.SDLK_d:
            modifier = 1 if key == sdl2.SDLK_a else -1
            intended_pos = movement.getIntendedPosition(camera_rot, camera_pos[0], camera_pos[2], 0, modifier)
            
            # Check for collision before updating position
            intended_x = intended_pos[0]
            intended_z = intended_pos[2]

            if not collision.testCollision(cube_size=cube_size, map=map, x=intended_x, z=intended_z, padding=collision_padding):
                camera_pos[0], camera_pos[2] = intended_x, intended_z

    return True




def main():
    global ceiling_texture, floor_texture, object_textures, map

    # Initialize SDL
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        print("SDL Initialization failed!")
        return

    # Create SDL Window
    window = sdl2.SDL_CreateWindow(
        b"Maze Master",
        sdl2.SDL_WINDOWPOS_CENTERED,
        sdl2.SDL_WINDOWPOS_CENTERED,
        WINDOW_WIDTH,
        WINDOW_HEIGHT,
        sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_MAXIMIZED
    )

    if not window:
        print("SDL Window creation failed!")
        sdl2.SDL_Quit()
        return

    # Create OpenGL Context
    context = sdl2.SDL_GL_CreateContext(window)
    if not context:
        print("Failed to create OpenGL context")
        sdl2.SDL_DestroyWindow(window)
        sdl2.SDL_Quit()
        return

    # Ensure the OpenGL context is active
    sdl2.SDL_GL_MakeCurrent(window, context)
    initGL(WINDOW_WIDTH, WINDOW_HEIGHT)

    # Load Map and Textures
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--map', help='The map to load.')
    args = parser.parse_args()

    if args.map:
        map = Map.loadMap(args.map)
    else:
        generator = Generator()
        map = generator.generateMap(16)

    texture = Texture()
    try:
        ceiling_texture = texture.loadImage('tex/ceiling.png')
        floor_texture = texture.loadImage('tex/floor.png')
        wall_textures.append(texture.loadImage('tex/wall/01.png'))
        wall_textures.append(texture.loadImage('tex/wall/02.png'))
        object_textures.append(texture.loadImage('tex/object/orb.png'))
    except Exception as e:
        print(f"Error loading textures: {e}")
        sdl2.SDL_GL_DeleteContext(context)
        sdl2.SDL_DestroyWindow(window)
        sdl2.SDL_Quit()
        return

    # Main Loop
    running = True
    while running:
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                running = False
            running = handleInput(event)

        drawScene()
        sdl2.SDL_GL_SwapWindow(window)

    # Cleanup
    sdl2.SDL_GL_DeleteContext(context)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()

if __name__ == "__main__":
    main()