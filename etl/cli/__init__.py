import click

from etl.cli.token_events_etl import token_events_collector


@click.group()
@click.pass_context
def cli(context):
    pass


cli.add_command(token_events_collector, "token_events_collector")
