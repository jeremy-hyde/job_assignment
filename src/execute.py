from src.schemas import Car, Field


def execute_simulation_one_car(field: Field, car: Car) -> Car:
    for command in car.command_list:
        if command == "F":
            if car.is_move_valid_for_field(field):
                car.move()
        else:  # R or L
            car.change_direction(command)

    return car


def execute_simulation_multiples_cars(field: Field, cars: list[Car]) -> str:
    for step, _ in enumerate(max(map(lambda x: x.command_list, cars))):
        for car in cars:
            command = car.command_list[step]
            if command == "F":
                if car.is_move_valid_for_field(field):
                    car.move()
                    if other_car_id := car.collision_with_car(cars):
                        return f"{other_car_id} {car.id}\n{car.x} {car.y}\n{step + 1}"
            else:  # R or L
                car.change_direction(command)

    return "no collision"
