
import numpy

class Map:

    def loadMap(filename):
        try:
            with open('maps/' + filename + '.map') as file:
                # Read map data into an array.
                map_data = numpy.loadtxt(file, delimiter=',')
                
        except IOError as ex:
            print('IOError: failed to open map file')
            print(ex)
            return -1

        print('Opened map file: ', 'maps/' + filename + '.map')

        return map_data
