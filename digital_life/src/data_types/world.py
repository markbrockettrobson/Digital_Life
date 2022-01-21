from typing import Dict, Set

from rtree import Rtree  # type: ignore

from digital_life.interface.data_types.i_entity import IEntity
from digital_life.interface.data_types.i_world import IWorld
from digital_life.src.data_types.location import Location


class World(IWorld):
    def __init__(self, height: float, width: float):
        self._width = width
        self._height = height
        self._index_to_entities: Dict[int, IEntity] = {}
        self._entities_to_index: Dict[IEntity, int] = {}
        self._r_tee = Rtree()
        self._next_index = 0

    @property
    def height(self) -> float:
        return self._height

    @property
    def width(self) -> float:
        return self._width

    def add_entity(self, entity: IEntity) -> None:
        self._add_entity(entity=entity, location=entity.location)
        entity.add_pre_del_action(self._on_entity_delete)
        entity.add_on_update_location_action(self._on_entity_location_update)

    def _add_entity(self, entity: IEntity, location: Location) -> None:
        self._index_to_entities[self._next_index] = entity
        self._entities_to_index[entity] = self._next_index
        self._r_tee.insert(self._next_index, (location.left, location.bottom, location.right, location.top))
        self._next_index += 1

    def remove_entity(self, entity: IEntity) -> None:
        index = self._entities_to_index[entity]
        del self._index_to_entities[index]
        del self._entities_to_index[entity]
        self._r_tee.delete(
            index, (entity.location.left, entity.location.bottom, entity.location.right, entity.location.top)
        )

    def get_entities_overlapping_location(self, location: Location) -> Set[IEntity]:
        return set(
            self._index_to_entities[index]
            for index in self._r_tee.intersection((location.left, location.bottom, location.right, location.top))
        )

    def get_entities(self) -> Set[IEntity]:
        return set(self._entities_to_index.keys())

    def _on_entity_location_update(self, entity: IEntity, new_location: Location):
        self.remove_entity(entity=entity)
        self._add_entity(entity=entity, location=new_location)

    def _on_entity_delete(self, entity: IEntity):
        self.remove_entity(entity=entity)
