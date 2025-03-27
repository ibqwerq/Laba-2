from abc import ABC, abstractmethod
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


class Shape(ABC):
    def __init__(self, points):
        self.points = points

    @abstractmethod
    def area(self):
        pass

    def __str__(self):
        points_str = ", ".join(str(point) for point in self.points)
        return f"{self.__class__.__name__} [Точки: {points_str}]"


class Circle(Shape):
    def __init__(self, center, radius_point):
        super().__init__([center, radius_point])
        self.center = center
        self.radius = math.sqrt((radius_point.x - center.x) ** 2 + (radius_point.y - center.y) ** 2)

    def area(self):
        return math.pi * self.radius ** 2

    def __str__(self):
        return f"Circle [Центр: {self.center}, Радиус: {self.radius:.2f}]"


class Triangle(Shape):
    def area(self):
        if len(self.points) != 3:
            raise ValueError("Треугольник должен иметь 3 точки")

        a, b, c = self.points
        # Формула Герона
        ab = math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)
        bc = math.sqrt((c.x - b.x) ** 2 + (c.y - b.y) ** 2)
        ca = math.sqrt((a.x - c.x) ** 2 + (a.y - c.y) ** 2)

        s = (ab + bc + ca) / 2
        return math.sqrt(s * (s - ab) * (s - bc) * (s - ca))


class Rectangle(Shape):
    def area(self):
        if len(self.points) != 4:
            raise ValueError("Прямоугольник должен иметь 4 точки")

        # Проверяем, что это действительно прямоугольник (упрощенная проверка)
        a, b, c, d = self.points
        ab = math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)
        bc = math.sqrt((c.x - b.x) ** 2 + (c.y - b.y) ** 2)
        cd = math.sqrt((d.x - c.x) ** 2 + (d.y - c.y) ** 2)
        da = math.sqrt((a.x - d.x) ** 2 + (a.y - d.y) ** 2)

        # Для прямоугольника противоположные стороны должны быть равны
        if not (math.isclose(ab, cd) and math.isclose(bc, da)):
            print("Предупреждение: точки не образуют прямоугольник. Площадь может быть вычислена некорректно.")

        # Используем формулу площади через векторное произведение
        return abs(
            (a.x * b.y + b.x * c.y + c.x * d.y + d.x * a.y) - (a.y * b.x + b.y * c.x + c.y * d.x + d.y * a.x)) / 2


class Polygon(Shape):
    def area(self):
        if len(self.points) < 3:
            raise ValueError("Многоугольник должен иметь хотя бы 3 точки")

        # Формула площади Гаусса (шнурования)
        n = len(self.points)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += self.points[i].x * self.points[j].y
            area -= self.points[j].x * self.points[i].y
        return abs(area) / 2


def input_point(prompt):
    print(prompt)
    x = float(input("Введите координату x: "))
    y = float(input("Введите координату y: "))
    return Point(x, y)


def create_shape():
    print("\nВыберите тип фигуры:")
    print("1. Круг")
    print("2. Треугольник")
    print("3. Прямоугольник")
    print("4. Многоугольник")

    choice = input("Введите номер (1-4): ")

    if choice == '1':
        print("\nСоздание круга:")
        center = input_point("Введите координаты центра:")
        radius_point = input_point("Введите координаты точки на окружности:")
        return Circle(center, radius_point)
    elif choice == '2':
        print("\nСоздание треугольника (введите 3 точки):")
        points = [input_point(f"Точка {i + 1}:") for i in range(3)]
        return Triangle(points)
    elif choice == '3':
        print("\nСоздание прямоугольника (введите 4 точки по порядку):")
        points = [input_point(f"Точка {i + 1}:") for i in range(4)]
        return Rectangle(points)
    elif choice == '4':
        n = int(input("\nВведите количество вершин многоугольника: "))
        points = [input_point(f"Точка {i + 1}:") for i in range(n)]
        return Polygon(points)
    else:
        print("Неверный выбор")
        return None


def main():
    shapes = []

    print("Создайте 5 геометрических фигур:")
    for i in range(5):
        print(f"\nФигура #{i + 1}:")
        shape = create_shape()
        if shape:
            shapes.append(shape)
            print(f"Фигура создана: {shape}")
            print(f"Площадь: {shape.area():.2f}")

    print("\nСписок всех созданных фигур:")
    for i, shape in enumerate(shapes, 1):
        print(f"\nФигура #{i}:")
        print(f"Тип: {shape.__class__.__name__}")
        print(shape)
        print(f"Площадь: {shape.area():.2f}")




if __name__ == "__main__":
    main()