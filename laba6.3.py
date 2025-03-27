from enum import Enum, auto
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import random
import time


class FlightStatus(Enum):
    SCHEDULED = auto()
    BOARDING = auto()
    DEPARTED = auto()
    ARRIVED = auto()
    DELAYED = auto()
    CANCELLED = auto()


class RunwayStatus(Enum):
    FREE = auto()
    IN_USE = auto()
    MAINTENANCE = auto()


class GateStatus(Enum):
    FREE = auto()
    OCCUPIED = auto()
    MAINTENANCE = auto()


class AircraftType(Enum):
    BOEING_737 = "Boeing 737"
    AIRBUS_A320 = "Airbus A320"
    BOEING_777 = "Boeing 777"
    AIRBUS_A380 = "Airbus A380"


class Passenger:
    def __init__(self, name: str, passport: str, ticket_class: str):
        self.name = name
        self.passport = passport
        self.ticket_class = ticket_class
        self.boarding_pass = None

    def __str__(self):
        return f"{self.name} ({self.passport}), класс: {self.ticket_class}"


class Flight:
    def __init__(self, number: str, airline: str, aircraft_type: AircraftType,
                 origin: str, destination: str, departure_time: datetime,
                 arrival_time: datetime, capacity: int):
        self.number = number
        self.airline = airline
        self.aircraft_type = aircraft_type
        self.origin = origin
        self.destination = destination
        self.scheduled_departure = departure_time
        self.scheduled_arrival = arrival_time
        self.actual_departure = None
        self.actual_arrival = None
        self.status = FlightStatus.SCHEDULED
        self.capacity = capacity
        self.passengers: List[Passenger] = []
        self.gate = None
        self.runway = None

    def add_passenger(self, passenger: Passenger):
        if len(self.passengers) < self.capacity:
            self.passengers.append(passenger)
            return True
        return False

    def board(self):
        if self.status == FlightStatus.SCHEDULED:
            self.status = FlightStatus.BOARDING
            print(f"Рейс {self.number}: началась посадка")

    def depart(self):
        if self.status == FlightStatus.BOARDING:
            self.status = FlightStatus.DEPARTED
            self.actual_departure = datetime.now()
            print(f"Рейс {self.number}: вылетел")

    def arrive(self):
        self.status = FlightStatus.ARRIVED
        self.actual_arrival = datetime.now()
        print(f"Рейс {self.number}: прибыл")

    def delay(self, minutes: int):
        self.status = FlightStatus.DELAYED
        self.scheduled_departure += timedelta(minutes=minutes)
        self.scheduled_arrival += timedelta(minutes=minutes)
        print(f"Рейс {self.number}: задержан на {minutes} минут")

    def __str__(self):
        return (f"Рейс {self.number} {self.airline} ({self.aircraft_type.value})\n"
                f"Из: {self.origin} в {self.destination}\n"
                f"Время: {self.scheduled_departure.strftime('%H:%M')} - "
                f"{self.scheduled_arrival.strftime('%H:%M')}\n"
                f"Статус: {self.status.name}, Пассажиров: {len(self.passengers)}/{self.capacity}")


class Gate:
    def __init__(self, number: str):
        self.number = number
        self.status = GateStatus.FREE
        self.current_flight = None

    def assign_flight(self, flight: Flight):
        if self.status == GateStatus.FREE:
            self.current_flight = flight
            self.status = GateStatus.OCCUPIED
            flight.gate = self
            return True
        return False

    def release(self):
        self.current_flight = None
        self.status = GateStatus.FREE

    def __str__(self):
        status = f"Статус: {self.status.name}"
        if self.current_flight:
            status += f", Рейс: {self.current_flight.number}"
        return f"Гейт {self.number}: {status}"


class Runway:
    def __init__(self, number: str, length: int):
        self.number = number
        self.length = length
        self.status = RunwayStatus.FREE
        self.current_flight = None

    def assign_flight(self, flight: Flight):
        if self.status == RunwayStatus.FREE:
            self.current_flight = flight
            self.status = RunwayStatus.IN_USE
            flight.runway = self
            return True
        return False

    def release(self):
        self.current_flight = None
        self.status = RunwayStatus.FREE

    def __str__(self):
        status = f"Статус: {self.status.name}"
        if self.current_flight:
            status += f", Рейс: {self.current_flight.number}"
        return f"Полоса {self.number} ({self.length}m): {status}"


class Terminal:
    def __init__(self, name: str):
        self.name = name
        self.gates: List[Gate] = []

    def add_gate(self, gate: Gate):
        self.gates.append(gate)

    def find_free_gate(self) -> Optional[Gate]:
        for gate in self.gates:
            if gate.status == GateStatus.FREE:
                return gate
        return None

    def __str__(self):
        gates_info = "\n".join(str(gate) for gate in self.gates)
        return f"Терминал {self.name}:\n{gates_info}"


class Airport:
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code
        self.terminals: List[Terminal] = []
        self.runways: List[Runway] = []
        self.flights: List[Flight] = []
        self.passengers: Dict[str, Passenger] = {}

    def add_terminal(self, terminal: Terminal):
        self.terminals.append(terminal)

    def add_runway(self, runway: Runway):
        self.runways.append(runway)

    def schedule_flight(self, flight: Flight):
        self.flights.append(flight)
        print(f"Рейс {flight.number} добавлен в расписание")

    def assign_gate(self, flight: Flight) -> bool:
        for terminal in self.terminals:
            gate = terminal.find_free_gate()
            if gate and gate.assign_flight(flight):
                print(f"Рейсу {flight.number} назначен гейт {gate.number}")
                return True
        print(f"Нет свободных гейтов для рейса {flight.number}")
        return False

    def assign_runway(self, flight: Flight) -> bool:
        for runway in self.runways:
            if runway.status == RunwayStatus.FREE:
                if runway.assign_flight(flight):
                    print(f"Рейсу {flight.number} назначена полоса {runway.number}")
                    return True
        print(f"Нет свободных полос для рейса {flight.number}")
        return False

    def process_flights(self):
        print("\nОбработка рейсов...")
        now = datetime.now()

        for flight in self.flights:
            # Проверка на начало посадки (за 40 минут до вылета)
            if (flight.status == FlightStatus.SCHEDULED and
                    flight.scheduled_departure - timedelta(minutes=40) <= now <= flight.scheduled_departure):
                flight.board()

            # Проверка на вылет (время вылета)
            elif (flight.status == FlightStatus.BOARDING and
                  flight.scheduled_departure <= now):
                if self.assign_runway(flight):
                    flight.depart()

            # Проверка на прибытие (время прибытия + случайный фактор)
            elif (flight.status == FlightStatus.DEPARTED and
                  flight.scheduled_arrival <= now):
                flight.arrive()
                if flight.gate:
                    flight.gate.release()
                if flight.runway:
                    flight.runway.release()

            # Случайная задержка рейса (10% вероятность)
            elif (flight.status == FlightStatus.SCHEDULED and
                  random.random() < 0.1 and
                  flight.scheduled_departure - timedelta(minutes=30) <= now <= flight.scheduled_departure):
                flight.delay(random.randint(15, 120))

    def generate_random_passenger(self):
        first_names = ["Иван", "Алексей", "Екатерина", "Мария", "Дмитрий"]
        last_names = ["Иванов", "Петров", "Сидоров", "Смирнова", "Кузнецова"]
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        passport = f"{random.randint(1000, 9999)} {random.randint(100000, 999999)}"
        ticket_class = random.choice(["Economy", "Business", "First"])
        passenger = Passenger(name, passport, ticket_class)
        self.passengers[passport] = passenger
        return passenger

    def board_passengers(self):
        for flight in self.flights:
            if flight.status == FlightStatus.BOARDING:
                # Добавляем случайное количество пассажиров (50-100% вместимости)
                num_passengers = random.randint(flight.capacity // 2, flight.capacity)
                for _ in range(num_passengers):
                    passenger = self.generate_random_passenger()
                    flight.add_passenger(passenger)
                print(f"На рейс {flight.number} зарегистрировано {len(flight.passengers)} пассажиров")

    def print_status(self):
        print(f"\n=== Статус аэропорта {self.name} ({self.code}) ===")
        print(f"Всего рейсов: {len(self.flights)}")
        print(f"Всего пассажиров: {len(self.passengers)}")

        print("\nТерминалы:")
        for terminal in self.terminals:
            print(terminal)

        print("\nВзлетные полосы:")
        for runway in self.runways:
            print(runway)

        print("\nБлижайшие рейсы:")
        now = datetime.now()
        upcoming_flights = sorted(
            [f for f in self.flights if f.scheduled_departure >= now],
            key=lambda x: x.scheduled_departure
        )[:5]

        for flight in upcoming_flights:
            print(flight)
            print("---")


def create_sample_airport():
    # Создаем аэропорт
    airport = Airport("Шереметьево", "SVO")

    # Добавляем терминалы и гейты
    terminal_a = Terminal("A")
    for i in range(1, 6):
        terminal_a.add_gate(Gate(f"A{i}"))
    airport.add_terminal(terminal_a)

    terminal_b = Terminal("B")
    for i in range(1, 8):
        terminal_b.add_gate(Gate(f"B{i}"))
    airport.add_terminal(terminal_b)

    # Добавляем взлетные полосы
    airport.add_runway(Runway("06L/24R", 3700))
    airport.add_runway(Runway("06R/24L", 3550))
    airport.add_runway(Runway("07L/25R", 3200))

    # Создаем несколько рейсов
    now = datetime.now()

    # Вылетающие рейсы
    flights_data = [
        ("SU 123", "Аэрофлот", AircraftType.AIRBUS_A320, "SVO", "LED", 0, 90, 180),
        ("SU 456", "Аэрофлот", AircraftType.BOEING_777, "SVO", "JFK", 30, 600, 350),
        ("U6 789", "Уральские авиалинии", AircraftType.BOEING_737, "SVO", "KZN", 60, 120, 160),
        ("TK 321", "Turkish Airlines", AircraftType.AIRBUS_A380, "SVO", "IST", 90, 180, 500),
        ("DL 987", "Delta Airlines", AircraftType.BOEING_777, "SVO", "ATL", 120, 720, 300)
    ]

    for i, (number, airline, aircraft, origin, dest, dep_delta, arr_delta, cap) in enumerate(flights_data):
        departure = now + timedelta(minutes=dep_delta)
        arrival = departure + timedelta(minutes=arr_delta)
        flight = Flight(number, airline, aircraft, origin, dest, departure, arrival, cap)
        airport.schedule_flight(flight)

        # Назначаем гейт для рейса
        if i % 2 == 0:
            airport.assign_gate(flight)

    return airport


def main():
    airport = create_sample_airport()

    # Имитация работы аэропорта
    print("Запуск симуляции работы аэропорта...")

    for _ in range(10):  # 10 циклов симуляции
        airport.print_status()
        airport.process_flights()
        airport.board_passengers()
        time.sleep(5)  # Пауза между циклами симуляции

    print("\nСимуляция завершена")


if __name__ == "__main__":
    main()