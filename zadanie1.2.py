imya = input("Введите ваше имя: ")
vozrast = int(input("Введите ваш возраст: "))
nomer_shkoli = input("Введите номер школы: ")
klass = int(input("Какой класс вы окончили (9 или 11)? "))
god_tekyshii = 2025

if klass == 11:
    god_vipyska = 18
elif klass == 9:
    god_vipyska = 16
else:
    print("Ошибка: введен неверный класс. Допустимые значения: 9 или 11.")
    exit()

if god_vipyska < god_vipyska:
    print("Ошибка: возраст не соответствует выпускному классу.")
    exit()

god_vipyska = god_tekyshii - (vozrast - god_vipyska)

print(f"\nПривет {imya}!")
print(f"Поздравляю с окончанием {klass} класса школы №{nomer_shkoli}")
print(f"в {god_vipyska} году.")
