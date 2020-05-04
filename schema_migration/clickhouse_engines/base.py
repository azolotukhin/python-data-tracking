from abc import ABC, abstractmethod
from google.protobuf.descriptor import Descriptor


class Engine(ABC):
    def __init__(self, table_meta: Descriptor) -> None:
        self._table_meta = table_meta

    @abstractmethod
    def create_table_sql(self) -> str:
        ...
