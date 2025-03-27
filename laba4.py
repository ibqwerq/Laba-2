from abc import ABC, abstractmethod
import math
from enum import Enum


class CoordinateSystem(Enum):
    CARTESIAN_2D = 1
    POLAR_2D = 2
    CARTESIAN_3D = 3


class Point:
    def __init__(self, *args, coord_system=CoordinateSystem.CARTESIAN_2D):
        self.coord_system = coord_system

        if coord_system == CoordinateSystem.CARTESIAN_2D:
            self.x, self.y = args
            self.z = 0
        elif coord_system == CoordinateSystem.POLAR_2D:
            r, theta = args
            self.x = r * math.cos(theta)
            self.y = r * math.sin(theta)
            self.z = 0
        elif coord_system == CoordinateSystem.CARTESIAN_3D:
            self.x, self.y, self.z = args
        else:
            raise ValueError("Неподдерживаемая система координат")

    def to_cartesian_2d(self):
        return (self.x, self.y)

    def __str__(self):
        if self.coord_system == CoordinateSystem.POLAR_2D:
            r = math.sqrt(self.x ** 2 + self.y ** 2)
            theta = math.atan2(self.y, self.x)
            return f"(r={r:.2f}, θ={theta:.2f})"
        elif self.z == 0:
            return f"({self.x:.2f}, {self.y:.2f})"
        else:
            return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"


class Shape(ABC):
    def __init__(self, points):
        self.points = points

    @abstractmethod
    def area(self):
        pass

    def __str__(self):
        points_str = ", ".join(str(point) for point in self.points)
        return f"{self.__class__.__name__} [Точки: {points_str}, Площадь: {self.area():.2f}]"


class Circle(Shape):
    def __init__(self, center, radius_point):
        super().__init__([center, radius_point])
        self.center = center
        dx = radius_point.x - center.x
        dy = radius_point.y - center.y
        self.radius = math.sqrt(dx ** 2 + dy ** 2)

    def area(self):
        return math.pi * self.radius ** 2


class Triangle(Shape):
    def area(self):
        if len(self.points) != 3:
            raise ValueError("Треугольник должен иметь 3 точки")

        a, b, c = [p.to_cartesian_2d() for p in self.points]
        ax, ay = a
        bx, by = b
        cx, cy = c

        # Формула площади через векторное произведение
        return abs((ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) / 2)


class Rectangle(Shape):
    def area(self):
        if len(self.points) != 4:
            raise ValueError("Прямоугольник должен иметь 4 точки")

        # Формула площади Гаусса для четырехугольника
        points = [p.to_cartesian_2d() for p in self.points]
        n = len(points)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            xi, yi = points[i]
            xj, yj = points[j]
            area += xi * yj
            area -= xj * yi
        return abs(area) / 2


class Polygon(Shape):
    def area(self):
        if len(self.points) < 3:
            raise ValueError("Многоугольник должен иметь хотя бы 3 точки")

        # Формула площади Гаусса
        points = [p.to_cartesian_2d() for p in self.points]
        n = len(points)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            xi, yi = points[i]
            xj, yj = points[j]
            area += xi * yj
            area -= xj * yi
        return abs(area) / 2


def input_point(prompt, coord_system):
    print(prompt)

    if coord_system == CoordinateSystem.CARTESIAN_2D:
        x = float(input("Введите координату x: "))
        y = float(input("Введите координату y: "))
        return Point(x, y, coord_system=coord_system)
    elif coord_system == CoordinateSystem.POLAR_2D:
        r = float(input("Введите радиус r: "))
        theta = float(input("Введите угол θ (в радианах): "))
        return Point(r, theta, coord_system=coord_system)
    elif coord_system == CoordinateSystem.CARTESIAN_3D:
        x = float(input("Введите координату x: "))
        y = float(input("Введите координату y: "))
        z = float(input("Введите координату z: "))
        return Point(x, y, z, coord_system=coord_system)


def create_shape(coord_system):
    print("\nВыберите тип фигуры:")
    print("1. Круг")
    print("2. Треугольник")
    print("3. Прямоугольник")
    print("4. Многоугольник")

    choice = input("Введите номер (1-4): ")

    if choice == '1':
        print("\nСоздание круга:")
        center = input_point("Введите координаты центра:", coord_system)
        radius_point = input_point("Введите координаты точки на окружности:", coord_system)
        return Circle(center, radius_point)
    elif choice == '2':
        print("\nСоздание треугольника (введите 3 точки):")
        points = [input_point(f"Точка {i + 1}:", coord_system) for i in range(3)]
        return Triangle(points)
    elif choice == '3':
        print("\nСоздание прямоугольника (введите 4 точки по порядку):")
        points = [input_point(f"Точка {i + 1}:", coord_system) for i in range(4)]
        return Rectangle(points)
    elif choice == '4':
        n = int(input("\nВведите количество вершин многоугольника: "))
        points = [input_point(f"Точка {i + 1}:", coord_system) for i in range(n)]
        return Polygon(points)
    else:
        print("Неверный выбор")
        return None


def select_coordinate_system():
    print("\nВыберите систему координат:")
    print("1. Двумерная декартова (x, y)")
    print("2. Двумерная полярная (r, θ)")
    print("3. Трехмерная декартова (x, y, z)")

    choice = input("Введите номер (1-3): ")

    if choice == '1':
        return CoordinateSystem.CARTESIAN_2D
    elif choice == '2':
        return CoordinateSystem.POLAR_2D
    elif choice == '3':
        return CoordinateSystem.CARTESIAN_3D
    else:
        print("Неверный выбор, используется двумерная декартова система")
        return CoordinateSystem.CARTESIAN_2D


def main():
    shapes = []

    print("Создайте 5 геометрических фигур:")
    coord_system = select_coordinate_system()

    for i in range(5):
        print(f"\nФигура #{i + 1}:")
        shape = create_shape(coord_system)
        if shape:
            shapes.append(shape)
            print(f"Фигура создана: {shape}")

    # Сортировка фигур по площади
    shapes.sort(key=lambda x: x.area())

    print("\nОтсортированный список всех созданных фигур (по возрастанию площади):")
    for i, shape in enumerate(shapes, 1):
        print(f"\nФигура #{i}:")
        print(f"Тип: {shape.__class__.__name__}")
        print(shape)





if __name__ == "__main__":
    main()