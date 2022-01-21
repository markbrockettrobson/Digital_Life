from unittest import TestCase
from unittest.mock import Mock
from uuid import uuid4

from digital_life.src.data_types.entity import Entity


class TestEntity(TestCase):
    def test_init_sets_location(self):
        # Arrange
        mock_location = Mock()

        # Act
        entity = Entity(location=mock_location)

        # Assert
        self.assertEqual(entity.location, mock_location)

    def test_init_sets_identifier(self):
        # Arrange
        mock_location = Mock()
        identifier = uuid4()

        # Act
        entity = Entity(location=mock_location, identifier=identifier)

        # Assert
        self.assertEqual(entity.identifier, identifier)

    def test_init_creates_new_identifier(self):
        # Arrange
        mock_location = Mock()

        # Act
        entity_one = Entity(location=mock_location)
        entity_two = Entity(location=mock_location)

        # Assert
        self.assertNotEqual(entity_one.identifier, entity_two.identifier)

    def test_set_location(self):
        # Arrange
        mock_location_one = Mock()
        mock_location_two = Mock()
        entity = Entity(location=mock_location_one)

        # Act
        entity.location = mock_location_two

        # Assert
        self.assertEqual(entity.location, mock_location_two)

    def test_on_update_location_action(self):
        # Arrange
        mock_location_one = Mock()
        mock_location_two = Mock()

        mock_action_one = Mock()
        mock_action_two = Mock()

        entity = Entity(location=mock_location_one)
        entity.add_on_update_location_action(
            lambda updated_entity, new_location: mock_action_one(updated_entity, updated_entity.location, new_location)
        )
        entity.add_on_update_location_action(
            lambda updated_entity, new_location: mock_action_two(updated_entity, updated_entity.location, new_location)
        )

        # Act
        entity.location = mock_location_two

        # Assert
        self.assertEqual(entity.location, mock_location_two)
        mock_action_one.assert_called_once_with(entity, mock_location_one, mock_location_two)
        mock_action_two.assert_called_once_with(entity, mock_location_one, mock_location_two)

    def test_pre_del_action(self):
        # Arrange
        mock_location = Mock()

        mock_action_one = Mock()
        mock_action_two = Mock()

        entity = Entity(location=mock_location)
        entity.add_pre_del_action(lambda updated_entity: mock_action_one(updated_entity.identifier))
        entity.add_pre_del_action(lambda updated_entity: mock_action_two(updated_entity.identifier))

        identifier = entity.identifier
        location = entity.location
        # Act
        entity.delete()

        # Assert
        self.assertEqual(location, mock_location)
        mock_action_one.assert_called_once_with(identifier)
        mock_action_two.assert_called_once_with(identifier)
