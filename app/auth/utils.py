"App auth utilities functions"

import os
import hashlib


def default_token_generator() -> str:
    """
    Generates token based on random 64-bits and BLAKE2B hashing algorithm.

    Returns:
        string with generated token
    """
    result = hashlib.blake2b(os.urandom(64))
    return result.hexdigest()
