from schema_migration.clickhouse_engines.base import Engine


class MergeTree(Engine):
    @property
    def partition_by(self) -> str:
        return self._table_meta.PARTITION_BY or 'toYYYYMM(date)'

    @property
    def order_by(self) -> str:
        return self._table_meta.ORDER_BY or 'date, action, player_id, sipHash64(player_id)'

    @property
    def primary_key(self) -> str:
        return self._table_meta.PRIMARY_KEY

    @property
    def sample_by(self) -> str:
        return self._table_meta.SAMPLE_BY or 'sipHash64(player_id)'

    def create_table_sql(self) -> str:
        sql = (
            f'ENGINE = MergeTree() PARTITION BY {self.partition_by} '
            f'ORDER BY ({self.order_by})'
        )
        if self.primary_key:
            sql += f' PRIMARY KEY {self.primary_key}'
        if self.sample_by:
            sql += f' SAMPLE BY {self.sample_by}'
        return sql
