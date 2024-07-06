from OpenGL.GL import *

class Sprite:

    def drawSprite(self, texture_id = None):

        if texture_id is not None:
            glEnable(GL_TEXTURE_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
            glBindTexture(GL_TEXTURE_2D, texture_id)

            # Enable alpha blending for transparency.
            glEnable(GL_BLEND)
            glDepthMask(GL_FALSE)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE)

            glBegin(GL_QUADS)

            # Textured plane.
            glTexCoord2f(0.0, 0.0); glVertex3f(1.0, 1.0,-1.0)
            glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, 1.0,-1.0)
            glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, 1.0, 1.0)
            glTexCoord2f(0.0, 1.0); glVertex3f(1.0, 1.0, 1.0)

            glEnd()

            glDisable(GL_TEXTURE_2D)
            glDisable(GL_BLEND)
            glDepthMask(GL_TRUE)
