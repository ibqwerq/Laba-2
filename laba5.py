from enum import Enum, auto
import random
from typing import List, Dict


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    STOPPED = auto()


class DoorState(Enum):
    OPEN = auto()
    CLOSED = auto()


class ElevatorStatus(Enum):
    WORKING = auto()
    BROKEN = auto()


class Elevator:
    def __init__(self, elevator_id: int, max_floor: int):
        self.id = elevator_id
        self.max_floor = max_floor
        self.current_floor = 1
        self.direction = Direction.STOPPED
        self.door_state = DoorState.CLOSED
        self.status = ElevatorStatus.WORKING

    def move(self):
        """Логика движения лифта"""
        if self.status == ElevatorStatus.BROKEN:
            return

        if self.door_state == DoorState.OPEN:
            return

        if self.direction == Direction.UP:
            if self.current_floor < self.max_floor:
                self.current_floor += 1
            else:
                self.direction = Direction.STOPPED
        elif self.direction == Direction.DOWN:
            if self.current_floor > 1:
                self.current_floor -= 1
            else:
                self.direction = Direction.STOPPED

    def set_direction(self, direction: Direction):
        """Установка направления движения"""
        if self.status == ElevatorStatus.BROKEN:
            return False

        if direction == Direction.DOWN and self.current_floor == 1:
            return False
        if direction == Direction.UP and self.current_floor == self.max_floor:
            return False

        self.direction = direction
        return True

    def toggle_door(self):
        """Открытие/закрытие дверей"""
        if self.status == ElevatorStatus.BROKEN:
            return False

        if self.direction != Direction.STOPPED:
            return False

        self.door_state = DoorState.OPEN if self.door_state == DoorState.CLOSED else DoorState.CLOSED
        return True

    def force_open_door(self):
        """Принудительное открытие дверей"""
        if self.status == ElevatorStatus.BROKEN:
            return False

        self.direction = Direction.STOPPED
        self.door_state = DoorState.OPEN
        return True

    def force_close_door(self):
        """Принудительное закрытие дверей"""
        if self.status == ElevatorStatus.BROKEN:
            return False

        self.door_state = DoorState.CLOSED
        return True

    def return_to_first_floor(self):
        """Возврат на первый этаж"""
        if self.status == ElevatorStatus.BROKEN:
            return False

        if self.current_floor > 1:
            self.direction = Direction.DOWN
            self.door_state = DoorState.CLOSED
        elif self.current_floor < 1:
            self.direction = Direction.UP
            self.door_state = DoorState.CLOSED
        else:
            self.direction = Direction.STOPPED
        return True

    def break_down(self):
        """Поломка лифта"""
        self.status = ElevatorStatus.BROKEN
        self.direction = Direction.STOPPED

    def repair(self):
        """Ремонт лифта"""
        self.status = ElevatorStatus.WORKING

    def __str__(self):
        status = "Работает" if self.status == ElevatorStatus.WORKING else "Сломан"
        direction = {
            Direction.UP: "↑",
            Direction.DOWN: "↓",
            Direction.STOPPED: "="
        }[self.direction]
        door = "Открыты" if self.door_state == DoorState.OPEN else "Закрыты"
        return (f"Лифт #{self.id}: {status}, этаж {self.current_floor}/{self.max_floor}, "
                f"направление: {direction}, двери: {door}")


class Building:
    def __init__(self, address: str, coordinates: tuple, floors: int, elevators_count: int):
        self.address = address
        self.coordinates = coordinates
        self.floors = floors
        self.elevators: List[Elevator] = []

        # Создаем лифты для здания
        for i in range(1, elevators_count + 1):
            self.elevators.append(Elevator(i, floors))

    def update_elevators(self):
        """Обновление состояния всех лифтов"""
        for elevator in self.elevators:
            # Случайная поломка лифта (5% шанс)
            if random.random() < 0.05 and elevator.status == ElevatorStatus.WORKING:
                elevator.break_down()

            elevator.move()

    def return_all_to_first_floor(self):
        """Возврат всех лифтов на первый этаж"""
        for elevator in self.elevators:
            if elevator.status == ElevatorStatus.WORKING:
                elevator.return_to_first_floor()
                elevator.force_open_door()

    def get_elevator(self, elevator_id: int) -> Elevator:
        """Получение лифта по ID"""
        for elevator in self.elevators:
            if elevator.id == elevator_id:
                return elevator
        raise ValueError(f"Лифт с ID {elevator_id} не найден")

    def __str__(self):
        return (f"Здание по адресу: {self.address}, координаты: {self.coordinates}, "
                f"этажей: {self.floors}, лифтов: {len(self.elevators)}")


class Operator:
    def __init__(self):
        self.buildings: Dict[str, Building] = {}

    def add_building(self, building: Building):
        """Добавление здания в систему"""
        self.buildings[building.address] = building

    def update_system(self):
        """Обновление состояния системы"""
        for building in self.buildings.values():
            building.update_elevators()

    def show_buildings(self):
        """Показать список зданий"""
        print("\nСписок зданий:")
        for address, building in self.buildings.items():
            print(f"- {address} ({building.floors} этажей, {len(building.elevators)} лифтов)")

    def show_elevators(self, address: str):
        """Показать состояние лифтов в здании"""
        building = self.buildings.get(address)
        if not building:
            print("Здание не найдено")
            return

        print(f"\nСостояние лифтов в здании {address}:")
        for elevator in building.elevators:
            print(elevator)

    def stop_elevator(self, address: str, elevator_id: int):
        """Остановка лифта"""
        building = self.buildings.get(address)
        if not building:
            print("Здание не найдено")
            return

        try:
            elevator = building.get_elevator(elevator_id)
            if elevator.status == ElevatorStatus.WORKING:
                elevator.direction = Direction.STOPPED
                print(f"Лифт #{elevator_id} остановлен")
            else:
                print(f"Лифт #{elevator_id} сломан и не может быть остановлен")
        except ValueError as e:
            print(e)

    def return_elevator_to_first_floor(self, address: str, elevator_id: int):
        """Возврат лифта на первый этаж"""
        building = self.buildings.get(address)
        if not building:
            print("Здание не найдено")
            return

        try:
            elevator = building.get_elevator(elevator_id)
            if elevator.status == ElevatorStatus.WORKING:
                if elevator.return_to_first_floor():
                    print(f"Лифт #{elevator_id} возвращается на первый этаж")
                else:
                    print(f"Лифт #{elevator_id} уже на первом этаже")
            else:
                print(f"Лифт #{elevator_id} сломан и не может быть перемещен")
        except ValueError as e:
            print(e)

    def open_elevator_doors(self, address: str, elevator_id: int):
        """Принудительное открытие дверей лифта"""
        building = self.buildings.get(address)
        if not building:
            print("Здание не найдено")
            return

        try:
            elevator = building.get_elevator(elevator_id)
            if elevator.force_open_door():
                print(f"Двери лифта #{elevator_id} открыты")
            else:
                print(f"Невозможно открыть двери лифта #{elevator_id}")
        except ValueError as e:
            print(e)

    def close_elevator_doors(self, address: str, elevator_id: int):
        """Принудительное закрытие дверей лифта"""
        building = self.buildings.get(address)
        if not building:
            print("Здание не найдено")
            return

        try:
            elevator = building.get_elevator(elevator_id)
            if elevator.force_close_door():
                print(f"Двери лифта #{elevator_id} закрыты")
            else:
                print(f"Невозможно закрыть двери лифта #{elevator_id}")
        except ValueError as e:
            print(e)

    def return_all_elevators(self, address: str):
        """Возврат всех лифтов здания на первый этаж"""
        building = self.buildings.get(address)
        if not building:
            print("Здание не найдено")
            return

        building.return_all_to_first_floor()
        print(f"Все лифты в здании {address} возвращены на первый этаж")


def main():
    # Создаем оператора
    operator = Operator()

    # Добавляем здания в систему
    building1 = Building("ул. Ленина, 10", (55.751244, 37.618423), 5, 2)
    building2 = Building("пр. Мира, 25", (55.755814, 37.617635), 9, 3)
    building3 = Building("ул. Пушкина, 15", (55.752725, 37.621026), 12, 4)

    operator.add_building(building1)
    operator.add_building(building2)
    operator.add_building(building3)

    # Пример работы оператора
    while True:
        print("\nМеню оператора:")
        print("1. Показать список зданий")
        print("2. Показать состояние лифтов в здании")
        print("3. Остановить лифт")
        print("4. Вернуть лифт на первый этаж")
        print("5. Открыть двери лифта")
        print("6. Закрыть двери лифта")
        print("7. Вернуть все лифты здания на первый этаж")
        print("8. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            operator.show_buildings()
        elif choice == "2":
            address = input("Введите адрес здания: ")
            operator.show_elevators(address)
        elif choice == "3":
            address = input("Введите адрес здания: ")
            elevator_id = int(input("Введите номер лифта: "))
            operator.stop_elevator(address, elevator_id)
        elif choice == "4":
            address = input("Введите адрес здания: ")
            elevator_id = int(input("Введите номер лифта: "))
            operator.return_elevator_to_first_floor(address, elevator_id)
        elif choice == "5":
            address = input("Введите адрес здания: ")
            elevator_id = int(input("Введите номер лифта: "))
            operator.open_elevator_doors(address, elevator_id)
        elif choice == "6":
            address = input("Введите адрес здания: ")
            elevator_id = int(input("Введите номер лифта: "))
            operator.close_elevator_doors(address, elevator_id)
        elif choice == "7":
            address = input("Введите адрес здания: ")
            operator.return_all_elevators(address)
        elif choice == "8":
            break
        else:
            print("Неверный выбор")

        # Обновляем состояние системы
        operator.update_system()


if __name__ == "__main__":
    main()