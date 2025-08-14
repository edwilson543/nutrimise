import functools
import pathlib

from PIL import Image


TEST_IMAGE_PATH = pathlib.Path(__file__).parent / "test-image.jpeg"


def get_image(*, image_format: str = "JPEG") -> Image.Image:
    image = Image.new("RGB", (100, 100))
    image.format = image_format
    return image


@functools.lru_cache(maxsize=1)
def get_uploaded_image() -> tuple[str, bytes]:
    with open(TEST_IMAGE_PATH, "rb") as uploaded_image:
        return "test-image.jpeg", uploaded_image.read()
