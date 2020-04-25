from random import *
import math
import numpy as np
import matplotlib.pyplot as plt
import time


def displayTour(tour):
    plt.cla()
    xValues = [locationsX[tour[i]] for i in range(len(tour))]
    yValues = [locationsY[tour[i]] for i in range(len(tour))]
    plt.plot(xValues + [xValues[0]], yValues + [yValues[0]],
             color='black', alpha=0.7, linewidth=4, label='Tour')
    plt.plot(locationsX, locationsY, 'ro')
    plt.draw()
    plt.pause(0.001)


def distance(x0, y0, x1, y1):
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)


def generateProblem(n):
    global distanceMatrix, locationsX, locationsY
    locationsX = [random() for _ in range(n)]
    locationsY = [random() for _ in range(n)]
    distanceMatrix = np.zeros((n, n))
    for i in range(0, n):
        for j in range(0, n):
            distanceMatrix[i, j] = distance(locationsX[i], locationsY[i], locationsX[j], locationsY[j])


def tspTop(n):
    global bestSoFar, bestSolution, count
    generateProblem(n)
    print(distanceMatrix)
    bestSoFar = float("inf")
    bestSolution = []
    count = 0
    tsp([i for i in range(1, n)])
    print("iterations = %7d, distance = %.3f, tour = %s" % (count, bestSoFar, bestSolution))


def tsp(cities, tour=[0], total=0):
    global bestSoFar, bestSolution, count
    count = count + 1
    # print("%s %s " % (str(cities), str(tour)))
    if cities == []:
        # add the return trip
        total = total + distanceMatrix[tour[0], tour[-1]]
        # update best so far tour
        if total < bestSoFar:
            # print("iterations = %7d, distance = %.3f, tour = %s" % (count, total, tour))
            bestSoFar = total
            bestSolution = tour
            displayTour(bestSolution)
    else:
        for i in range(0, len(cities)):
            # remove the ith
            copyCities = cities[:]
            copyCities.pop(i)
            # add each available city to a new tour, update total and continue
            tsp(copyCities, [cities[i]] + tour, total + distanceMatrix[tour[0], cities[i]])



sizes = []
times = []
for i in range(3, 12):
    start = time.time()
    tspTop(i)
    times.append(time.time() - start)
    sizes.append(i)

plt.clf()
plt.plot(sizes, times)
plt.xlabel('n')
plt.ylabel('Time (s)')
print('Times: ', times)
plt.show()
