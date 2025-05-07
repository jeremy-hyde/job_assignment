import pytest

from src.execute import execute_simulation_multiples_cars, execute_simulation_one_car
from src.schemas import Car, Field


@pytest.fixture
def field():
    return Field(width=5, height=5)


class TestMoveMultiplesCars:
    def test_no_collision(self, field):
        car1 = Car(id="A", x=0, y=0, direction="N", command_list=["F", "F"])
        car2 = Car(id="B", x=2, y=0, direction="N", command_list=["F", "F"])

        result = execute_simulation_multiples_cars(field, [car1, car2])
        assert result == "no collision"
        assert car1.y == 2
        assert car1.x == 0
        assert car2.y == 2
        assert car2.x == 2

    def test_collision_detection(self, field):
        car1 = Car(id="A", x=0, y=0, direction="E", command_list=["F", "F"])
        car2 = Car(id="B", x=1, y=1, direction="S", command_list=["F", "F"])

        result = execute_simulation_multiples_cars(field, [car1, car2])
        assert result == "A B\n1 0\n1"

    def test_sample_from_instructions(self):
        field = Field(width=10, height=10)
        car1 = Car(
            id="A",
            x=1,
            y=2,
            direction="N",
            command_list=["F", "F", "R", "F", "F", "F", "F", "R", "R", "L"],
        )
        car2 = Car(
            id="B",
            x=7,
            y=8,
            direction="W",
            command_list=["F", "F", "L", "F", "F", "F", "F", "F", "F", "F"],
        )

        result = execute_simulation_multiples_cars(field, [car1, car2])
        assert result == "A B\n5 4\n7"

    def test_boundary_collision(self, field):
        car1 = Car(id="A", x=0, y=0, direction="N", command_list=["F", "F"])
        car2 = Car(id="B", x=0, y=2, direction="S", command_list=["F", "F"])

        result = execute_simulation_multiples_cars(field, [car1, car2])
        assert result == "A B\n0 1\n1"

    def test_three_cars_no_collision(self, field):
        car1 = Car(id="A", x=0, y=0, direction="N", command_list=["F", "F"])
        car2 = Car(id="B", x=2, y=0, direction="N", command_list=["F", "F"])
        car3 = Car(id="C", x=4, y=0, direction="N", command_list=["F", "F"])

        result = execute_simulation_multiples_cars(field, [car1, car2, car3])
        assert result == "no collision"
        assert car1.y == 2
        assert car1.x == 0
        assert car2.y == 2
        assert car2.x == 2
        assert car3.y == 2
        assert car3.x == 4

    def test_three_cars_with_collision(self, field):
        car1 = Car(id="A", x=0, y=0, direction="E", command_list=["F", "F", "F"])
        car2 = Car(id="B", x=2, y=1, direction="N", command_list=["F", "F", "F"])
        car3 = Car(id="C", x=3, y=0, direction="W", command_list=["F", "F", "F"])

        result = execute_simulation_multiples_cars(field, [car1, car2, car3])
        assert result == "C A\n2 0\n2"


class TestMoveOneCar:
    def test_basic_forward_movement(self, field):
        car = Car(id="A", x=2, y=2, direction="W", command_list=["F"])

        result = execute_simulation_one_car(field, car)
        assert result.y == 2
        assert result.x == 1
        assert result.direction == "W"

    def test_multiple_forward_movements(self, field):
        car = Car(id="A", x=0, y=0, direction="N", command_list=["F", "F", "F"])

        result = execute_simulation_one_car(field, car)
        assert result.y == 3
        assert result.x == 0
        assert result.direction == "N"

    def test_rotation_commands(self, field):
        car = Car(id="A", x=2, y=2, direction="N", command_list=["R", "L"])

        result = execute_simulation_one_car(field, car)
        assert result.y == 2  # Position shouldn't change
        assert result.x == 2  # Position shouldn't change
        assert result.direction == "N"  # After R then L, should face original direction

    def test_combined_movement_and_rotation(self, field):
        car = Car(id="A", x=0, y=0, direction="N", command_list=["F", "R", "F"])

        result = execute_simulation_one_car(field, car)
        assert result.y == 1
        assert result.x == 1
        assert result.direction == "E"

    def test_prevent_moving_outside_field_north(self, field):
        car = Car(id="A", x=2, y=4, direction="N", command_list=["F"])

        result = execute_simulation_one_car(field, car)
        assert result.y == 4  # Should not move past the northern boundary
        assert result.x == 2
        assert result.direction == "N"

    def test_prevent_moving_outside_field_south(self, field):
        car = Car(id="A", x=2, y=0, direction="S", command_list=["F"])

        result = execute_simulation_one_car(field, car)
        assert result.y == 0  # Should not move past the southern boundary
        assert result.x == 2
        assert result.direction == "S"

    def test_prevent_moving_outside_field_east(self, field):
        car = Car(id="A", x=4, y=2, direction="E", command_list=["F"])

        result = execute_simulation_one_car(field, car)
        assert result.y == 2
        assert result.x == 4  # Should not move past the eastern boundary
        assert result.direction == "E"

    def test_prevent_moving_outside_field_west(self, field):
        car = Car(id="A", x=0, y=2, direction="W", command_list=["F"])

        result = execute_simulation_one_car(field, car)
        assert result.y == 2
        assert result.x == 0  # Should not move past the western boundary
        assert result.direction == "W"

    def test_complex_movement_pattern(self, field):
        car = Car(id="A", x=0, y=0, direction="N", command_list=["F", "R", "F", "R", "F", "L", "F"])

        result = execute_simulation_one_car(field, car)
        assert result.y == 0
        assert result.x == 2
        assert result.direction == "E"

    def test_empty_command_list(self, field):
        car = Car(id="A", x=2, y=2, direction="N", command_list=[])

        result = execute_simulation_one_car(field, car)
        assert result.y == 2
        assert result.x == 2
        assert result.direction == "N"

    def test_full_rotation(self, field):
        car = Car(id="A", x=2, y=2, direction="N", command_list=["R", "R", "R", "R"])

        result = execute_simulation_one_car(field, car)
        assert result.y == 2
        assert result.x == 2
        assert result.direction == "N"  # Should complete a full 360° rotation
