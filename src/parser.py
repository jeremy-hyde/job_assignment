import argparse

from src.schemas import Car, Field


def parse_args():
    cli_instructions = """No input text provided.
        Your input must consists of 3 lines. 
        The fist line indicates the width and height of the field. 
        The second line indicates the current position and facing direction of the car. 
        The last line shows the subsequent commands it will execute. 

        For example:
        10 10
        1 2 N
        FFRFFFRRLF
        """

    parser = argparse.ArgumentParser(description="Auto Driving Car Simulation")
    parser.add_argument("text", nargs="?", default=None, help=cli_instructions)

    args = parser.parse_args()

    if args.text is None:
        parser.error(cli_instructions)

    dimensions, start_position, commands = parse_lines(parser, args.text)
    width, height = parse_dimensions(parser, dimensions)
    x, y, direction = parse_start_position(parser, start_position)
    command_list = parse_commands(parser, commands)
    check_starting_conditions(parser, width, height, x, y)

    field = Field(width=width, height=height)
    car = Car(x=x, y=y, direction=direction, command_list=command_list)

    return field, car


def parse_lines(parser, text: str) -> tuple[str, str, str]:
    try:
        dimensions, start_position, commands = text.split("\n")
    except Exception:
        parser.error("")

    return dimensions, start_position, commands


def parse_dimensions(parser, dimensions: str) -> tuple[int, int]:
    try:
        width, height = list(map(int, dimensions.strip().split()))
    except Exception:
        parser.error("Dimensions must be int => 10 10")

    return width, height


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
