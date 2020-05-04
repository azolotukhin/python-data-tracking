import click
from proto_builder.cli import cli as proto_builder_cli
from collector.cli import cli as collector_cli
from schema_migration.cli import cli as schema_migration_cli


@click.group()
def cli():
    pass


cli.add_command(proto_builder_cli, name='proto_builder')
cli.add_command(collector_cli, name='collector_cli')
cli.add_command(schema_migration_cli, name='schema_migration')


if __name__ == '__main__':
    cli()
