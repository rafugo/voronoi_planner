# generates random graphs with a given probability of 
# a space being an object

import random as r

class GraphGenerator:

    # p is the probablity that a spot is an obstacle
    def __init__(self, rows, cols, p, filename):
        f = open(filename, "w")

        line = ''
        for j in range(cols):
            line += '1 '
        line = line[:-1]
        f.write(line + '\n')

        for i in range(rows-2):
            line = '1 '
            for j in range(cols-2):
                if r.random() < p:
                    line += '1 '

                else:
                    line += '0 '

            line += '1'
            f.write(line + '\n')

        line = ''
        for j in range(cols):
            line += '1 '
        line = line[:-1]
        f.write(line + '\n')




