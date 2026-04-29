import functools
import pandas as pd


class InvalidDataError(Exception):
    """Raised when the input data has values that should not be possible."""
    pass


def logger(func):
    """Small logger so we can see when important steps are running."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Running {func.__name__}...")
        return func(*args, **kwargs)
    return wrapper


def data_chunk_generator(file_path, chunk_size=1000):
    """Read a CSV file in smaller pieces instead of loading everything at once."""
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        yield chunk
