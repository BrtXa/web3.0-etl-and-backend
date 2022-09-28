from eth_utils import keccak
from constants.event_constants import RawEvent


class EventDataTransformer(object):
    def __init__(self) -> None:
        self.event_signature_hash_to_text: dict = {}

    def get_event_signature_hash(self, event_in_abi: dict) -> str:
        event_signature: str = event_in_abi.get("name") + "("
        for input in event_in_abi.get("inputs"):
            event_signature += input.get("type") + ","

        # Delete the last comma, which is invalid.
        event_signature = event_signature[:-1]
        event_signature += ")"

        signature_hash: str = "0x" + keccak(text=event_signature).hex()
        return signature_hash

    def get_events_params(self, event_in_abi: dict) -> list[str]:
        indexed: list = []
        non_indexed: list = []
        for input in event_in_abi.get("inputs"):
            if input.get("indexed"):
                indexed.append(input.get("name"))
            else:
                non_indexed.append(input.get("name"))
        return indexed + non_indexed

    def build_hash_to_text_mapper(self, event_abi: list[dict]):
        for abi in event_abi:
            signature_hash: str = self.get_event_signature_hash(abi)
            event_type: str = abi.get("name")
            event_params: list[str] = self.get_events_params(event_in_abi=abi)

            self.event_signature_hash_to_text[signature_hash] = [event_type]
            self.event_signature_hash_to_text[signature_hash] += event_params

        return self.event_signature_hash_to_text

    def get_valid_address(self, address: str) -> str:
        return "0x" + address[-40:]

    # TODO: Fix this method, it is sometime returning wrong value (right value = wrong value * 1e18).
    def get_valid_value(self, value: str) -> float:
        try:
            return float.fromhex(value) * (1e-18)
        # 0x value is considered invalid.
        except Exception as e:
            return float.fromhex(value + "0") * (1e-18)

    def transform_event_data(self, raw_event) -> dict:
        transaction_hash: str = raw_event[RawEvent.transaction_hash].hex()
        block_number = int = raw_event[RawEvent.block_number]
        log_index: int = raw_event[RawEvent.log_index]

        transformed_event: dict = {
            "contract_address": raw_event[RawEvent.address].lower(),
            "block_number": block_number,
            "transaction_hash": transaction_hash,
            "log_index": log_index,
        }

        event_args: list = self.event_signature_hash_to_text[
            raw_event["topics"][0].hex()
        ]
        event_type = event_args[0].upper()
        transformed_event["event_type"] = event_type

        # Loop from the second element of the list.
        for index in range(len(raw_event["topics"]) - 1):
            event_value: str = self.get_valid_address(
                raw_event["topics"][index + 1].hex()
            )
            transformed_event[event_args[index + 1]] = event_value

        transformed_event["amount"] = self.get_valid_value(str(raw_event["data"]))

        transformed_event[
            "_id"
        ] = f"transaction_{transaction_hash}_{event_type}_{block_number}_{log_index}"
        transformed_event["type"] = "event"

        return transformed_event
