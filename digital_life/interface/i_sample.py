from abc import ABCMeta, abstractmethod


class ISample(ABCMeta):
    @staticmethod
    @abstractmethod
    def add_one(value: int) -> int:
        pass
