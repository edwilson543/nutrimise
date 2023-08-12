# Standard library imports
import io

# Third party imports
from PIL import Image

# Django imports
from django.core import files


def image() -> files.File:
    buffer = image_buffer()
    return files.File(file=buffer, name="some-file.jpg")


def image_buffer() -> io.BytesIO:
    buffer = io.BytesIO()
    square = Image.new("RGB", (100, 100))
    square.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer
