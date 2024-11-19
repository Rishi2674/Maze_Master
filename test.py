
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sdl2
import sdl2.ext

def test():
    sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
    window = sdl2.SDL_CreateWindow(b"Test SDL2 + OpenGL", 100, 100, 800, 600, sdl2.SDL_WINDOW_OPENGL)
    context = sdl2.SDL_GL_CreateContext(window)

    glClearColor(0.0, 1.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    sdl2.SDL_GL_SwapWindow(window)

    sdl2.SDL_Delay(5000)
    sdl2.SDL_GL_DeleteContext(context)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()

test()
