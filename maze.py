from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from src.collision import Collision
from src.cube import Cube
from src.generator import Generator
from src.input import Input
from src.movement import Movement
from src.plane import Plane
from src.sprite import Sprite
from src.texture import Texture

window = 0

# Size of cubes used to create wall segments.
cube_size = 2
# Space around cubes to extend hitbox (prevents peeking through walls).
collision_padding = 0.5
# Initial camera position after map is drawn.
camera_pos = [-8.0, 0.0, -38.0]
# camerapos = [0.0, 0.0, 0.0]
# Initial camera rotation.
camera_rot = 0.0
# The angle in degrees the camera rotates each turn.
rotate_angle = 1

first_run = False

collision = Collision()
input = Input()
movement = Movement()

map = []

# Loaded textures.
ceiling_texture = None
floor_texture = None
orb_texture = None
wall_texture = None

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

    global camera_pos, first_run

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    cube = Cube()
    plane = Plane()
    sprite = Sprite()

    # Set up the current maze view.
    # Reset position to zero, rotate around y-axis, restore position.
    glTranslatef(0.0, 0.0, 0.0)
    glRotatef(camera_rot, 0.0, 1.0, 0.0)
    glTranslatef(camera_pos[0], camera_pos[1], camera_pos[2])

    # Draw floor.
    glPushMatrix()
    glTranslatef(0.0, -2.0, 0.0)
    glScalef(30.0, 1.0, 30.0)
    plane.drawplane(floor_texture, 10.0)
    glPopMatrix()

    # Draw ceiling.
    glPushMatrix()
    glTranslatef(0.0, 2.0, 0.0)
    glRotatef(180.0, 0.0, 0.0, 1.0)
    glScalef(30.0, 1.0, 30.0)
    plane.drawplane(ceiling_texture, 10.0)
    glPopMatrix()

    # Draw test sprite.
    glPushMatrix()
    glTranslatef(0.0, 0.5, -6.0)
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glRotatef(camera_rot, 0.0, 0.0, 1.0)
    glScalef(1.0, 0.0, 1.0)
    sprite.drawSprite(orb_texture)
    glPopMatrix()

    # Build the maze like a printer; back to front, left to right.
    row_count = 0
    column_count = 0

    wall_x = 0.0
    wall_z = 0.0

    for i in map:

        wall_z = (row_count * (cube_size * -1))

        for j in i:

            # 1 = cube, 0 = empty space.
            if (j == 1):
                cube.drawcube(wall_texture, 1.0)

                wall_x = (column_count * (cube_size * -1))

                if (first_run != True):
                    print('Drawing cube at X:', wall_x, 'Z:', wall_z)

            # Move from left to right one cube size.
            glTranslatef(cube_size, 0.0, 0.0)

            column_count += 1

        # Reset position before starting next row, while moving
        # one cube size towards the camera.
        glTranslatef(((cube_size * column_count) * -1), 0.0, cube_size)

        row_count += 1
        # Reset the column count; this is a new row.
        column_count = 0

    glutSwapBuffers()

    handleInput()

    if (first_run != True):
        first_run = True

def handleInput():

    global input, camera_pos, camera_rot

    if input.isKeyDown(Input.KEY_STATE_ESCAPE):
        sys.exit()

    if input.isKeyDown(Input.KEY_STATE_LEFT):
        camera_rot -= rotate_angle

    if input.isKeyDown(Input.KEY_STATE_RIGHT):
        camera_rot += rotate_angle

    intended_pos = [camera_pos[0], 0, camera_pos[2]]

    if input.isKeyDown(Input.KEY_STATE_FORWARD) or input.isKeyDown(Input.KEY_STATE_BACK):
        modifier = 1 if input.isKeyDown(Input.KEY_STATE_FORWARD) else -1
        intended_pos = movement.getIntendedPosition(camera_rot, camera_pos[0], camera_pos[2], 90, modifier)

    if input.isKeyDown(Input.KEY_STATE_LEFT_STRAFE) or input.isKeyDown(Input.KEY_STATE_RIGHT_STRAFE):
        modifier = 1 if input.isKeyDown(Input.KEY_STATE_LEFT_STRAFE) else -1
        intended_pos = movement.getIntendedPosition(camera_rot, camera_pos[0], camera_pos[2], 0, modifier)

    intended_x = intended_pos[0]
    intended_z = intended_pos[2]

    # Detect collision with walls.
    if (collision.testCollision(cube_size, map, intended_x, intended_z, collision_padding)):
        print('Collision at X:', intended_x, 'Z:', intended_z)

        # If it's possible to keep the user moving by sliding along the wall, do so.
        slide_time = False
        if (collision.testCollision(cube_size, map, intended_x, camera_pos[2], collision_padding) == False):
            intended_z = camera_pos[2]
            slide_time = True
        elif (collision.testCollision(cube_size, map, camera_pos[0], intended_z, collision_padding) == False):
            intended_x = camera_pos[0]
            slide_time = True

        if (slide_time):
            # Slide the camera along the wall.
            camera_pos[0] = intended_x
            camera_pos[2] = intended_z
    else:
        # Move the camera to the user's intended position.
        camera_pos[0] = intended_x
        camera_pos[2] = intended_z

def main():

    global window, ceiling_texture, floor_texture, orb_texture, wall_texture, map

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(1024, 768)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow('Experimental Maze')

    # Generate map.
    generator = Generator()
    map = generator.generateMap(16)

    # Represents a top-down view of the maze.
    # map = [
    #     [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    #     [1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1],
    #     [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    #     [1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1],
    #     [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    #     [1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1],
    #     [1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1],
    #     [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    #     [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    #     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #     [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
    #     [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
    #     [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1]
    # ]

    # Load texture.
    texture = Texture()

    ceiling_texture = texture.loadImage('tex/ceiling.png')
    floor_texture = texture.loadImage('tex/floor.png')
    orb_texture = texture.loadImage('tex/orb.png')
    wall_texture = texture.loadImage('tex/wall.png')

    glutIgnoreKeyRepeat(1)
    glutKeyboardFunc(input.registerKeyDown)
    glutKeyboardUpFunc(input.registerKeyUp)

    glutDisplayFunc(drawScene)
    glutIdleFunc(drawScene)
    initGL(1024, 768)
    glutMainLoop()

if __name__ == "__main__":

    main()
