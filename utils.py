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


def average_kw(values):
    """Quick helper that returns the average of a list of kW readings.
    Skips any None entries so it doesn't crash on missing data."""
    cleaned = [v for v in values if v is not None]
    if not cleaned:
        return 0
    return sum(cleaned) / len(cleaned)
