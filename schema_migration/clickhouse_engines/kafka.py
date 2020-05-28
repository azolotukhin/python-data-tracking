from schema_migration.clickhouse_engines.base import Engine


class Kafka(Engine):
    @property
    def kafka_broker_list(self) -> str:
        return self._table_meta.kafka_broker_list

    @property
    def kafka_topic_list(self) -> str:
        return self._table_meta.kafka_topic_list

    @property
    def kafka_group_name(self) -> str:
        return self._table_meta.kafka_group_name

    @property
    def kafka_format(self) -> str:
        return self._table_meta.kafka_format

    @property
    def kafka_row_delimiter(self) -> str:
        return self._table_meta.kafka_row_delimiter

    @property
    def kafka_schema(self) -> str:
        return self._table_meta.kafka_schema

    @property
    def kafka_num_consumers(self) -> str:
        return self._table_meta.kafka_num_consumers

    @property
    def kafka_skip_broken_messages(self) -> str:
        return self._table_meta.kafka_skip_broken_messages

    def create_table_sql(self) -> str:
        sql = (
            f"ENGINE = Kafka() SETTINGS\n"
            f" kafka_broker_list = '{self.kafka_broker_list}',\n"
            f" kafka_topic_list = '{self.kafka_topic_list}',\n"
            f" kafka_group_name = '{self.kafka_group_name}',\n"
            f" kafka_format = '{self.kafka_format}'\n"
        )
        if self.kafka_row_delimiter:
            sql += f' ,\nkafka_row_delimiter = {self.kafka_row_delimiter}'
        if self.kafka_schema:
            sql += f' ,\nkafka_schema = {self.kafka_schema}'
        if self.kafka_num_consumers:
            sql += f' ,\nkafka_num_consumers = {self.kafka_num_consumers}'
        if self.kafka_skip_broken_messages:
            sql += f' \nkafka_skip_broken_messages = {self.kafka_skip_broken_messages}'
        return sql
