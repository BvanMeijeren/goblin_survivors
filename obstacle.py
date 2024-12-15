class Obstacle:
    def __init__(self, x, y, batch, image_path, scale):
        image = pyglet.image.load(image_path)
        super().__init__(image, x, y, batch=batch)


# all obstacles in dictionary
obstacles = {
    "Rock" : Obstacle(
        x = random.choice([0, 800]),
        y = random.choice([0, 600]),
        batch,
        image_path =  ,
        scale
    ),
    "Tree" : Obstacle(
        x = random.choice([0, 800]),
        y = random.choice([0, 600]),
        batch,
        image_path =  ,
        scale
    )
}


