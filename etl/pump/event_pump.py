import logging
from web3 import Web3
from web3._utils.filters import Filter
from database.mongodb_connector import MongoDBConnector
from auto.event_data_transformer import EventDataTransformer
from etl.batch.batch_job_executor import BatchJobExecutor
from etl.model.pump_model import PumpModel

_LOGGER = logging.getLogger(__name__)


class EventPump(PumpModel):
    def __init__(
        self,
        start_block: int,
        end_block: int,
        contract_addresses: list[str],
        abi: list,
        batch_size: int,
        max_workers: int,
        web3: Web3,
        item_loader: MongoDBConnector,
    ) -> None:
        self.start_block: int = start_block
        self.end_block: int = end_block
        self.contract_addresses: list = contract_addresses
        self.abi: list = abi
        self.batch_job_executor: BatchJobExecutor = BatchJobExecutor(
            batch_size=batch_size,
            max_workers=max_workers,
        )
        self.web3: Web3 = web3
        self.item_loader: MongoDBConnector = item_loader
        self.event_data_transformer: EventDataTransformer = EventDataTransformer()

    def _start(self):
        self.event_data: list = []
        self.hash_to_text_mapper: dict = (
            self.event_data_transformer.build_hash_to_text_mapper(event_abi=self.abi)
        )
        self.list_event_hash: list = [hash for hash in self.hash_to_text_mapper]
        _LOGGER.info("Start crawling events")

    def _pump(self):
        self.batch_job_executor.submit(
            work_handler=self.__pump_with_batch_executor,
            work_iterable=range(self.start_block, self.end_block + 1),
        )

    def __pump_with_batch_executor(self, block_number_batch: list[int]):
        _LOGGER.info(
            f"Crawling events from {block_number_batch[0]} to {block_number_batch[-1]}"
        )
        event_list: list = self.__pump_data(
            start_block=block_number_batch[0],
            end_block=block_number_batch[-1],
            addresses=self.contract_addresses,
            topics=self.list_event_hash,
        )
        self.event_data += event_list

    def __pump_data(
        self,
        start_block: int,
        end_block: int,
        addresses: list[str],
        topics: list[str],
    ) -> list:
        filter_params: dict = {
            "fromBlock": start_block,
            "toBlock": end_block,
            "topics": [topics],
        }
        if addresses is not None and len(addresses) > 0:
            filter_params["address"] = addresses

        event_filter: Filter = self.web3.eth.filter(filter_params)
        events: list = event_filter.get_all_entries()

        # TODO: Add data transform moduel.
        event_list: list = []
        for event in events:
            event_in_dict: dict = self.event_data_transformer.transform_event_data(
                raw_event=event
            )
            event_list.append(event_in_dict)

        self.web3.eth.uninstallFilter(event_filter.filter_id)
        return event_list

    def _end(self):
        self.batch_job_executor.shutdown()
        self.item_loader.load_data(self.event_data)
        _LOGGER.info(f"Crawled events from {self.start_block} to {self.end_block}")
