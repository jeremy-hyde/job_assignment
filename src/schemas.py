from dataclasses import dataclass


@dataclass
class Field:
    width: int
    height: int

    def __format__(self, format_spec):
        return f"{self.width} {self.height}"


@dataclass
class Car:
    id: str
    x: int
    y: int
    direction: str
    command_list: list[str]

    def is_move_valid_for_field(self, field: Field) -> bool:
        if self.direction == "N" and self.y + 1 >= field.height:
            return False
        elif self.direction == "S" and self.y - 1 < 0:
            return False
        elif self.direction == "E" and self.x + 1 >= field.width:
            return False
        elif self.direction == "W" and self.x - 1 < 0:
            return False
        else:
            return True

    def collision_with_car(self, cars: list) -> bool:
        for car in cars:
            if self.id != car.id and (self.x, self.y) == (car.x, car.y):
                return car.id

        return None

    def move(self):
        if self.direction == "N":
            self.y += 1
        elif self.direction == "S":
            self.y -= 1
        elif self.direction == "E":
            self.x += 1
        elif self.direction == "W":
            self.x -= 1
        else:
            raise ValueError("Invalid direction")

    def change_direction(self, command: str):
        if command == "R":
            self.direction = {"N": "E", "E": "S", "S": "W", "W": "N"}[self.direction]
        elif command == "L":
            self.direction = {"N": "W", "W": "S", "S": "E", "E": "N"}[self.direction]
        else:
            raise ValueError("Invalid direction")

    def __format__(self, format_spec):
        return f"{self.x} {self.y} {self.direction}"
