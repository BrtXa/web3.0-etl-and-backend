import logging

from etl.pipe.event_pipeline_pumper import EventPipelinePumper


_LOGGER = logging.getLogger(__name__)


class Pipeline:
    def __init__(
        self,
        pipeline_pumper: EventPipelinePumper,
        start_block: int,
        end_block: int,
        block_batch_size: int,
    ) -> None:
        self.pipeline_pumper = pipeline_pumper
        self.start_block: int = start_block
        self.end_block: int = end_block
        self.block_batch_size = block_batch_size
        self.target_block: int = 0
        self.last_synced_block: int = self.start_block - 1

    def open_pipeline(self):
        try:
            self.pipeline_pumper.open()
            self._pipeline()
        finally:
            self.pipeline_pumper.close()

    def _pipeline(self):
        while True and self.last_synced_block < self.end_block:
            try:
                self._sync_cycle()
            except Exception as e:
                _LOGGER.warning("An exception occurred while syncing block data")
                _LOGGER.info(f"Error: {e}")

    def _sync_cycle(self):
        self.target_block: int = self._calculate_target_block()
        _LOGGER.info(
            f"Current block: {self.last_synced_block + 1}, target block: {self.target_block}"
        )
        self.pipeline_pumper.pump_to_pipeline(
            self.last_synced_block + 1, self.target_block
        )
        self.last_synced_block = self.target_block

    def _calculate_target_block(self):
        next_block: int = self.last_synced_block
        target_block: int = next_block + self.block_batch_size

        if target_block >= self.end_block:
            return self.end_block
        return target_block
