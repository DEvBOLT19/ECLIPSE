import json
import pygame
import time

class Cutscene:
    def __init__(self, scene_file):
        self.scene_file = scene_file
        self.dialogues = []
        self.load_scene()

    def load_scene(self):
        with open(self.scene_file) as f:
            data = json.load(f)
            self.dialogues = data.get("dialogues", [])

    def play(self):
        for dialogue in self.dialogues:
            print(f"{dialogue['speaker']}: {dialogue['text']}")
            time.sleep(dialogue.get("delay", 2))
