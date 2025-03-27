from abc import ABC, abstractmethod
from typing import List


class BankClient(ABC):
    def __init__(self, initial_deposit: float):
        self.balance = initial_deposit

    @abstractmethod
    def get_info(self) -> str:
        pass

    @abstractmethod
    def calculate_profit(self, months: int) -> float:
        pass

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self.balance += amount

    def get_balance(self) -> float:
        return self.balance


class Individual(BankClient):
    def __init__(self, full_name: str, passport: str, initial_deposit: float):
        super().__init__(initial_deposit)
        self.full_name = full_name
        self.passport = passport

    def get_info(self) -> str:
        return (f"Физ. лицо: {self.full_name}, "
                f"Паспорт: {self.passport}, "
                f"Баланс: {self.balance:.2f} руб.")

    def calculate_profit(self, months: int) -> float:
        annual_rate = 0.18  # 18% годовых
        return self.balance * (annual_rate / 12) * months


class LegalEntity(BankClient):
    def __init__(self, name: str, inn: str, legal_form: str, initial_deposit: float):
        super().__init__(initial_deposit)
        self.name = name
        self.inn = inn
        self.legal_form = legal_form

    def get_info(self) -> str:
        return (f"Юр. лицо: {self.name}, "
                f"ИНН: {self.inn}, "
                f"Форма: {self.legal_form}, "
                f"Баланс: {self.balance:.2f} руб.")

    def calculate_profit(self, months: int) -> float:
        annual_rate = 0.12  # 12% годовых
        return self.balance * (annual_rate / 12) * months


def input_client() -> BankClient:
    print("\nДобавление нового клиента")
    client_type = input("Выберите тип клиента (1 - физ. лицо, 2 - юр. лицо): ")

    initial_deposit = float(input("Введите начальную сумму вклада: "))

    if client_type == "1":
        full_name = input("Введите ФИО: ")
        passport = input("Введите паспортные данные: ")
        return Individual(full_name, passport, initial_deposit)
    elif client_type == "2":
        name = input("Введите название организации: ")
        inn = input("Введите ИНН: ")
        legal_form = input("Введите форму организации (ООО, ОАО, ИП и т.п.): ")
        return LegalEntity(name, inn, legal_form, initial_deposit)
    else:
        raise ValueError("Неверный тип клиента")


def main():
    clients: List[BankClient] = []

    print("Добро пожаловать в банковскую систему!")

    # Добавляем 3 клиентов
    clients.append(Individual("Иванов Иван Иванович", "1234 567890", 50000))
    clients.append(LegalEntity("ООО Ромашка", "1234567890", "ООО", 150000))
    clients.append(Individual("Петрова Мария Сергеевна", "0987 654321", 75000))

    # Пополнение счетов
    clients[0].deposit(10000)
    clients[1].deposit(50000)
    clients[2].deposit(25000)

    # Сортировка клиентов по сумме вклада (по убыванию)
    sorted_clients = sorted(clients, key=lambda x: x.get_balance(), reverse=True)

    # Вывод информации о клиентах
    print("\nСписок клиентов, отсортированный по сумме вклада:")
    for i, client in enumerate(sorted_clients, 1):
        months = 12  # Расчет прибыли за 12 месяцев
        profit = client.calculate_profit(months)
        print(f"\n{i}. {client.get_info()}")
        print(f"Прибыль за {months} месяцев: {profit:.2f} руб.")


if __name__ == "__main__":
    main()