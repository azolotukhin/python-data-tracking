from schema_migration.clickhouse_engines.merge_tree import MergeTree


class ReplicatedMergeTree(MergeTree):
    @property
    def zoo_path(self):
        return self._table_meta.zoo_path or f'/clickhouse/{self.db_name}/tables/{{shard}}/{self.table_name}'

    @property
    def replica_name(self):
        return self._table_meta.replica_name or '{replica}'

    def create_table_sql(self) -> str:
        sql = (
            f'ENGINE = ReplicatedMergeTree({self.zoo_path}, {self.replica_name}) '
            f'PARTITION BY {self.partition_by} '
            f'ORDER BY ({self.order_by})'
        )
        if self.primary_key:
            sql += f' PRIMARY KEY {self.primary_key}'
        if self.sample_by:
            sql += f' SAMPLE BY {self.sample_by}'
        return sql
