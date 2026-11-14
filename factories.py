from abc import ABC, abstractmethod

from data_reader import ExcelDataReader


class DataReaderFactory(ABC):
    """
    Abstract factory for creating data readers.
    """

    @abstractmethod
    def create_reader(self):
        pass


class ExcelDataReaderFactory(DataReaderFactory):
    """
    Factory for creating Excel data readers.
    """

    def create_reader(self):
        return ExcelDataReader()
