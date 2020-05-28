import click
from google.protobuf.symbol_database import Default
from analytics_schema import options_pb2
from analytics_schema.game.track_event_pb2 import *
# from analytics_schema.game2.track_event_pb2 import *
# from analytics_schema.game.aggregations.install_pb2 import *
from schema_migration.table import Table
from schema_migration.view import View


@click.group()
def cli():
    pass


@cli.command('create_tables')
def create_tables():
    sym_db = Default()
    for message_type in sym_db._classes:
        message_meta = message_type.GetOptions().Extensions[options_pb2.message_meta]
        meta_object = message_meta.WhichOneof('Meta')
        if meta_object == 'table_meta':
            if message_meta.table_meta.WhichOneof('ENGINE'):
                table = Table('office', 'bfg', message_type)
                print(table.create_table_sql())
        elif meta_object == 'view_meta':
            table = View('office', 'bfg', message_type)
            print(table.create_view_sql())
    return

    # tables = {}
    # d = TrackEvent.DESCRIPTOR
    # fields_by_name = d.fields_by_name.items()
    # for name, field in fields_by_name:
    #     if field.containing_oneof is None or field.containing_oneof.name != 'event':
    #         continue
    #     if field.message_type is None:
    #         continue
    #     table = Table('anal', 'ww2', field.message_type)
    #     print(table.create_table_sql())
    #     if not field.message_type.GetOptions().Extensions[options_pb2.table_meta].DISABLE_DISTRIBUTED:
    #         distributed_table = DistributedTable('anal', 'ww2', field.message_type)
    #         print(distributed_table.create_table_sql())
