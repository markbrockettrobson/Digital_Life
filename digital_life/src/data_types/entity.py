from typing import Callable, List, Optional
from uuid import UUID, uuid4

from digital_life.interface.data_types.i_entity import IEntity
from digital_life.src.data_types.location import Location


class Entity(IEntity):
    def __init__(self, location: Location, identifier: Optional[UUID] = None) -> None:
        if identifier is None:
            identifier = uuid4()
        self._identifier = identifier
        self._location = location
        self._on_update_location_actions: List[Callable[[IEntity, Location], None]] = []
        self._pre_del_actions: List[Callable[[IEntity], None]] = []

    @property
    def identifier(self) -> UUID:
        return self._identifier

    @property
    def location(self) -> Location:
        return self._location

    @location.setter
    def location(self, value: Location) -> None:
        for action in self._on_update_location_actions:
            action(self, value)
        self._location = value

    def add_on_update_location_action(self, action: Callable[[IEntity, Location], None]):
        self._on_update_location_actions.append(action)

    def add_pre_del_action(self, action: Callable[[IEntity], None]):
        self._pre_del_actions.append(action)

    def delete(self):
        for action in self._pre_del_actions:
            action(self)
        del self
