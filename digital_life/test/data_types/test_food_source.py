from unittest import TestCase
from unittest.mock import Mock
from uuid import uuid4

from digital_life.src.data_types.food_source import FoodSource


class TestFoodSource(TestCase):
    def test_init_sets_location(self):
        # Arrange
        mock_location = Mock()
        energy = 30

        # Act
        food_source = FoodSource(location=mock_location, energy=energy)

        # Assert
        self.assertEqual(food_source.location, mock_location)

    def test_init_sets_identifier(self):
        # Arrange
        mock_location = Mock()
        identifier = uuid4()
        energy = 30

        # Act
        food_source = FoodSource(location=mock_location, identifier=identifier, energy=energy)

        # Assert
        self.assertEqual(food_source.identifier, identifier)

    def test_init_sets_energy(self):
        # Arrange
        mock_location = Mock()
        identifier = uuid4()
        energy = 30

        # Act
        food_source = FoodSource(location=mock_location, identifier=identifier, energy=energy)

        # Assert
        self.assertEqual(food_source.energy, energy)

    def test_init_creates_new_identifier(self):
        # Arrange
        mock_location = Mock()
        energy = 30

        # Act
        food_source_one = FoodSource(location=mock_location, energy=energy)
        food_source_two = FoodSource(location=mock_location, energy=energy)

        # Assert
        self.assertNotEqual(food_source_one.identifier, food_source_two.identifier)

    def test_set_location(self):
        # Arrange
        mock_location_one = Mock()
        mock_location_two = Mock()
        energy = 30
        food_source = FoodSource(location=mock_location_one, energy=energy)

        # Act
        food_source.location = mock_location_two

        # Assert
        self.assertEqual(food_source.location, mock_location_two)

    def test_on_update_location_action(self):
        # Arrange
        mock_location_one = Mock()
        mock_location_two = Mock()

        mock_action_one = Mock()
        mock_action_two = Mock()

        energy = 30
        food_source = FoodSource(location=mock_location_one, energy=energy)
        food_source.add_on_update_location_action(
            lambda updated_entity, new_location: mock_action_one(updated_entity, updated_entity.location, new_location)
        )
        food_source.add_on_update_location_action(
            lambda updated_entity, new_location: mock_action_two(updated_entity, updated_entity.location, new_location)
        )

        # Act
        food_source.location = mock_location_two

        # Assert
        self.assertEqual(food_source.location, mock_location_two)
        mock_action_one.assert_called_once_with(food_source, mock_location_one, mock_location_two)
        mock_action_two.assert_called_once_with(food_source, mock_location_one, mock_location_two)

    def test_set_energy(self):
        # Arrange
        mock_location = Mock()
        energy = 30
        food_source = FoodSource(location=mock_location, energy=energy)

        # Act
        food_source.energy = 40

        # Assert
        self.assertEqual(food_source.energy, 40)

    def test_on_update_energy_action(self):
        # Arrange
        mock_location = Mock()

        mock_action_one = Mock()
        mock_action_two = Mock()

        energy = 30
        food_source = FoodSource(location=mock_location, energy=energy)
        food_source.add_on_update_energy_action(
            lambda updated_entity, new_energy: mock_action_one(updated_entity, updated_entity.energy, new_energy)
        )
        food_source.add_on_update_energy_action(
            lambda updated_entity, new_energy: mock_action_two(updated_entity, updated_entity.energy, new_energy)
        )

        # Act
        food_source.energy = 40

        # Assert
        self.assertEqual(food_source.energy, 40)
        mock_action_one.assert_called_once_with(food_source, energy, 40)
        mock_action_two.assert_called_once_with(food_source, energy, 40)

    def test_pre_del_action(self):
        # Arrange
        mock_location = Mock()

        mock_action_one = Mock()
        mock_action_two = Mock()

        energy = 30
        food_source = FoodSource(location=mock_location, energy=energy)
        food_source.add_pre_del_action(lambda updated_entity: mock_action_one(updated_entity.identifier))
        food_source.add_pre_del_action(lambda updated_entity: mock_action_two(updated_entity.identifier))

        identifier = food_source.identifier
        location = food_source.location
        # Act
        food_source.delete()

        # Assert
        self.assertEqual(location, mock_location)
        mock_action_one.assert_called_once_with(identifier)
        mock_action_two.assert_called_once_with(identifier)
