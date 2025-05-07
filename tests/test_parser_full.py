import sys

import pytest

from src.parser import (
    Car,
    Field,
    parse_args,
    parse_part1,
    parse_part2,
)


@pytest.fixture
def parser_mock():
    return type("MockParser", (), {"error": lambda x: sys.exit(1)})


class TestArgParser:
    def test_parse_args_no_args(self, monkeypatch):
        # Test with no arguments provided
        test_args = ["program"]
        monkeypatch.setattr("sys.argv", test_args)

        with pytest.raises(SystemExit):
            parse_args()

    def test_parse_args_part1(self, monkeypatch):
        # Set up mock command line arguments
        test_args = ["program", "-p", "1", "10 10\n1 2 N\nFRLF"]
        monkeypatch.setattr("sys.argv", test_args)

        # Call the function
        field, cars = parse_args()

        # Verify the results
        assert isinstance(field, Field)
        assert field.width == 10
        assert field.height == 10

        assert len(cars) == 1
        car = cars[0]
        assert isinstance(car, Car)
        assert car.x == 1
        assert car.y == 2
        assert car.direction == "N"
        assert car.command_list == ["F", "R", "L", "F"]

    def test_parse_args_part2(self, monkeypatch):
        # Set up mock command line arguments for part 2
        test_input = """10 10
        
        A
        1 2 N
        FRLF
        
        B
        5 5 E
        RRFF"""
        test_args = ["program", "-p", "2", test_input]
        monkeypatch.setattr("sys.argv", test_args)

        # Call the function
        field, cars = parse_args()

        # Verify the results
        assert isinstance(field, Field)
        assert field.width == 10
        assert field.height == 10

        assert len(cars) == 2

        # Check first car
        assert cars[0].id == "A"
        assert cars[0].x == 1
        assert cars[0].y == 2
        assert cars[0].direction == "N"
        assert cars[0].command_list == ["F", "R", "L", "F"]

        # Check second car
        assert cars[1].id == "B"
        assert cars[1].x == 5
        assert cars[1].y == 5
        assert cars[1].direction == "E"
        assert cars[1].command_list == ["R", "R", "F", "F"]


class TestParserPart1:
    def test_parse_part1_valid(self, parser_mock):
        # Test valid input for part 1
        text = "10 10\n1 2 N\nFRLF"
        field, cars = parse_part1(parser_mock, text)

        # Verify field
        assert isinstance(field, Field)
        assert field.width == 10
        assert field.height == 10

        # Verify car
        assert len(cars) == 1
        car = cars[0]
        assert isinstance(car, Car)
        assert car.id == "A"  # Default ID for part 1
        assert car.x == 1
        assert car.y == 2
        assert car.direction == "N"
        assert car.command_list == ["F", "R", "L", "F"]

    def test_parse_part1_invalid_dimensions(self, parser_mock):
        # Test invalid dimensions
        with pytest.raises(SystemExit):
            parse_part1(parser_mock, "a b\n1 2 N\nFRLF")

    def test_parse_part1_invalid_position(self, parser_mock):
        # Test invalid position
        with pytest.raises(SystemExit):
            parse_part1(parser_mock, "10 10\n1 b N\nFRLF")

    def test_parse_part1_invalid_commands(self, parser_mock):
        # Test invalid commands
        with pytest.raises(SystemExit):
            parse_part1(parser_mock, "10 10\n1 2 N\nFRXL")

    def test_parse_part1_position_outside_field(self, parser_mock):
        # Test position outside field
        with pytest.raises(SystemExit):
            parse_part1(parser_mock, "5 5\n10 10 N\nFRLF")


class TestParserPart2:
    def test_parse_part2_valid(self, parser_mock):
        # Test valid input for part 2
        text = """10 10
        
        A
        1 2 N
        FRLF
        
        B
        5 5 E
        RRFF"""
        field, cars = parse_part2(parser_mock, text)

        # Verify field
        assert isinstance(field, Field)
        assert field.width == 10
        assert field.height == 10

        # Verify cars list
        assert isinstance(cars, list)
        assert len(cars) == 2

        # Check first car
        assert cars[0].id == "A"
        assert cars[0].x == 1
        assert cars[0].y == 2
        assert cars[0].direction == "N"
        assert cars[0].command_list == ["F", "R", "L", "F"]

        # Check second car
        assert cars[1].id == "B"
        assert cars[1].x == 5
        assert cars[1].y == 5
        assert cars[1].direction == "E"
        assert cars[1].command_list == ["R", "R", "F", "F"]

    def test_parse_part2_single_car(self, parser_mock):
        # Test part 2 with only one car
        text = """10 10
        
        A
        1 2 N
        FRLF"""
        field, cars = parse_part2(parser_mock, text)

        # Verify results
        assert field.width == 10
        assert field.height == 10
        assert len(cars) == 1
        assert cars[0].id == "A"
        assert cars[0].x == 1
        assert cars[0].y == 2
        assert cars[0].direction == "N"
        assert cars[0].command_list == ["F", "R", "L", "F"]

    def test_parse_part2_invalid_dimensions(self, parser_mock):
        # Test invalid dimensions
        text = """a b
        
        A
        1 2 N
        FRLF"""
        with pytest.raises(SystemExit):
            parse_part2(parser_mock, text)

    def test_parse_part2_invalid_car_id(self, parser_mock):
        # Test invalid car ID
        text = """10 10
        
        123
        1 2 N
        FRLF"""
        with pytest.raises(SystemExit):
            parse_part2(parser_mock, text)

    def test_parse_part2_invalid_position(self, parser_mock):
        # Test invalid position
        text = """10 10
        
        A
        1 b N
        FRLF"""
        with pytest.raises(SystemExit):
            parse_part2(parser_mock, text)

    def test_parse_part2_invalid_commands(self, parser_mock):
        # Test invalid commands
        text = """10 10
        
        A
        1 2 N
        FRXL"""
        with pytest.raises(SystemExit):
            parse_part2(parser_mock, text)

    def test_parse_part2_position_outside_field(self, parser_mock):
        # Test position outside field
        text = """5 5
        
        A
        10 10 N
        FRLF"""
        with pytest.raises(SystemExit):
            parse_part2(parser_mock, text)

    def test_parse_part2_no_cars(self, parser_mock):
        # Test with no cars defined
        text = "10 10"
        with pytest.raises(SystemExit):
            parse_part2(parser_mock, text)

    def test_parse_part2_incomplete_car_definition(self, parser_mock):
        # Test with incomplete car definition
        text = """10 10
        
        A
        1 2 N"""
        with pytest.raises(SystemExit):
            parse_part2(parser_mock, text)
