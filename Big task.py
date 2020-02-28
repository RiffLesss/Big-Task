import requests
import pygame
import sys
import os
import math


LAT_STEP = 0.008
LON_STEP = 0.02
coord_to_geo_x = 0.0000428
coord_to_geo_y = 0.0000428


def ll(x, y):
    return "{}, {}".format(x, y)


class MapParams(object):
    def __init__(self):
        self.lat = 56.326887
        self.lon = 44.005986
        self.zoom = 15
        self.type = 'map'

    def ll(self):
        return ll(self.lon, self.lat)

    def update(self, event):
        if event.key == 280 and self.zoom < 19:
            self.zoom += 1
        elif event.key == 280 and self.zoom > 2:
            self.zoom -= 1
        elif event.key == 276:
            self.lon -= LON_STEP * math.pow(2, 15 - self.zoom)
        elif event.key == 275:
            self.lon += LON_STEP * math.pow(2, 15 - self.zoom)
        elif event.key == 273 and self.lat < 85:
            self.lat += LAT_STEP * math.pow(2, 15 - self.zoom)
        elif event.key == 274 and self.lat > -85:
            self.lat -= LAT_STEP * math.pow(2, 15 - self.zoom)
        if self.lon > 180:
            self.lon -= 360
        if self.lat < -180:
            self.lat += 360
