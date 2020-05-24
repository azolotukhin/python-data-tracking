from schema_migration.table import Table


class Database:
    def __init__(self, cluster_name: str, db_name: str, endpoint: str):
        self.cluster_name = cluster_name
        self.db_name = db_name
        self.endpoint = endpoint
        self.client = None

    def create_database_sql(self):
        sql = f'CREATE DATABASE IF NOT EXISTS {self.db_name}'
        if self.cluster_name:
            sql += f' ON CLUSTER {self.cluster_name}'
        return sql

    def drop_database_sql(self):
        sql = f'DROP DATABASE IF EXISTS {self.db_name}'
        if self.cluster_name:
            sql += f' ON CLUSTER {self.cluster_name}'
        return sql

    def db_size_sql(self):
        sql = f'SELECT sum(bytes) as total_size FROM system.parts WHERE database = {self.db_name} AND active = 1'
        return sql

    def create_tables(self):
        pass

    def create_table(self, message_descriptor):
        pass

    def alter_tables(self):
        pass

    def alter_table(self, message_descriptor):
        table = Table(
            self.cluster_name,
            self.db_name,
            message_descriptor
        )
        pass

    def drop_tables(self):
        pass

    def drop_table(self, message_descriptor):
        pass
