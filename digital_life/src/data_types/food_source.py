from typing import Callable, List, Optional
from uuid import UUID

from digital_life.interface.data_types.i_food_source import IFoodSource
from digital_life.src.data_types.entity import Entity
from digital_life.src.data_types.location import Location


class FoodSource(IFoodSource, Entity):
    def __init__(self, energy: float, location: Location, identifier: Optional[UUID] = None) -> None:
        super().__init__(location=location, identifier=identifier)
        self._energy = energy
        self._update_energy_actions: List[Callable[[IFoodSource, float], None]] = []

    @property
    def energy(self) -> float:
        return self._energy

    @energy.setter
    def energy(self, value: float):
        for action in self._update_energy_actions:
            action(self, value)
        self._energy = value

    def add_on_update_energy_action(self, action: Callable[[IFoodSource, float], None]):
        self._update_energy_actions.append(action)
