import enum


class ImageExtractionVendor(enum.Enum):
    OPENAI = "OPENAI"

    # Fake vendors.
    FAKE = "FAKE"
    FAKE_NO_SERVICE = "FAKE_NO_SERVICE"
    BROKEN = "BROKEN"


class ImageExtractionModel(enum.Enum):
    # OpenAI.
    GPT_4O = "gpt-4o-2024-08-06"

    # Fake models.
    FAKE = "fake"
