from schema_migration.clickhouse_engines.base import Engine


class Distributed(Engine):
    @property
    def sharding_key(self) -> str:
        return self._table_meta.sharding_key

    @property
    def origin_table_name(self) -> str:
        return self._table_meta.table_name

    def create_table_sql(self):
        sql = f'ENGINE = Distributed({self.cluster_name}, {self.db_name}, {self.origin_table_name}'
        finish_part = f', {self.sharding_key})' if self.sharding_key else ')'
        sql += finish_part
        return sql
