from . import _vendors


def get_image_extraction_service() -> _vendors.ImageExtractionService:
    return _vendors.OpenAIImageExtractService()
