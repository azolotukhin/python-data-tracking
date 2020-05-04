from schema_migration.clickhouse_engines.base import Engine


class URL(Engine):
    @property
    def url(self) -> str:
        return self._table_meta.URL

    @property
    def format(self) -> str:
        return self._table_meta.Format

    def create_table_sql(self):
        return f'ENGINE = URL({self.url}, {self.format})'
