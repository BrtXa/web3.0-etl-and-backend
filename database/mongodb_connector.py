import sys
from pymongo import MongoClient
from pymongo import UpdateOne
from config import MongoDBConfig
from pymongo.cursor import Cursor


class MongoDBEventLoader(object):
    def __init__(
        self,
        collection_url: str = MongoDBConfig.LOCAL_CONNECTION_URL,
        db_name: str = MongoDBConfig.DATABASE,
        collection_name: str = MongoDBConfig.COLLECTION,
    ) -> None:
        try:
            # FIXME Unable to read from .env file
            self.client: MongoClient = MongoClient(collection_url)
        except:
            sys.exit(1)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def load_data(self, data: list) -> None:
        self.__create_data(data)

    def __create_data(self, operations_data: list[dict]) -> None:
        if not operations_data:
            return

        bulk_operation = [
            UpdateOne({"_id": data["_id"]}, {"$set": data}, upsert=True)
            for data in operations_data
        ]

        try:
            self.collection.bulk_write(bulk_operation)
        except Exception as bwe:
            print(bwe)

    def delete_events_for_testing(self):
        filter: dict = {"block_number": {"$lte": 21175364}}
        self.collection.delete_many(filter=filter)
