from web3 import Web3
from web3.middleware import geth_poa_middleware
from database.mongodb_connector import MongoDBEventLoader
from etl.pump.event_pump import EventPump


class EventPipelinePumper:
    def __init__(
        self,
        contract_addresses: list[str],
        item_loader: MongoDBEventLoader,
        batch_size: int,
        max_workers: int,
        provider,
        abi: list,
    ) -> None:
        self.contract_addresses: list[str] = [
            Web3.toChecksumAddress(address).lower() for address in contract_addresses
        ]
        self.item_loader: MongoDBEventLoader = item_loader
        self.batch_size: int = batch_size
        self.max_workers: int = max_workers
        self.abi: list = abi
        self.web3: Web3 = Web3(provider)
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    def open(self):
        pass

    def pump_to_pipeline(self, start_block: int, end_block: int):
        self.__pump(
            start_block=start_block,
            end_block=end_block,
        )

    def __pump(self, start_block: int, end_block: int):
        pump: EventPump = EventPump(
            start_block=start_block,
            end_block=end_block,
            contract_addresses=self.contract_addresses,
            abi=self.abi,
            batch_size=self.batch_size,
            max_workers=self.max_workers,
            web3=self.web3,
            item_loader=self.item_loader,
        )
        pump.run()

    def close(self):
        pass
