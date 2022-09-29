from sanic import Blueprint
from sanic.request import Request
from sanic_openapi.openapi2 import doc
from sanic.request import RequestParameters
from sanic.response import json
from sanic.log import logger
from web3 import Web3
from web3.middleware import geth_poa_middleware
from auto.string_input_handler import get_provider_from_string
from config import Provider
from database.mongodb_connector import MongoDBConnector


get_event_data_bp: Blueprint = Blueprint(
    name="get_event_data_blueprint", url_prefix="/event"
)
web3: Web3 = Web3(get_provider_from_string(provider_string=Provider.PUBLIC_RPC_NODE))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
_mongo: MongoDBConnector = MongoDBConnector()


@get_event_data_bp.route("/event-data", methods={"GET"}, strict_slashes=True)
@doc.tag("event")
@doc.summary("Get event data")
@doc.consumes(
    doc.String(
        name="token_address",
        description="Address of token: 0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c",
    ),
    location="query",
    required=False,
)
@doc.consumes(
    doc.Integer(
        name="block_number",
        description="A specific block: 20045095",
    ),
    location="query",
    required=False,
)
@doc.consumes(
    doc.String(
        name="transaction_hash",
        description="A specific transaction: 0x84ac34377973c13e14e09ead4aa7ac5717c5a709d4fbbebf451c8034e9118059",
    ),
    location="query",
    required=False,
)
@doc.consumes(
    doc.String(
        name="event_type",
        description="All events of the same type: Transfer",
    ),
    location="query",
    required=False,
)
@doc.response(400, {"message": str}, description="Bad Request")
@doc.response(401, {"message": str}, description="Unauthorized")
@doc.response(404, {"message": str}, description="Not Found")
async def get_event_data(request: Request):
    request_parameters: RequestParameters = request.args

    token_address = request_parameters.get("token_address")
    block_number: int = request_parameters.get("block_number")
    transaction_hash: str = request_parameters.get("transaction_hash")
    event_type: str = request_parameters.get("event_type")

    filter: dict = {}

    if token_address:
        token_address: str = web3.toChecksumAddress(token_address).lower()
        filter["block_number"] = str(token_address)
    if block_number:
        filter["block_number"] = int(block_number)
    if transaction_hash:
        filter["transaction_hash"] = str(transaction_hash)
    if event_type:
        event_type = event_type.upper()
        filter["event_type"] = str(event_type)

    result = _mongo.get_data(filter=filter)
    logger.info(f"Getting event with filter {filter}")

    return json(result)
