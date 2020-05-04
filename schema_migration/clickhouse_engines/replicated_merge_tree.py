from schema_migration.clickhouse_engines.merge_tree import MergeTree


class ReplicatedMergeTree(MergeTree):
    def create_table_sql(self) -> str:
        sql = (
            f'ENGINE = ReplicatedMergeTree() PARTITION BY {self.partition_by} '
            f'ORDER BY ({self.order_by})'
        )
        if self.primary_key:
            sql += f' PRIMARY KEY {self.primary_key}'
        if self.sample_by:
            sql += f' SAMPLE BY {self.sample_by}'
        return sql
