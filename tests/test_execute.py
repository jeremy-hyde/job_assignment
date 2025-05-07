import pytest

from src.execute import execute_simulation
from src.schemas import Car, Field


@pytest.fixture
def field():
    return Field(width=5, height=5)


class TestMove:
    def test_basic_forward_movement(self, field):
        car = Car(x=2, y=2, direction="W", command_list=["F"])

        result = execute_simulation(field, car)
        assert result.y == 2
        assert result.x == 1
        assert result.direction == "W"

    def test_multiple_forward_movements(self, field):
        car = Car(x=0, y=0, direction="N", command_list=["F", "F", "F"])

        result = execute_simulation(field, car)
        assert result.y == 3
        assert result.x == 0
        assert result.direction == "N"

    def test_rotation_commands(self, field):
        car = Car(x=2, y=2, direction="N", command_list=["R", "L"])

        result = execute_simulation(field, car)
        assert result.y == 2  # Position shouldn't change
        assert result.x == 2  # Position shouldn't change
        assert result.direction == "N"  # After R then L, should face original direction

    def test_combined_movement_and_rotation(self, field):
        car = Car(x=0, y=0, direction="N", command_list=["F", "R", "F"])

        result = execute_simulation(field, car)
        assert result.y == 1
        assert result.x == 1
        assert result.direction == "E"

    def test_prevent_moving_outside_field_north(self, field):
        car = Car(x=2, y=4, direction="N", command_list=["F"])

        result = execute_simulation(field, car)
        assert result.y == 4  # Should not move past the northern boundary
        assert result.x == 2
        assert result.direction == "N"

    def test_prevent_moving_outside_field_south(self, field):
        car = Car(x=2, y=0, direction="S", command_list=["F"])

        result = execute_simulation(field, car)
        assert result.y == 0  # Should not move past the southern boundary
        assert result.x == 2
        assert result.direction == "S"

    def test_prevent_moving_outside_field_east(self, field):
        car = Car(x=4, y=2, direction="E", command_list=["F"])

        result = execute_simulation(field, car)
        assert result.y == 2
        assert result.x == 4  # Should not move past the eastern boundary
        assert result.direction == "E"

    def test_prevent_moving_outside_field_west(self, field):
        car = Car(x=0, y=2, direction="W", command_list=["F"])

        result = execute_simulation(field, car)
        assert result.y == 2
        assert result.x == 0  # Should not move past the western boundary
        assert result.direction == "W"

    def test_complex_movement_pattern(self, field):
        car = Car(x=0, y=0, direction="N", command_list=["F", "R", "F", "R", "F", "L", "F"])

        result = execute_simulation(field, car)
        assert result.y == 0
        assert result.x == 2
        assert result.direction == "E"

    def test_empty_command_list(self, field):
        car = Car(x=2, y=2, direction="N", command_list=[])

        result = execute_simulation(field, car)
        assert result.y == 2
        assert result.x == 2
        assert result.direction == "N"

    def test_full_rotation(self, field):
        car = Car(x=2, y=2, direction="N", command_list=["R", "R", "R", "R"])

        result = execute_simulation(field, car)
        assert result.y == 2
        assert result.x == 2
        assert result.direction == "N"  # Should complete a full 360° rotation
