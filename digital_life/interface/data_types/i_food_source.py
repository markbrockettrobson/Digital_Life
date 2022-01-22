from abc import abstractmethod
from typing import Callable

from digital_life.interface.data_types.i_entity import IEntity


class IFoodSource(IEntity):
    @property
    @abstractmethod
    def energy(self) -> float:
        pass

    @energy.setter
    def energy(self, value: float):
        # See: https://github.com/python/mypy/issues/4165
        raise NotImplementedError

    @abstractmethod
    def add_on_update_energy_action(self, action: Callable[["IFoodSource", float], None]):
        pass
