from PIL import Image


def get_image(*, image_format: str = "JPEG") -> Image.Image:
    image = Image.new("RGB", (100, 100))
    image.format = image_format
    return image
