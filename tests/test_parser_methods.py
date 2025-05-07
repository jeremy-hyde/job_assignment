import sys

import pytest

from src.parser import (
    check_starting_conditions,
    parse_car_id,
    parse_commands,
    parse_dimensions,
    parse_lines,
    parse_start_position,
)


@pytest.fixture
def parser_mock():
    return type("MockParser", (), {"error": lambda x: sys.exit(1)})


class TestParserLines:
    def test_parse_lines_valid(self, parser_mock):
        # Test valid input with 3 lines
        text = "10 10\n1 2 N\nFRLF"
        dimensions, start_position, commands = parse_lines(parser_mock, text)

        assert dimensions == "10 10"
        assert start_position == "1 2 N"
        assert commands == "FRLF"

    def test_parse_lines_invalid(self, parser_mock):
        # Test with insufficient lines
        with pytest.raises(SystemExit):
            parse_lines(parser_mock, "10 10\n1 2 N")

        # Test with excess lines (should split into first 3)
        with pytest.raises(SystemExit):
            parse_lines(parser_mock, "10 10\n1 2 N\nFRLF\nextra")


class TestParserDimensions:
    def test_parse_dimensions_valid(self, parser_mock):
        # Test valid dimensions
        width, height = parse_dimensions(parser_mock, "10 10")
        assert width == 10
        assert height == 10

        # Test with leading/trailing whitespace
        width, height = parse_dimensions(parser_mock, "  5 7  ")
        assert width == 5
        assert height == 7

    def test_parse_dimensions_invalid_format(self, parser_mock):
        # Test non-numeric values
        with pytest.raises(SystemExit):
            parse_dimensions(parser_mock, "a 10")

        # Test incorrect number of values
        with pytest.raises(SystemExit):
            parse_dimensions(parser_mock, "10")

        with pytest.raises(SystemExit):
            parse_dimensions(parser_mock, "10 20 30")

        # Test invalid format
        with pytest.raises(SystemExit):
            parse_dimensions(parser_mock, "10,20")


class TestParseCarId:
    def test_parse_car_id_valid(self, parser_mock):
        # Test valid car IDs
        assert parse_car_id(parser_mock, "A") == "A"
        assert parse_car_id(parser_mock, "B") == "B"
        assert parse_car_id(parser_mock, "Z") == "Z"

    def test_parse_car_id_invalid(self, parser_mock):
        # Test non-single letter IDs
        with pytest.raises(SystemExit):
            parse_car_id(parser_mock, "AB")

        # Test non-uppercase letters
        with pytest.raises(SystemExit):
            parse_car_id(parser_mock, "a")

        # Test numbers
        with pytest.raises(SystemExit):
            parse_car_id(parser_mock, "1")

        # Test special characters
        with pytest.raises(SystemExit):
            parse_car_id(parser_mock, "*")


class TestParserStartPosition:
    def test_parse_start_position_valid(self, parser_mock):
        # Test valid positions and directions
        x, y, direction = parse_start_position(parser_mock, "1 2 N")
        assert x == 1
        assert y == 2
        assert direction == "N"

        x, y, direction = parse_start_position(parser_mock, "0 0 S")
        assert x == 0
        assert y == 0
        assert direction == "S"

        # Test with whitespace
        x, y, direction = parse_start_position(parser_mock, "  5 7 W  ")
        assert x == 5
        assert y == 7
        assert direction == "W"

    def test_parse_start_position_invalid(self, parser_mock):
        # Test invalid coordinates
        with pytest.raises(SystemExit):
            parse_start_position(parser_mock, "a 2 N")

        with pytest.raises(SystemExit):
            parse_start_position(parser_mock, "1 b N")

        # Test invalid direction
        with pytest.raises(SystemExit):
            parse_start_position(parser_mock, "1 2 X")

        # Test incorrect number of values
        with pytest.raises(SystemExit):
            parse_start_position(parser_mock, "1 2")

        with pytest.raises(SystemExit):
            parse_start_position(parser_mock, "1 2 N E")


class TestParserCommands:
    def test_parse_commands_valid(self, parser_mock):
        # Test valid commands
        commands = parse_commands(parser_mock, "FRL")
        assert commands == ["F", "R", "L"]

        commands = parse_commands(parser_mock, "FFRFFFRRLF")
        assert commands == ["F", "F", "R", "F", "F", "F", "R", "R", "L", "F"]

        # Test with whitespace
        commands = parse_commands(parser_mock, "  FRL  ")
        assert commands == ["F", "R", "L"]

    def test_parse_commands_invalid(self, parser_mock):
        # Test invalid commands
        with pytest.raises(SystemExit):
            parse_commands(parser_mock, "FRXL")

        with pytest.raises(SystemExit):
            parse_commands(parser_mock, "123")

        with pytest.raises(SystemExit):
            parse_commands(parser_mock, "FR L")


class TestStartingConditions:
    def test_check_starting_conditions_valid(self, parser_mock):
        # Test positions inside field
        # For a 10x10 field (width=10, height=10), valid coordinates are 0-9
        check_starting_conditions(parser_mock, 10, 10, 0, 0)  # bottom-left corner
        check_starting_conditions(parser_mock, 10, 10, 9, 9)  # top-right corner
        check_starting_conditions(parser_mock, 10, 10, 5, 5)  # middle

        # Specifically testing edges
        check_starting_conditions(parser_mock, 10, 10, 0, 9)  # top-left
        check_starting_conditions(parser_mock, 10, 10, 9, 0)  # bottom-right

        # Test valid field sizes
        check_starting_conditions(parser_mock, 1, 1, 0, 0)  # minimum field size
        check_starting_conditions(parser_mock, 100, 200, 50, 100)  # large field

    def test_check_starting_conditions_invalid_starting_position(self, parser_mock):
        # Test positions outside field
        # For a 10x10 field (width=10, height=10), invalid coordinates are < 0 or > 9
        with pytest.raises(SystemExit):
            check_starting_conditions(parser_mock, 10, 10, -1, 5)  # left of field

        with pytest.raises(SystemExit):
            check_starting_conditions(parser_mock, 10, 10, 5, -1)  # below field

        with pytest.raises(SystemExit):
            check_starting_conditions(parser_mock, 10, 10, 10, 5)  # right of field

        with pytest.raises(SystemExit):
            check_starting_conditions(parser_mock, 10, 10, 5, 10)  # above field

        # Test extreme positions
        with pytest.raises(SystemExit):
            check_starting_conditions(parser_mock, 10, 10, 100, 100)  # far outside

    def test_check_starting_conditions_invalid_field(self, parser_mock):
        # Test invalid field dimensions
        with pytest.raises(SystemExit):
            check_starting_conditions(parser_mock, 0, 10, 0, 0)  # zero width

        with pytest.raises(SystemExit):
            check_starting_conditions(parser_mock, 10, 0, 0, 0)  # zero height

        with pytest.raises(SystemExit):
            check_starting_conditions(parser_mock, -5, 10, 0, 0)  # negative width

        with pytest.raises(SystemExit):
            check_starting_conditions(parser_mock, 10, -5, 0, 0)  # negative height
