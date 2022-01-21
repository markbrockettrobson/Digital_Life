from unittest import TestCase

from digital_life.src.data_types.entity import Entity
from digital_life.src.data_types.location import Location
from digital_life.src.data_types.world import World


class TestWorld(TestCase):
    def setUp(self) -> None:
        self._height = 1000
        self._width = 2000
        self._world = World(height=self._height, width=self._width)

    def test_init_sets_height(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(self._world.height, self._height)

    def test_init_sets_width(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(self._world.width, self._width)

    def test_init_starts_with_no_entities(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(len(self._world.get_entities()), 0)

    def test_init_starts_with_no_entities_with_location(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(
            len(
                self._world.get_entities_overlapping_location(
                    Location(left=0, right=self._width, top=self._height, bottom=0)
                )
            ),
            0,
        )

    def test_init_add_entity(self):
        # Arrange
        test_location = Location(left=10, right=10, top=20, bottom=20)
        entity = Entity(test_location)
        # Act
        self._world.add_entity(entity)
        # Assert
        self.assertEqual(len(self._world.get_entities()), 1)
        self.assertSetEqual(self._world.get_entities(), {entity})

    def test_init_add_entities(self):
        # Arrange
        count = 100
        test_location = Location(left=10, right=10, top=20, bottom=20)
        mock_entities = [Entity(test_location) for _ in range(count)]

        # Act
        for mock_entity in mock_entities:
            self._world.add_entity(mock_entity)

        # Assert
        self.assertEqual(len(self._world.get_entities()), count)
        self.assertSetEqual(self._world.get_entities(), set(mock_entities))

    def test_entity_deleted(self):
        # Arrange
        test_location = Location(left=10, right=10, top=20, bottom=20)
        entity = Entity(test_location)
        self._world.add_entity(entity)

        # Act
        entity.delete()

        # Assert
        self.assertEqual(len(self._world.get_entities()), 0)

    def test_del_entities(self):
        # Arrange
        count = 100
        test_location = Location(left=10, right=10, top=20, bottom=20)
        entities = [Entity(test_location) for _ in range(count)]
        for entity in entities:
            self._world.add_entity(entity)
        # Act
        for _entity in entities[::2]:
            _entity.delete()
        # Assert
        self.assertEqual(len(self._world.get_entities()), count / 2)
        self.assertSetEqual(self._world.get_entities(), set(entities[1::2]))

    def test_entity_location_updated(self):
        # Arrange
        test_location_one = Location(left=10, right=10, top=20, bottom=20)
        test_location_two = Location(left=40, right=40, top=50, bottom=50)
        entity = Entity(test_location_one)
        self._world.add_entity(entity)

        # Act
        entity.location = test_location_two

        # Assert
        self.assertEqual(len(self._world.get_entities_overlapping_location(test_location_one)), 0)
        self.assertEqual(len(self._world.get_entities_overlapping_location(test_location_two)), 1)
        self.assertSetEqual(self._world.get_entities_overlapping_location(test_location_two), {entity})

    def test_entities_overlapping_location_no_entity_inside(self):
        # Arrange
        test_location_one = Location(left=10, right=10, top=20, bottom=20)
        test_location_two = Location(left=40, right=40, top=50, bottom=50)
        entity = Entity(test_location_one)
        self._world.add_entity(entity)

        # Act
        # Assert
        self.assertEqual(len(self._world.get_entities_overlapping_location(test_location_two)), 0)

    def test_entities_overlapping_location_one_entity_inside(self):
        # Arrange
        world = World(height=self._height, width=self._width)

        test_location_one = Location(left=35, right=35, bottom=20, top=20)
        test_location_two = Location(left=30, right=40, bottom=20, top=30)
        entity = Entity(test_location_one)
        world.add_entity(entity)

        # Act
        # Assert
        self.assertEqual(len(world.get_entities_overlapping_location(test_location_two)), 1)
        self.assertSetEqual(world.get_entities_overlapping_location(test_location_two), {entity})

    def test_entities_overlapping_location_one_of_many_entities_inside(self):
        # Arrange
        count = 10
        test_location_one = Location(left=35, right=35, bottom=30, top=35)
        test_location_two = Location(left=30, right=40, bottom=20, top=30)
        test_location_three = Location(left=50, right=55, bottom=40, top=45)
        entity = Entity(test_location_one)
        entities = [Entity(test_location_three) for _ in range(count)]

        for _entity in entities:
            self._world.add_entity(_entity)
        self._world.add_entity(entity)

        # Act
        # Assert
        self.assertEqual(len(self._world.get_entities_overlapping_location(test_location_two)), 1)
        self.assertSetEqual(self._world.get_entities_overlapping_location(test_location_two), {entity})

    def test_entities_overlapping_location_some_of_many_entities_inside(self):
        # Arrange
        count = 10

        test_location_one = Location(left=35, right=35, bottom=30, top=35)
        test_location_two = Location(left=30, right=40, bottom=20, top=30)
        test_location_three = Location(left=50, right=55, bottom=40, top=45)
        entities = [Entity(test_location_three) for _ in range(count)]

        for entity in entities[::2]:
            self._world.add_entity(entity)
        for entity in entities[1::2]:
            entity.location = test_location_one
            self._world.add_entity(entity)

        # Act
        # Assert
        self.assertEqual(len(self._world.get_entities_overlapping_location(test_location_two)), count / 2)
        self.assertSetEqual(self._world.get_entities_overlapping_location(test_location_two), set(entities[1::2]))
