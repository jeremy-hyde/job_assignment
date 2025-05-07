from src.execute import execute_simulation
from src.parser import parse_args


def main():
    field, car = parse_args()
    print(format(field))
    print(format(car))
    print("".join(car.command_list), end="\n\n")
    car = execute_simulation(field, car)
    print(format(car))
