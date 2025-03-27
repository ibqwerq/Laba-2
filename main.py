class BankAccount:
    def __init__(self, account_number, owner_name, balance=0):
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Пополнение на {amount} руб. Баланс: {self.balance} руб.")
        else:
            print("Сумма пополнения должна быть положительной")

    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                print(f"Снятие {amount} руб. Баланс: {self.balance} руб.")
            else:
                print("Недостаточно средств на счете")
        else:
            print("Сумма снятия должна быть положительной")

    def get_balance(self):
        return self.balance

    def __str__(self):
        return f"Счет №{self.account_number}, Владелец: {self.owner_name}, Баланс: {self.balance} руб."


class PersonalAccount(BankAccount):
    def __init__(self, account_number, owner_name, balance=0):
        super().__init__(account_number, owner_name, balance)
        self.account_type = "Физическое лицо"
        self.interest_rate = 0.05  # 5% годовых

    def apply_interest(self):
        interest = self.balance * self.interest_rate / 12
        self.balance += interest
        print(f"Начислены проценты: {interest:.2f} руб. Баланс: {self.balance:.2f} руб.")

    def __str__(self):
        return super().__str__() + f", Тип: {self.account_type}, Процентная ставка: {self.interest_rate * 100}%"


class BusinessAccount(BankAccount):
    def __init__(self, account_number, owner_name, balance=0, company_name=None):
        super().__init__(account_number, owner_name, balance)
        self.account_type = "Юридическое лицо"
        self.company_name = company_name if company_name else owner_name
        self.transaction_fee = 10  # Комиссия за операцию

    def withdraw(self, amount):
        total_amount = amount + self.transaction_fee
        if self.balance >= total_amount:
            self.balance -= total_amount
            print(f"Снятие {amount} руб. + комиссия {self.transaction_fee} руб. Баланс: {self.balance} руб.")
        else:
            print("Недостаточно средств на счете (учитывая комиссию)")

    def __str__(self):
        return super().__str__() + f", Тип: {self.account_type}, Компания: {self.company_name}, Комиссия за операцию: {self.transaction_fee} руб."


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = []

    def create_personal_account(self, account_number, owner_name, initial_balance=0):
        account = PersonalAccount(account_number, owner_name, initial_balance)
        self.accounts.append(account)
        print(f"Создан новый личный счет для {owner_name}")
        return account

    def create_business_account(self, account_number, owner_name, company_name, initial_balance=0):
        account = BusinessAccount(account_number, owner_name, initial_balance, company_name)
        self.accounts.append(account)
        print(f"Создан новый бизнес-счет для компании {company_name}")
        return account

    def find_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None

    def display_all_accounts(self):
        print(f"\nВсе счета в банке '{self.name}':")
        for account in self.accounts:
            print(account)
        print()


# Демонстрация работы банка
def main():
    # Создаем банк
    my_bank = Bank("Национальный Банк")

    # Создаем счета для физических лиц
    acc1 = my_bank.create_personal_account("1001", "Иванов Иван Иванович", 1000)
    acc2 = my_bank.create_personal_account("1002", "Петрова Мария Сергеевна", 5000)

    # Создаем счета для юридических лиц
    acc3 = my_bank.create_business_account("2001", "ООО Ромашка", "ООО Ромашка", 50000)
    acc4 = my_bank.create_business_account("2002", "АО ТехноПром", "АО ТехноПром", 100000)

    # Операции со счетами
    print("\nОперации со счетами:")
    acc1.deposit(2000)
    acc1.withdraw(500)
    acc1.apply_interest()

    acc3.deposit(10000)
    acc3.withdraw(2000)  # Будет списана комиссия

    # Выводим информацию о всех счетах
    my_bank.display_all_accounts()


if __name__ == "__main__":
    main()