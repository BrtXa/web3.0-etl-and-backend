from typing import Callable, Iterable 
from etl.auto.batch_distributor import dynamic_batch_iterator
from etl.batch.bounded_executor import BoundedExecutor


class BatchJobExecutor:
    def __init__(
        self,
        batch_size: int,
        max_workers: int,
    ) -> None:
        self.batch_size: int = batch_size
        self.max_workers: int = max_workers
        self.bounded_executor: BoundedExecutor = BoundedExecutor(
            max_workers=self.max_workers
        )

    def submit(self, work_handler: Callable, work_iterable: Iterable):
        for batch in dynamic_batch_iterator(
            iterable=work_iterable,
            batch_size=self.batch_size,
        ):
            self.bounded_executor.submit(work_handler, batch)

    def shutdown(self):
        self.bounded_executor.shutdown()
