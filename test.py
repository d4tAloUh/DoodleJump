import pygame

pygame.init()

sc = pygame.display.set_mode((400, 300))
sc.fill((100, 150, 200))

dog_surf = pygame.image.load('resources/Doodle_left.png')
# dog_surf.set_colorkey((255, 255, 255))
dog_rect = dog_surf.get_rect(center=(200, 150))
sc.blit(dog_surf, dog_rect)

pygame.display.update()

# ждем 1 секунду перед изменением
pygame.time.wait(1000)

sc.fill((100, 150, 200))
# уменьшаем в два раза
scale = pygame.transform.scale(dog_surf, (dog_surf.get_width() // 2,
                                          dog_surf.get_height() // 2))

scale_rect = scale.get_rect(center=(200, 150))

sc.blit(scale, scale_rect)

pygame.display.update(dog_rect)
pygame.time.wait(1000)

sc.fill((100, 150, 200))
# поворачиваем на 45 градусов
rot = pygame.transform.rotate(dog_surf, 45)
rot_rect = rot.get_rect(center=(200, 150))
sc.blit(rot, rot_rect)
pygame.display.update()