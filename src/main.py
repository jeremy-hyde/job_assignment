from src.execute import execute_simulation_multiples_cars, execute_simulation_one_car
from src.parser import parse_args


def main():
    field, cars = parse_args()

    if len(cars) == 1:
        car = execute_simulation_one_car(field, cars[0])
        print(format(car))
    else:
        result = execute_simulation_multiples_cars(field, cars)
        print(result)
