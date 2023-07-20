# Standard library imports
import io

# Django imports
from django.core import files


def image() -> files.File:
    file = io.BytesIO(b"sausage pasta")
    return files.File(file=file, name="some-file.jpg")
