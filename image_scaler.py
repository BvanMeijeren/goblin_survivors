import pyglet

def scale_image(image, target_width, target_height):
    """
    Resizes a Pyglet image to the specified width and height.
    
    Args:
        image (pyglet.image.AbstractImage): The original image to be scaled.
        target_width (int): The desired width in pixels.
        target_height (int): The desired height in pixels.

    Returns:
        pyglet.image.Texture: The resized image as a Pyglet texture.
    """
    # Convert the image to a Texture if it's not already
    texture = image.get_texture()

    # Create a new blank texture with the target dimensions
    resized_texture = pyglet.image.Texture.create(target_width, target_height)

    # Scale the original image into the resized texture
    texture.blit_into(resized_texture, 0, 0, 0)

    return resized_texture
