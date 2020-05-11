from abc import ABC, abstractmethod
from google.protobuf.descriptor import Descriptor


class Engine(ABC):
    def __init__(self, cluster_name: str, db_name: str, table_name: str, table_meta: Descriptor) -> None:
        self.cluster_name = cluster_name
        self.db_name = db_name
        self.table_name = table_name
        self._table_meta = table_meta

    @abstractmethod
    def create_table_sql(self) -> str:
        ...
