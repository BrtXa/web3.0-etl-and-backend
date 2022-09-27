# Distribute the big batch to smaller batches evenly for workers.
from typing import Iterable


def dynamic_batch_iterator(iterable: Iterable, batch_size: int) -> list:
    batch: list = []
    batch_size: int = batch_size
    for item in iterable:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
            batch_size = batch_size
    if len(batch) > 0:
        yield batch
