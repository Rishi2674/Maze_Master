from OpenGL.GL import *
from PIL.Image import open

class Texture:

    def loadImage(self, filename):
        try:
            image = open(filename)
        except IOError as ex:
            print('IOError: failed to open texture file')
            print(ex)
            return -1

        print('Opened image file: size =', image.size, 'format =', image.format)

        textureID = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
        glBindTexture(GL_TEXTURE_2D, textureID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)

        imageData = image.convert('RGBA').tobytes()

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.size[0], image.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, imageData)

        image.close()

        return textureID
