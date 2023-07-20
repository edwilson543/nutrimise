# Standard library imports
import io

# Third party imports
from PIL import Image

# Django imports
from django.core import files


def image() -> files.File:
    file = io.BytesIO()
    blue_square = Image.new("RGB", (100, 100))
    blue_square.save(file, format="JPEG")
    file.seek(0)
    return files.File(file=file, name="some-file.jpg")
