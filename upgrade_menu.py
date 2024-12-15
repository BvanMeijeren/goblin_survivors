import pyglet
from upgrades import Upgrade, upgrades
import random

class UpgradePopup:
    def __init__(self, batch, player, upgrades, available_upgrades = None):
        self.batch = batch
        self.player = player
        self.upgrades = upgrades
        self.available_upgrades = available_upgrades 
        self.labels = []
        self.active = False

    def pick_available_upgrades(self):
        # Pick 3 random upgrades 
        upgrades_to_be_shown = random.sample(self.upgrades, 2)
        self.available_upgrades = upgrades_to_be_shown 

    def show(self):
        self.active = True

        # Display upgrade options
        for i, upgrade in enumerate(self.available_upgrades):
            label = pyglet.text.Label(
                f"{i + 1}: {upgrade.name}",
                x=200,
                y=400 - i * 30,
                batch=self.batch,
                color=(255, 255, 255, 255)
            )
            self.labels.append(label)

    def apply_upgrade(self, choice):
        if 0 <= choice < len(self.available_upgrades):
            self.available_upgrades[choice].logic(self.player)
        self.hide()

    def hide(self):
        self.active = False
        for label in self.labels:
            label.delete()
        self.labels = []
