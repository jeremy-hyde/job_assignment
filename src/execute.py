def execute_simulation(field, car):
    for command in car.command_list:
        if command == "F":
            if car.is_move_valid_for_field(field):
                car.move()
        else:  # R or L
            car.change_direction(command)

    return car
