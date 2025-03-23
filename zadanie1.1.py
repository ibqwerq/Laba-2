chislo1 = float (input ("Введите первое число: "))
chislo2 = float(input("Введите второе число: "))

summa = chislo1 + chislo2
print(f"Сумма чисел: {summa}")

raznost = chislo1 - chislo2
print(f"Разность чисел: {raznost}")

proizvedenie = chislo1 * chislo2
print(f"Произведение чисел: {proizvedenie}")

srednee_arifmeticheskoe = (chislo1 + chislo2) / 2
print(f"Среднее арифметическое чисел: {srednee_arifmeticheskoe}")

modul_chislo1 = chislo1 if chislo1 >= 0 else - chislo1
modul_chislo2 = chislo2 if chislo2 >= 0 else - chislo2

maksimum = modul_chislo1 if modul_chislo1 > modul_chislo2 else modul_chislo2
minimum = modul_chislo1 if modul_chislo1 < modul_chislo2 else modul_chislo2

raznost_modulei = maksimum - minimum
print(f"Разность максимального и минимального по модулю: {raznost_modulei}")
