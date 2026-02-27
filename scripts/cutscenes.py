import json
import pygame

class Cutscene:
    def __init__(self, scene_file, screen):
        self.scene_file = scene_file
        self.dialogues = []
        self.screen = screen
        self.load_scene()

    def load_scene(self):
        with open(self.scene_file) as f:
            data = json.load(f)
            self.dialogues = data.get("dialogues", [])

    def play(self):
        font = pygame.font.SysFont(None, 30)
        for dialogue in self.dialogues:
            self.screen.fill((0,0,0))
            text = font.render(f"{dialogue['speaker']}: {dialogue['text']}", True, (255,255,255))
            self.screen.blit(text, (50, 500))
            pygame.display.flip()
            pygame.time.delay(dialogue.get("delay", 2000))
