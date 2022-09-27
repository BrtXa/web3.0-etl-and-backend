from eth_utils import keccak
from constants.abi_constants import ABI


def get_abi_from_string(abi_string: str):
    return ABI.abi_mapping[abi_string]


def get_event_hash(abi: list[dict]) -> list[str]:
    event_list: list[str] = []
    for event in abi:
        event_signature: str = event.get("name") + "("
        for input in event.get("inputs"):
            event_signature += input.get("type") + ","

        # Delete the last comma, which is invalid.
        event_signature = event_signature[:-1]
        event_signature += ")"

        signature_hash: str = "0x" + keccak(text=event_signature).hex()
        event_list.append(signature_hash)
    return event_list
