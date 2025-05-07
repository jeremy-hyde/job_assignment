import argparse
import string

from src.schemas import Car, Field


def parse_args():
    part1_instructions = """
        Your input must consists of 3 lines. 
        The fist line indicates the width and height of the field. 
        The second line indicates the current position and facing direction of the car. 
        The last line shows the subsequent commands it will execute. 

        For example:
        10 10
        1 2 N
        FFRFFFRRLF
        """

    part2_instructions = """
        Your input must consist of field dimensions followed by multiple car definitions.
        The first line indicates the width and height of the field.
        Then, for each car, you need to provide:
        - A blank line
        - The car's identifier (a single letter)
        - The car's starting position and direction (x y direction)
        - The car's command sequence
        
        For example:
        10 10

        A
        1 2 N
        FFRFFFRRLF

        B
        7 8 W
        FFLFFFFFFFF
        """

    parser = argparse.ArgumentParser(description="Auto Driving Car Simulation")
    parser.add_argument("text", nargs="?", default=None, help="Input text")
    parser.add_argument(
        "-p",
        "--part",
        type=int,
        choices=[1, 2],
        required=True,
        help="Define the functioning mode: 1 or 2",
    )

    args = parser.parse_args()

    if args.text is None:
        if args.part == 1:
            parser.error(part1_instructions)
        else:
            parser.error(part2_instructions)

    if args.part == 1:
        return parse_part1(parser, args.text)
    else:
        return parse_part2(parser, args.text)


def parse_part1(parser, text):
    """Parse input for Part 1 with a single car."""
    dimensions, start_position, commands = parse_lines(parser, text)
    width, height = parse_dimensions(parser, dimensions)
    x, y, direction = parse_start_position(parser, start_position)
    command_list = parse_commands(parser, commands)
    check_starting_conditions(parser, width, height, x, y)

    field = Field(width=width, height=height)
    car = Car(id="A", x=x, y=y, direction=direction, command_list=command_list)

    return field, [car]


def parse_part2(parser, text):
    """Parse input for Part 2 with multiple cars."""
    try:
        lines = text.strip().split("\n")

        # Parse field dimensions from first line
        width, height = parse_dimensions(parser, lines[0])
        field = Field(width=width, height=height)

        # Remove the first line
        lines = lines[1:]
        cars = []
        # Parse cars four lines at a time
        for i in range(0, len(lines), 4):
            chunk = lines[i : i + 4]
            # Each car definition should be 4 lines:
            # Empty line, ID, position, commands
            if len(chunk) != 4:
                parser.error("Incomplete car definition")

            car_id = parse_car_id(parser, chunk[1].strip())
            x, y, direction = parse_start_position(parser, chunk[2].strip())
            command_list = parse_commands(parser, chunk[3].strip())
            check_starting_conditions(parser, width, height, x, y)

            car = Car(id=car_id, x=x, y=y, direction=direction, command_list=command_list)
            cars.append(car)

        if not cars:
            parser.error("No cars defined in the input")

        return field, cars

    except Exception:
        parser.error("Error parsing Part 2")


def parse_lines(parser, text: str) -> tuple[str, str, str]:
    try:
        dimensions, start_position, commands = text.split("\n")
    except Exception:
        parser.error("Error parsing input lines")

    return dimensions, start_position, commands


def parse_dimensions(parser, dimensions: str) -> tuple[int, int]:
    try:
        width, height = list(map(int, dimensions.strip().split()))
    except Exception:
        parser.error("Dimensions must be int => 10 10")

    return width, height


def parse_car_id(parser, car_id: str) -> str:
    try:
        if len(car_id) != 1 or car_id not in string.ascii_uppercase:
            raise ValueError()
    except Exception:
        parser.error("Car ID must be a single character")

    return car_id


def parse_start_position(parser, start_position: str) -> tuple[int, int, str]:
    try:
        result = start_position.strip().split()
        if len(result) != 3:
            raise ValueError()

        x = int(result[0])
        y = int(result[1])
        if result[2] in ["N", "W", "S", "E"]:
            direction = result[2]
        else:
            raise ValueError()
    except Exception:
        parser.error(
            "Start Position must have the format => x y direction, where x, y are int and direction one of N, W, S, E"
        )

    return x, y, direction


def parse_commands(parser, commands: str) -> list[str]:
    try:
        command_list = []
        for command in commands.strip():
            if command not in ["F", "R", "L"]:
                raise ValueError()
            command_list.append(command)

    except Exception:
        parser.error("The commands must have the format => XXX where each X is one of F, R, L")

    return command_list


def check_starting_conditions(parser, width, height, x, y):
    if width <= 0 or height <= 0:
        parser.error("The field is invalid")

    if 0 > x or x > width - 1 or 0 > y or y > height - 1:
        parser.error("The starting position must be in the field")
