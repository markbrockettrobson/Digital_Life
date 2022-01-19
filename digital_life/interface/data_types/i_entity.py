from abc import ABC, abstractmethod
from typing import Callable
from uuid import UUID

from digital_life.src.data_types.location import Location


class IEntity(ABC):
    @property
    @abstractmethod
    def identifier(self) -> UUID:
        pass

    @property
    @abstractmethod
    def location(self) -> Location:
        pass

    @location.setter
    def location(self, value: Location):
        # See: https://github.com/python/mypy/issues/4165
        raise NotImplementedError

    @abstractmethod
    def add_on_update_location_action(self, action: Callable[["IEntity", Location], None]):
        pass

    @abstractmethod
    def add_pre_del_action(self, action: Callable[["IEntity"], None]):
        pass
