import hashlib


def get_hash_for_text(*, text: str) -> str:
    """
    Return the hexadecimal digest of the MD5 hash for some text.

    This is stored alongside the corresponding embedding, so that we can
    more efficiently check when the embedding needs updating.
    """
    hashed_text = hashlib.md5(text.encode())
    return hashed_text.hexdigest()
