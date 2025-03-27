from collections import defaultdict


class Flower:
    # Словари с ценами для каждого типа цветка и размера
    PRICES = {
        'роза': {'маленький': 100, 'средний': 150, 'большой': 200},
        'ромашка': {'маленький': 50, 'средний': 75, 'большой': 100},
        'ирис': {'маленький': 80, 'средний': 120, 'большой': 160}
    }

    # Доступные цвета для каждого типа цветка
    AVAILABLE_COLORS = {
        'роза': ['красный', 'розовый', 'желтый'],
        'ромашка': ['белый', 'желтый', 'розовый'],
        'ирис': ['фиолетовый', 'синий', 'желтый']
    }

    def __init__(self, flower_type, color, bud_size):
        if flower_type not in self.PRICES:
            raise ValueError(f"Неизвестный тип цветка: {flower_type}")
        if color not in self.AVAILABLE_COLORS[flower_type]:
            raise ValueError(f"Недопустимый цвет для {flower_type}: {color}")
        if bud_size not in self.PRICES[flower_type]:
            raise ValueError(f"Недопустимый размер бутона: {bud_size}")

        self.flower_type = flower_type
        self.color = color
        self.bud_size = bud_size
        self.price = self.PRICES[flower_type][bud_size]

    def __str__(self):
        return f"{self.flower_type.capitalize()} ({self.color}, {self.bud_size}): {self.price} руб."


class Bouquet:
    def __init__(self):
        self.flowers = []
        self.total_price = 0

    def add_flower(self, flower, quantity=1):
        for _ in range(quantity):
            self.flowers.append(flower)
            self.total_price += flower.price

    def get_summary(self):
        summary = defaultdict(int)
        for flower in self.flowers:
            key = (flower.flower_type, flower.color, flower.bud_size)
            summary[key] += 1

        result = []
        for (flower_type, color, bud_size), count in summary.items():
            price_per_unit = Flower.PRICES[flower_type][bud_size]
            result.append(f"{count} x {flower_type} ({color}, {bud_size}) - {price_per_unit} руб./шт.")

        result.append(f"\nИтого в букете: {len(self.flowers)} цветов")
        result.append(f"Общая стоимость букета: {self.total_price} руб.")
        return "\n".join(result)

    def __str__(self):
        return self.get_summary()


class FlowerShop:
    def __init__(self):
        self.current_bouquet = None
        self.bouquets = []

    def start_new_bouquet(self):
        self.current_bouquet = Bouquet()
        print("\nНачато создание нового букета")

    def add_flowers_to_bouquet(self):
        if not self.current_bouquet:
            print("Сначала начните новый букет!")
            return

        while True:
            try:
                print("\nДоступные цветы:")
                print("1. Роза (красный, розовый, желтый)")
                print("2. Ромашка (белый, желтый, розовый)")
                print("3. Ирис (фиолетовый, синий, желтый)")

                choice = input("Выберите тип цветка (1-3) или 'готово' для завершения: ")
                if choice.lower() == 'готово':
                    break

                flower_types = ['роза', 'ромашка', 'ирис']
                flower_type = flower_types[int(choice) - 1]

                colors = Flower.AVAILABLE_COLORS[flower_type]
                print(f"Доступные цвета для {flower_type}: {', '.join(colors)}")
                color = input("Выберите цвет: ")

                print("Доступные размеры бутона: маленький, средний, большой")
                bud_size = input("Выберите размер бутона: ")

                quantity = int(input("Введите количество таких цветов: "))

                flower = Flower(flower_type, color, bud_size)
                self.current_bouquet.add_flower(flower, quantity)

                print(f"Добавлено {quantity} {flower_type}(ов) {color} цвета, размер {bud_size}")
                print(f"Текущая стоимость букета: {self.current_bouquet.total_price} руб.")

            except (ValueError, IndexError) as e:
                print(f"Ошибка: {e}. Попробуйте еще раз.")

    def finish_bouquet(self):
        if not self.current_bouquet:
            print("Нет активного букета для завершения!")
            return

        self.bouquets.append(self.current_bouquet)
        print("\nБукет завершен:")
        print(self.current_bouquet)
        self.current_bouquet = None

    def show_all_bouquets(self):
        if not self.bouquets:
            print("Еще не создано ни одного букета.")
            return

        print("\nВсе созданные букеты:")
        for i, bouquet in enumerate(self.bouquets, 1):
            print(f"\nБукет #{i}:")
            print(bouquet)

        total_flowers = sum(len(b.flowers) for b in self.bouquets)
        total_price = sum(b.total_price for b in self.bouquets)
        print(f"\nОбщее количество цветов во всех букетах: {total_flowers}")
        print(f"Общая стоимость всех букетов: {total_price} руб.")


def main():
    shop = FlowerShop()

    while True:
        print("\nМеню цветочного магазина:")
        print("1. Начать новый букет")
        print("2. Добавить цветы в текущий букет")
        print("3. Завершить текущий букет")
        print("4. Показать все созданные букеты")
        print("5. Выйти")

        choice = input("Выберите действие (1-5): ")

        if choice == '1':
            shop.start_new_bouquet()
        elif choice == '2':
            shop.add_flowers_to_bouquet()
        elif choice == '3':
            shop.finish_bouquet()
        elif choice == '4':
            shop.show_all_bouquets()
        elif choice == '5':
            print("Спасибо за посещение нашего магазина!")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите от 1 до 5.")





if __name__ == "__main__":
    main()