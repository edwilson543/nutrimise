import hashlib

import numpy as np

from . import _embedding


def get_hash_for_text(*, text: str) -> str:
    """
    Return the hexadecimal digest of the MD5 hash for some text.

    This is stored alongside the corresponding embedding, so that we can
    more efficiently check when the embedding needs updating.
    """
    hashed_text = hashlib.md5(text.encode())
    return hashed_text.hexdigest()


def get_stub_vector_embedding() -> np.ndarray:
    """
    Get a stub vector of the correct dimension.

    This is for use in fake embedding services and tests.
    """
    return np.ones(_embedding.EMBEDDING_DIMENSIONS)
