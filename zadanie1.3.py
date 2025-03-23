radius1 = float(input("Введите радиус первого круга: "))
radius2 = float(input("Введите радиус второго круга: "))

pi = 3.14159
ploshad1 = pi * radius1**2
ploshad2 = pi * radius2**2

if ploshad1 > ploshad2:
    print("Первый круг имеет большую площадь.")
    raznost_ploshadei = ploshad1 - ploshad2
elif ploshad2 > ploshad1:
    print("Второй круг имеет большую площадь.")
    raznost_ploshadei = ploshad2 - ploshad1
else:
    print("Площади кругов равны.")
    raznost_ploshadei = 0

print(f"Разность площадей: {raznost_ploshadei:.2f}")
