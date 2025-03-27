from enum import Enum, auto
from typing import List, Optional


class RunwayStatus(Enum):
    """Статусы взлетной полосы"""
    FREE = auto()  # Свободна
    IN_USE = auto()  # Занята (взлет/посадка)
    MAINTENANCE = auto()  # На обслуживании
    CLOSED = auto()  # Закрыта


class Runway:
    """Класс взлетной полосы"""

    def __init__(self, number: str, length: float, width: float = 45.0):
        """
        :param number: Номер полосы (например, "09L/27R")
        :param length: Длина полосы в метрах
        :param width: Ширина полосы в метрах (по умолчанию 45м)
        """
        self.number = number
        self.length = length
        self.width = width
        self.status = RunwayStatus.FREE
        self.current_flight = None  # Текущий рейс, использующий полосу

    def __str__(self) -> str:
        return (f"Полоса {self.number} ({self.length}x{self.width} м), "
                f"Статус: {self.status.name}, "
                f"Рейс: {self.current_flight if self.current_flight else 'нет'}")

    def allocate_for_flight(self, flight_number: str) -> bool:
        """Выделить полосу для рейса"""
        if self.status == RunwayStatus.FREE:
            self.status = RunwayStatus.IN_USE
            self.current_flight = flight_number
            print(f"Полоса {self.number} выделена для рейса {flight_number}")
            return True
        return False

    def release(self) -> None:
        """Освободить полосу"""
        if self.status == RunwayStatus.IN_USE:
            print(f"Полоса {self.number} освобождена от рейса {self.current_flight}")
            self.status = RunwayStatus.FREE
            self.current_flight = None

    def set_maintenance(self, in_maintenance: bool) -> None:
        """Установить/снять статус обслуживания"""
        if in_maintenance:
            self.status = RunwayStatus.MAINTENANCE
            self.current_flight = None
            print(f"Полоса {self.number} переведена на обслуживание")
        else:
            self.status = RunwayStatus.FREE
            print(f"Полоса {self.number} доступна для использования")


class Airport:
    """Класс аэропорта"""

    def __init__(self, name: str, iata_code: str):
        """
        :param name: Название аэропорта
        :param iata_code: Код ИАТА (3 буквы)
        """
        self.name = name
        self.iata_code = iata_code
        self.runways: List[Runway] = []

    def __str__(self) -> str:
        return f"Аэропорт {self.name} ({self.iata_code}), Полос: {len(self.runways)}"

    def add_runway(self, runway: Runway) -> None:
        """Добавить взлетную полосу в аэропорт"""
        self.runways.append(runway)
        print(f"Добавлена полоса {runway.number} в аэропорт {self.name}")

    def find_available_runway(self, min_length: float = 0) -> Optional[Runway]:
        """
        Найти свободную полосу, удовлетворяющую требованиям
        :param min_length: Минимальная требуемая длина полосы
        :return: Найденная полоса или None
        """
        for runway in self.runways:
            if (runway.status == RunwayStatus.FREE and
                    runway.length >= min_length):
                return runway
        return None

    def get_runway_status(self) -> str:
        """Получить статус всех полос"""
        status = []
        for runway in self.runways:
            status.append(str(runway))
        return "\n".join(status)

    def close_runway(self, runway_number: str) -> bool:
        """Закрыть полосу"""
        for runway in self.runways:
            if runway.number == runway_number:
                if runway.status != RunwayStatus.MAINTENANCE:
                    runway.status = RunwayStatus.CLOSED
                    runway.current_flight = None
                    print(f"Полоса {runway_number} закрыта")
                    return True
                print(f"Полоса {runway_number} уже на обслуживании")
                return False
        print(f"Полоса {runway_number} не найдена")
        return False

    def open_runway(self, runway_number: str) -> bool:
        """Открыть полосу"""
        for runway in self.runways:
            if runway.number == runway_number:
                if runway.status in (RunwayStatus.CLOSED, RunwayStatus.MAINTENANCE):
                    runway.status = RunwayStatus.FREE
                    print(f"Полоса {runway_number} открыта")
                    return True
                print(f"Полоса {runway_number} уже открыта")
                return False
        print(f"Полоса {runway_number} не найдена")
        return False


# Пример использования
if __name__ == "__main__":
    # Создаем аэропорт
    sheremetyevo = Airport("Шереметьево", "SVO")

    # Добавляем взлетные полосы
    runway1 = Runway("06L/24R", 3700, 60)
    runway2 = Runway("06R/24L", 3550)
    runway3 = Runway("07L/25R", 3200)

    sheremetyevo.add_runway(runway1)
    sheremetyevo.add_runway(runway2)
    sheremetyevo.add_runway(runway3)

    print("\nСтатус полос:")
    print(sheremetyevo.get_runway_status())

    # Имитация работы
    print("\nИмитация работы аэропорта:")

    # Найти свободную полосу для рейса
    flight_num = "SU 123"
    runway = sheremetyevo.find_available_runway(3500)
    if runway:
        runway.allocate_for_flight(flight_num)

    print("\nСтатус полос после выделения:")
    print(sheremetyevo.get_runway_status())

    # Освободить полосу
    runway.release()

    # Перевести полосу на обслуживание
    runway2.set_maintenance(True)

    print("\nСтатус полос после изменений:")
    print(sheremetyevo.get_runway_status())

    # Закрыть полосу
    sheremetyevo.close_runway("06L/24R")

    # Попытка найти полосу для большого самолета
    print("\nПоиск полосы длиной не менее 4000 м:")
    long_runway = sheremetyevo.find_available_runway(4000)
    if not long_runway:
        print("Подходящей полосы не найдено")

    # Открыть полосу обратно
    sheremetyevo.open_runway("06L/24R")

    print("\nФинальный статус полос:")
    print(sheremetyevo.get_runway_status())