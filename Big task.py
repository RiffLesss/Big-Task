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
    return "{},{}".format(x, y)


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
        elif event.key == 281 and self.zoom > 2:
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


def screen_to_geo(self, pos):
    dy = 225 - pos[1]
    dx = pos[0] - 300
    lx = self.lon + dx * coord_to_geo_x * math.pow(2, 15 - self.zoom)
    ly = self.lat + dy * coord_to_geo_y * math.pow(2, 15 - self.zoom) * math.cos(math.radians(self.lat))
    return lx, ly

def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={}&z={}&l={}".format(mp.ll(), mp.zoom, mp.type)
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        sys.exit(1)
    map_file = 'map.png'
    try:
        with open(map_file, 'wb') as file:
            file.write(response.content)
    except IOError as ex:
        print('Ошибка записи временного файла:', ex)
        sys.exit(2)
    return map_file

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    mp = MapParams()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYUP:
            mp.update(event)
        else:
            continue

        map_file = load_map(mp)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


main()

