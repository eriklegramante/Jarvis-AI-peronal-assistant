import pygame
import random
import os

class JarvisAvatar:
    def __init__(self, image_path="jarvis_avatar.png"):
        pygame.init()
        
        self.screen = pygame.display.set_mode((300, 300), pygame.NOFRAME | pygame.SRCALPHA)
        
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except:
            self.image = pygame.Surface((200, 200), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (0, 150, 255, 200), (100, 100), 100)
            
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect(center=(150, 150))
        self.is_talking = False

    def draw(self):
        self.screen.fill((0, 0, 0, 0))
        
        if self.is_talking:
            scale_factor = random.uniform(1.0, 1.15)
            new_size = (int(200 * scale_factor), int(200 * scale_factor))
            scaled_image = pygame.transform.scale(self.image, new_size)
            temp_rect = scaled_image.get_rect(center=(150, 150))
            self.screen.blit(scaled_image, temp_rect)
        else:
            self.screen.blit(self.image, self.rect)

        pygame.display.flip()