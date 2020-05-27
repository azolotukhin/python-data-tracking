from schema_migration.clickhouse_engines.base import Engine


class Distributed(Engine):
    # def __init__(self, cluster_name, db_name, table_name, sharding_key=None):
    #     self.cluster_name = cluster_name
    #     self.db_name = db_name
    #     self.table_name = table_name
    #     self.sharding_key = sharding_key

    @property
    def sharding_key(self) -> str:
        return self._table_meta.sharding_key

    def create_table_sql(self):
        sql = f'ENGINE = Distributed({self.cluster_name}, {self.db_name}, {self.table_name}'
        finish_part = f', {self.sharding_key})' if self.sharding_key else ')'
        sql += finish_part
        return sql
