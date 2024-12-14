import pyglet
from upgrades import Upgrade, upgrades

class UpgradePopup:
    def __init__(self, batch, player, upgrades):
        self.batch = batch
        self.player = player
        self.upgrades = upgrades
        self.labels = []
        self.active = False

    def show(self):
        self.active = True
        # Display upgrade options
        for i, upgrade in enumerate(self.upgrades):
            label = pyglet.text.Label(
                f"{i + 1}: {upgrade.name}",
                x=200,
                y=400 - i * 30,
                batch=self.batch,
                color=(255, 255, 255, 255)
            )
            self.labels.append(label)

    def apply_upgrade(self, choice):
        if 0 <= choice < len(self.upgrades):
            self.upgrades[choice].logic(self.player)
        self.hide()

    def hide(self):
        self.active = False
        for label in self.labels:
            label.delete()
        self.labels = []
