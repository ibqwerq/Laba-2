import json

class School:
    def __init__(self, number, director, students):
        self.number = number
        self.director = director
        self.students = students

    def __repr__(self):
        return f"School(number={self.number}, director='{self.director}', students={self.students})"

def load_data(filename):
    schools = []
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            for item in data:
                schools.append(School(item['number'], item['director'], item['students']))
    except FileNotFoundError:
        print("Файл не найден. Создан новый список школ.")
    return schools

def add_school(schools):
    number = int(input("Введите номер школы: "))
    director = input("Введите фамилию директора: ")
    students = int(input("Введите количество учащихся: "))
    schools.append(School(number, director, students))
    print("Школа успешно добавлена.")

def view_schools(schools):
    for school in schools:
        print(school)

def search_by_director(schools, director):
    found = [school for school in schools if school.director == director]
    if found:
        for school in found:
            print(school)
    else:
        print("Школы с таким директором не найдены.")

def sort_schools(schools, key):
    schools.sort(key=lambda x: getattr(x, key))
    print("Данные отсортированы.")

def save_data(schools, filename):
    data = [{'number': school.number, 'director': school.director, 'students': school.students} for school in schools]
    with open(filename, 'w') as file:
        json.dump(data, file)
    print("Данные сохранены в файл.")

def main():
    filename = "schools.json"
    schools = load_data(filename)

    while True:
        print("\nМеню:")
        print("1. Добавить школу")
        print("2. Просмотреть все школы")
        print("3. Поиск по фамилии директора")
        print("4. Сортировать школы")
        print("5. Сохранить данные")
        print("6. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            add_school(schools)
        elif choice == '2':
            view_schools(schools)
        elif choice == '3':
            director = input("Введите фамилию директора: ")
            search_by_director(schools, director)
        elif choice == '4':
            key = input("Введите поле для сортировки (number/students): ")
            sort_schools(schools, key)
        elif choice == '5':
            save_data(schools, filename)
        elif choice == '6':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()