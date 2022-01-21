from abc import ABC, abstractmethod
from typing import Set

from digital_life.interface.data_types.i_entity import IEntity
from digital_life.src.data_types.location import Location


class IWorld(ABC):
    @property
    @abstractmethod
    def height(self) -> float:
        pass

    @property
    @abstractmethod
    def width(self) -> float:
        pass

    @abstractmethod
    def add_entity(self, entity: IEntity) -> None:
        pass

    @abstractmethod
    def remove_entity(self, entity: IEntity) -> None:
        pass

    @abstractmethod
    def get_entities_overlapping_location(self, location: Location) -> Set[IEntity]:
        pass

    @abstractmethod
    def get_entities(self) -> Set[IEntity]:
        pass
