# Functions for the taxi trip duration & distance prediction project

# Import modules
import numpy as np
from math import sqrt, pi, atan2, sin, cos, radians


# Compute the angle of a point or between two points, a and b
# Each point has a latitude and longitude coordinate. In this case
# a,b = [longitude,latitude]
def computeAng(a, b):
    if (len(b) == 0):
        rad = atan2(a[1], a[0])
    else:
        rad = atan2(a[1], a[0]) - atan2(b[1], b[0])

    ang = rad * 180 / pi
    if ((ang < 0) & (len(b) < 0)):
        ang += 360

    return ang


# calculate bearing: http://www.movable-type.co.uk/scripts/latlong.html
# checked a few points using http://www.sunearthtools.com/tools/distance.php
def computeBearing(a, b):
    a = np.radians(a)  # starting point
    b = np.radians(b)  # end point

    lat2 = a[1]
    long2 = a[0]
    lat1 = b[1]
    long1 = b[0]

    y = sin(long2 - long1) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(long2 - long1)
    bearing = atan2(y, x) * 180 / pi
    if (bearing < 0):
        bearing = bearing + 360

    return bearing


# calculate the distance between two points
# Haversine formula
def computeDistance(a):
    gpsVec = np.asarray(a)
    latVec = [radians(coord[1]) for coord in gpsVec]
    longVec = [radians(coord[0]) for coord in gpsVec]
    dist = 0
    distVec = []
    for p in range(len(gpsVec) - 1):
        a = sin((latVec[p + 1] - latVec[p]) / 2) ** 2 + \
            cos(latVec[p]) * cos(latVec[p + 1]) * sin((longVec[p + 1] - longVec[p]) / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        d = 3959 * c  # in miles, 3959mi is the radius of the earth
        distVec.append(d)
        dist += d
    return distVec, dist
    

def directionality(a):
    if (a>0) & (a<=90):
        return 'NE'
    elif (a>90) & (a<= 180):
        return 'SE'
    elif (a>180) & (a<=270):
        return 'SW'
    elif (a>270) & (a<=360):
        return 'NW'    
        
        
        
        
# DTW functions
def distance_cost_plot(distances):
    im = plt.imshow(distances, interpolation='nearest', cmap='Reds') 
    plt.gca().invert_yaxis()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()
    plt.colorbar();

# code from http://nipunbatra.github.io/2014/07/dtw/
    
def dtw_distances(testGPS,trainGPS):
    distances = np.zeros((len(testGPS),len(trainGPS)))
    for i in range(len(testGPS)):
        for j in range(len(trainGPS)):
            distances[i,j] = sqrt((testGPS[i][0]-trainGPS[j][0])**2 +\
                              (testGPS[i][1]-trainGPS[j][1])**2)
    return distances

def dtw_start_cost(testGPS,trainGPS,distances):
    accumulated_cost = np.zeros((len(testGPS),len(trainGPS)))
    accumulated_cost[0,0] = distances[0,0]
    for i in range(1, len(trainGPS)):
        accumulated_cost[0,i] = distances[0,i] + accumulated_cost[0, i-1]
    for i in range(1, len(testGPS)):
        accumulated_cost[i,0] = distances[i, 0] + accumulated_cost[i-1, 0]
    for i in range(1, len(testGPS)):
        for j in range(1, len(trainGPS)):
            accumulated_cost[i, j] = min(accumulated_cost[i-1, j-1], accumulated_cost[i-1, j], accumulated_cost[i, j-1]) + distances[i, j]
    return accumulated_cost

def path_cost(x, y, accumulated_cost, distances):
    path = [[len(x)-1, len(y)-1]]
    cost = 0
    i = len(y)-1
    j = len(x)-1
    while i>0 and j>0:
        if i==0:
            j = j - 1
        elif j==0:
            i = i - 1
        else:
            if accumulated_cost[i-1, j] == min(accumulated_cost[i-1, j-1], accumulated_cost[i-1, j], accumulated_cost[i, j-1]):
                i = i - 1
            elif accumulated_cost[i, j-1] == min(accumulated_cost[i-1, j-1], accumulated_cost[i-1, j], accumulated_cost[i, j-1]):
                j = j-1
            else:
                i = i - 1
                j= j- 1
        path.append([j, i])
    path.append([0,0])
    for [y, x] in path:
        cost = cost +distances[x, y]
    return path, cost    