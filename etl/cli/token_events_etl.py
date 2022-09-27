import logging
import time
import click
from config import Provider
from database.mongodb_connector import MongoDBEventLoader
from etl.auto.string_input_handler import get_provider_from_string, get_abi_from_string
from etl.pipe.event_pipeline_pumper import EventPipelinePumper
from etl.pipe.pipeline import Pipeline

from utils.logger_utils import logging_basic_config


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-ca",
    "--contract-addresses",
    default=[],
    show_default=True,
    type=str,
    multiple=True,
    help="List of token addresses",
)
@click.option(
    "-s",
    "--start-block",
    default=20045095,
    show_default=True,
    type=int,
    help="Start block",
)
@click.option(
    "-e",
    "--end-block",
    default=20936754,
    show_default=True,
    type=int,
    help="End block",
)
@click.option(
    "-b",
    "--worker-batch-size",
    default=100,
    show_default=True,
    type=int,
    help="Number of blocks each worker will handle",
)
@click.option(
    "-B",
    "--pipeline-batch-size",
    default=100,
    show_default=True,
    type=int,
    help="The number of blocks to collect at a time.",
)
@click.option(
    "-w",
    "--max-workers",
    default=5,
    show_default=True,
    type=int,
    help="Maximum number of workers.",
)
@click.option(
    "-p",
    "--provider",
    default=Provider.PUBLIC_RPC_NODE,
    show_default=True,
    type=str,
    help="public rpc node url",
)
@click.option(
    "--abi",
    default="bep_20",
    show_default=True,
    type=str,
    help="token abi",
)
def token_events_collector(
    contract_addresses: str,
    start_block: int,
    end_block: int,
    worker_batch_size: int,
    pipeline_batch_size: int,
    max_workers: int,
    provider: str,
    abi: str,
):
    _mongo = MongoDBEventLoader()
    _mongo.delete_events_for_testing()

    logging_basic_config()
    _LOGGER: logging.Logger = logging.getLogger(__name__)

    item_loader: MongoDBEventLoader = MongoDBEventLoader()

    _LOGGER.info(f"Start streaming from block {start_block} to block {end_block}")

    pipeline_pumper: EventPipelinePumper = EventPipelinePumper(
        contract_addresses=list(contract_addresses),
        item_loader=item_loader,
        batch_size=worker_batch_size,
        max_workers=max_workers,
        provider=get_provider_from_string(provider),
        abi=get_abi_from_string(abi),
    )

    pipeline: Pipeline = Pipeline(
        pipeline_pumper=pipeline_pumper,
        start_block=start_block,
        end_block=end_block,
        block_batch_size=pipeline_batch_size,
    )

    start_time = int(time.time())
    pipeline.open_pipeline()
    end_time = int(time.time())
    logging.info("Total time " + str(end_time - start_time))
