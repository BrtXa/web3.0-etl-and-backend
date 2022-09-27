from urllib.parse import urlparse
from web3 import Web3

from constants.abi_constants import ABI


def get_abi_from_string(abi_string: str):
    return ABI.abi_mapping[abi_string]


def get_provider_from_string(provider_string: str):
    uri = urlparse(provider_string)
    if uri.scheme == "file":
        pass
    elif uri.scheme == "http" or uri.scheme == "https":
        return Web3.HTTPProvider(provider_string)
    elif uri.scheme == "wss" or uri.scheme == "ws":
        return Web3.WebsocketProvider(provider_string)
    else:
        raise ValueError("Unknown uri scheme {}".format(provider_string))
