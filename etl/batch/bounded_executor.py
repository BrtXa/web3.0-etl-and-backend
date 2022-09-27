from concurrent.futures import ThreadPoolExecutor, Future


class BoundedExecutor:
    def __init__(self, max_workers: int) -> None:
        self.__delegate: ThreadPoolExecutor = ThreadPoolExecutor(
            max_workers=max_workers
        )

    def submit(self, fn, *args, **kwargs):
        future: Future = self.__delegate.submit(fn, *args, **kwargs)
        return future

    def shutdown(self, wait=True):
        self.__delegate.shutdown(wait=wait)
