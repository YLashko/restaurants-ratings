from PIL import Image


def resize_image(image, size):
    img = Image.fromqimage(image)
    img.thumbnail(size)
    return img
