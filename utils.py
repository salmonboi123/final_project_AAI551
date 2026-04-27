import functools
import pandas as pd

# Custom Exception
class InvalidDataError(Exception):
    """Raised when weather or energy values are physically impossible."""
    pass

# Decorator for logging
def logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Executing {func.__name__}...")
        return func(*args, **kwargs)
    return wrapper

# Generator for memory efficiency
def data_chunk_generator(file_path, chunk_size=1000):
    """Yields chunks of the dataset to save RAM."""
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        yield chunk