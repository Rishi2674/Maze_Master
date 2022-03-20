#import random
#import numpy

class Collision:

    def testCollision(self, cube_size = 0, map = [], x = 0, z = 0):

        wall_x = 0
        wall_z = 0

        row_count = 0
        column_count = 0

        half_cube_size = (cube_size / 2)

        for i in map:

            wall_z = (row_count * (cube_size * -1))

            for j in i:

                if (j == 0):
                    continue

                wall_x = (column_count * (cube_size * -1))

                # Check for collision on the z axis.
                if (z >= (wall_z - half_cube_size)) and (z <= (wall_z + half_cube_size)):
                    if (x >= (wall_x - half_cube_size)) and (x <= (wall_x + half_cube_size)):
                        print('Wall X:', wall_x, 'Z:', wall_z)
                        return True

                column_count += 1

            row_count += 1
            column_count = 0

        return False
