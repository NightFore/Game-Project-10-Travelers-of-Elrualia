import pygame
import random
from os import path


def update_time_dependent(sprite):
    sprite.current_time += sprite.dt
    if sprite.current_time >= sprite.animation_time:
        sprite.current_time = 0
        sprite.index = (sprite.index + 1) % len(sprite.images)
        sprite.image = sprite.images[sprite.index]
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = sprite.pos
    sprite.image = pygame.transform.rotate(sprite.image, 0)


def update_bobbing(sprite):
    offset = BOB_RANGE * (sprite.tween(sprite.step / BOB_RANGE) - 0.5)
    sprite.rect.centery = sprite.pos.y + offset * sprite.dir
    sprite.step += BOB_SPEED
    if sprite.step > BOB_RANGE:
        sprite.step = 0
        sprite.dir *= -1


def load_file(path, image=False):
    file = []
    for file_name in os.listdir(path):
        if image:
            file.append(pygame.image.load(path + os.sep + file_name).convert_alpha())
        else:
            file.append(path + os.sep + file_name)
    return file


def load_image(image_path, image_list):
    images = []
    for image in image_list:
        images.append(pygame.image.load(path.join(image_path, image)).convert_alpha())
    return images


def load_rect(image_list):
    rect_list = []
    for image in image_list:
        rect_list.append(image.get_rect())
    return rect_list



def load_tile_table(filename, width, height, colorkey=(0, 0, 0)):
    image = pygame.image.load(filename).convert()
    image.set_colorkey(colorkey)
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_y in range(int(image_height / height)):
        line = []
        tile_table.append(line)
        for tile_x in range(int(image_width / width)):
            rect = (tile_x * width, tile_y * height, width, height)
            line.append(image.subsurface(rect))
    return tile_table


def transparent_surface(width, height, color, border, colorkey=(0, 0, 0)):
    surface = pygame.Surface((width, height)).convert()
    surface.set_colorkey(colorkey)
    surface.fill(color)
    surface.fill(colorkey, surface.get_rect().inflate(-border, -border))
    return surface


def collision(sprite_1, sprite_2, dx=0, dy=0):
    sprite_1.pos[0] += dx
    sprite_1.pos[1] += dy
    sprite_1.rect.x = sprite_1.pos[0] * TILESIZE
    sprite_1.rect.y = sprite_1.pos[1] * TILESIZE
    collide = pygame.sprite.spritecollide(sprite_1, sprite_2, False)

    sprite_1.pos[0] -= dx
    sprite_1.pos[1] -= dy
    sprite_1.rect.x = sprite_1.pos[0] * TILESIZE
    sprite_1.rect.y = sprite_1.pos[1] * TILESIZE
    return collide


def reachable(list, i_loop, j_loop, rg):
    for i in range(2 * i_loop + 1):
        for j in range(2 * j_loop + 1):
            if list[i][j]:
                reach = False
                for x in range(-rg, rg + 1):
                    for y in range(-rg, rg + 1):
                        if abs(x) + abs(y) == rg and 0 < i + x < 2 * i_loop + 1 and 0 < j + y < 2 * j_loop + 1:
                            if list[i + x][j + y]:
                                reach = True
                list[i][j] = reach


def sort_list(list, var, reverse=False):
    if reverse:
        list.reverse()

    for i in range(len(list)):
        # Display list
        #print(list)

        if list[i] == var:
            cpt = 0
            while list[i + cpt] == var and i + cpt < len(list)-1:
                cpt += 1
            list[i] = list[i+cpt]
            list[i+cpt] = var

    if reverse:
        list.reverse()