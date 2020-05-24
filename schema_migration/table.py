from typing import Optional, List

from google.protobuf.descriptor import Descriptor

from analytics_schema import options_pb2
from schema_migration.clickhouse_engines import Distributed, MergeTree, ReplicatedMergeTree
from schema_migration.clickhouse_engines.url import URL
from schema_migration.utils import convert_proto_type_to_click_house_type, UnknownMessageError


class Table:
    def __init__(self, cluster_name: str, db_name: str, message_descriptor: Descriptor) -> None:
        self.cluster_name = cluster_name
        self.db_name = db_name
        self.message_descriptor = message_descriptor
        self.table_meta = message_descriptor.GetOptions().Extensions[options_pb2.table_meta]

    @property
    def engine(self):
        engine_mapping = {
            'MergeTree': MergeTree,
            'ReplicatedMergeTree': ReplicatedMergeTree,
            'URL': URL
        }
        engine_name = self.table_meta.WhichOneof('ENGINE')
        engine_message = getattr(self.table_meta, engine_name)
        engine_cls = engine_mapping[engine_name]
        engine = engine_cls(
            self.cluster_name,
            self.db_name,
            self.name,
            engine_message
        )
        return engine

    @property
    def name(self) -> str:
        return self.table_meta.NAME or self.message_descriptor.name

    def _get_fields_by_name_from_message_descriptor(self,
                                                    message_descriptor,
                                                    fields_by_name: Optional[List[str]] = None,
                                                    prefix: str = '') -> List[str]:
        _fields_by_name = fields_by_name or []
        field_items = message_descriptor.fields_by_name.items()
        for field_name, field_descriptor in field_items:
            try:
                field_type = convert_proto_type_to_click_house_type(field_descriptor)
            except UnknownMessageError:
                self._get_fields_by_name_from_message_descriptor(
                    field_descriptor.message_type,
                    fields_by_name=_fields_by_name,
                    prefix=f'{field_name}_'
                )
            else:
                _fields_by_name.append(f'{prefix}{field_name} {field_type}')
        return _fields_by_name

    @property
    def fields_by_name(self) -> List[str]:
        _fields_by_name = self._get_fields_by_name_from_message_descriptor(self.message_descriptor)
        return _fields_by_name

    def create_table_sql(self) -> str:
        sql = f'CREATE TABLE IF NOT EXISTS {self.db_name}.{self.name}'
        if self.cluster_name:
            sql += f' ON CLUSTER {self.cluster_name}'
        joined_fields = ',\n\t'.join(self.fields_by_name)
        sql += f' ({joined_fields})'
        sql += f' {self.engine.create_table_sql()}'
        return sql

    def drop_table_sql(self) -> str:
        sql = f'DROP TABLE IF EXISTS {self.db_name}.{self.name}'
        if self.cluster_name:
            sql += f' ON CLUSTER {self.cluster_name}'
        return sql

    def description_table_sql(self):
        sql = f'DESC {self.db_name}.{self.name}'
        return sql

    def alter_table_sql(self):
        sql = f'ALTER TABLE {self.db_name}.{self.name}'
        if self.cluster_name:
            sql += f' ON CLUSTER {self.cluster_name}'
        sql += f'{{diff}}'
        return sql


class DistributedTable(Table):
    @property
    def engine(self) -> Distributed:
        engine = Distributed(
            self.cluster_name,
            self.db_name,
            self.name
        )
        return engine

    def create_table_sql(self) -> str:
        engine_sql = self.engine.create_table_sql()
        sql = f'CREATE TABLE IF NOT EXISTS {self.db_name}.d_{self.name} {engine_sql}'
        return sql
