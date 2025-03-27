'''Выбрано задание №5 - "Создать классы для сотрудников, заказчиков и задач.
Реализовать функциональность учета затраченного
времени, позволяя добавлять новые типы задач и формировать отчетность..'''

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union
from enum import Enum
import csv
import json


class TaskType(Enum):
    """Типы задач"""
    DEVELOPMENT = "Разработка"
    MEETING = "Совещание"
    DESIGN = "Дизайн"
    TESTING = "Тестирование"
    DOCUMENTATION = "Документирование"
    SUPPORT = "Поддержка"


class EmployeeRole(Enum):
    """Роли сотрудников"""
    DEVELOPER = "Разработчик"
    DESIGNER = "Дизайнер"
    MANAGER = "Менеджер"
    QA = "Тестировщик"
    ANALYST = "Аналитик"


class TimeEntry:
    """Запись о затраченном времени"""

    def __init__(self, start_time: datetime, end_time: datetime, description: str):
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.duration = end_time - start_time

    def to_dict(self) -> Dict:
        return {
            "start": self.start_time.isoformat(),
            "end": self.end_time.isoformat(),
            "description": self.description,
            "duration_hours": round(self.duration.total_seconds() / 3600, 2)
        }


class Employee:
    """Класс сотрудника"""

    def __init__(self, employee_id: int, name: str, role: EmployeeRole, hourly_rate: float):
        self.employee_id = employee_id
        self.name = name
        self.role = role
        self.hourly_rate = hourly_rate
        self.time_entries: List[TimeEntry] = []

    def add_time_entry(self, entry: TimeEntry):
        """Добавить запись о времени"""
        self.time_entries.append(entry)

    def get_total_hours(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> float:
        """Получить общее количество отработанных часов"""
        total = 0.0
        for entry in self.time_entries:
            if start_date and entry.start_time < start_date:
                continue
            if end_date and entry.end_time > end_date:
                continue
            total += entry.duration.total_seconds() / 3600
        return round(total, 2)

    def get_total_cost(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> float:
        """Рассчитать общую стоимость работы"""
        return round(self.get_total_hours(start_date, end_date) * self.hourly_rate, 2)

    def generate_time_report(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Dict:
        """Сгенерировать отчет по времени"""
        report = {
            "employee_id": self.employee_id,
            "name": self.name,
            "role": self.role.value,
            "total_hours": self.get_total_hours(start_date, end_date),
            "total_cost": self.get_total_cost(start_date, end_date),
            "entries": [entry.to_dict() for entry in self.time_entries]
        }
        return report

    def __str__(self):
        return f"{self.name} ({self.role.value}) - {self.get_total_hours()} ч"


class Customer:
    """Класс заказчика"""

    def __init__(self, customer_id: int, name: str, email: str, company: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.company = company
        self.projects: List['Project'] = []

    def add_project(self, project: 'Project'):
        """Добавить проект"""
        if project not in self.projects:
            self.projects.append(project)

    def get_total_cost(self) -> float:
        """Получить общую стоимость по всем проектам"""
        return round(sum(project.get_total_cost() for project in self.projects), 2)

    def __str__(self):
        return f"{self.company} ({self.name})"


class Project:
    """Класс проекта"""

    def __init__(self, project_id: int, name: str, customer: Customer):
        self.project_id = project_id
        self.name = name
        self.customer = customer
        self.tasks: List['Task'] = []
        customer.add_project(self)

    def add_task(self, task: 'Task'):
        """Добавить задачу"""
        if task not in self.tasks:
            self.tasks.append(task)

    def get_total_hours(self) -> float:
        """Получить общее количество часов по проекту"""
        return round(sum(task.get_total_hours() for task in self.tasks), 2)

    def get_total_cost(self) -> float:
        """Рассчитать общую стоимость проекта"""
        total = 0.0
        for task in self.tasks:
            total += task.get_total_cost()
        return round(total, 2)

    def generate_report(self) -> Dict:
        """Сгенерировать отчет по проекту"""
        return {
            "project_id": self.project_id,
            "name": self.name,
            "customer": self.customer.company,
            "total_hours": self.get_total_hours(),
            "total_cost": self.get_total_cost(),
            "tasks": [task.to_dict() for task in self.tasks]
        }

    def __str__(self):
        return f"{self.name} (Заказчик: {self.customer.company})"


class Task:
    """Класс задачи"""

    def __init__(self, task_id: int, name: str, description: str, task_type: TaskType, project: Project):
        self.task_id = task_id
        self.name = name
        self.description = description
        self.task_type = task_type
        self.project = project
        self.time_entries: List[TimeEntry] = []
        self.assigned_employees: List[Employee] = []
        project.add_task(self)

    def assign_employee(self, employee: Employee):
        """Назначить сотрудника на задачу"""
        if employee not in self.assigned_employees:
            self.assigned_employees.append(employee)

    def add_time_entry(self, employee: Employee, entry: TimeEntry):
        """Добавить запись времени для задачи"""
        if employee in self.assigned_employees:
            self.time_entries.append(entry)
            employee.add_time_entry(entry)

    def get_total_hours(self) -> float:
        """Получить общее количество часов по задаче"""
        total = sum(entry.duration.total_seconds() / 3600 for entry in self.time_entries)
        return round(total, 2)

    def get_total_cost(self) -> float:
        """Рассчитать общую стоимость задачи"""
        total = 0.0
        for entry in self.time_entries:
            for employee in self.assigned_employees:
                if any(e for e in employee.time_entries if e == entry):
                    total += entry.duration.total_seconds() / 3600 * employee.hourly_rate
        return round(total, 2)

    def to_dict(self) -> Dict:
        """Преобразовать задачу в словарь"""
        return {
            "task_id": self.task_id,
            "name": self.name,
            "type": self.task_type.value,
            "total_hours": self.get_total_hours(),
            "total_cost": self.get_total_cost(),
            "assigned_employees": [emp.name for emp in self.assigned_employees]
        }

    def __str__(self):
        return f"{self.name} ({self.task_type.value}) - {self.get_total_hours()} ч"


class TimeTracker:
    """Основной класс системы учета времени"""

    def __init__(self):
        self.employees: Dict[int, Employee] = {}
        self.customers: Dict[int, Customer] = {}
        self.projects: Dict[int, Project] = {}
        self.tasks: Dict[int, Task] = {}
        self.next_employee_id = 1
        self.next_customer_id = 1
        self.next_project_id = 1
        self.next_task_id = 1

    def add_employee(self, name: str, role: EmployeeRole, hourly_rate: float) -> Employee:
        """Добавить нового сотрудника"""
        employee = Employee(self.next_employee_id, name, role, hourly_rate)
        self.employees[self.next_employee_id] = employee
        self.next_employee_id += 1
        return employee

    def add_customer(self, name: str, email: str, company: str) -> Customer:
        """Добавить нового заказчика"""
        customer = Customer(self.next_customer_id, name, email, company)
        self.customers[self.next_customer_id] = customer
        self.next_customer_id += 1
        return customer

    def add_project(self, name: str, customer_id: int) -> Project:
        """Добавить новый проект"""
        if customer_id not in self.customers:
            raise ValueError("Заказчик не найден")
        project = Project(self.next_project_id, name, self.customers[customer_id])
        self.projects[self.next_project_id] = project
        self.next_project_id += 1
        return project

    def add_task(self, name: str, description: str, task_type: TaskType, project_id: int) -> Task:
        """Добавить новую задачу"""
        if project_id not in self.projects:
            raise ValueError("Проект не найден")
        task = Task(self.next_task_id, name, description, task_type, self.projects[project_id])
        self.tasks[self.next_task_id] = task
        self.next_task_id += 1
        return task

    def assign_employee_to_task(self, employee_id: int, task_id: int):
        """Назначить сотрудника на задачу"""
        if employee_id not in self.employees:
            raise ValueError("Сотрудник не найден")
        if task_id not in self.tasks:
            raise ValueError("Задача не найдена")
        self.tasks[task_id].assign_employee(self.employees[employee_id])

    def add_time_entry(self, employee_id: int, task_id: int,
                       start_time: datetime, end_time: datetime, description: str):
        """Добавить запись о затраченном времени"""
        if employee_id not in self.employees:
            raise ValueError("Сотрудник не найден")
        if task_id not in self.tasks:
            raise ValueError("Задача не найдена")

        entry = TimeEntry(start_time, end_time, description)
        self.tasks[task_id].add_time_entry(self.employees[employee_id], entry)

    def generate_employee_report(self, employee_id: int,
                                 start_date: Optional[datetime] = None,
                                 end_date: Optional[datetime] = None) -> Dict:
        """Сгенерировать отчет по сотруднику"""
        if employee_id not in self.employees:
            raise ValueError("Сотрудник не найден")
        return self.employees[employee_id].generate_time_report(start_date, end_date)

    def generate_project_report(self, project_id: int) -> Dict:
        """Сгенерировать отчет по проекту"""
        if project_id not in self.projects:
            raise ValueError("Проект не найден")
        return self.projects[project_id].generate_report()

    def save_report_to_csv(self, report_data: Dict, filename: str):
        """Сохранить отчет в CSV файл"""
        if "entries" in report_data:  # Employee report
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Сотрудник", report_data["name"]])
                writer.writerow(["Роль", report_data["role"]])
                writer.writerow(["Общее время (ч)", report_data["total_hours"]])
                writer.writerow(["Общая стоимость", report_data["total_cost"]])
                writer.writerow([])
                writer.writerow(["Начало", "Конец", "Описание", "Часы"])
                for entry in report_data["entries"]:
                    writer.writerow([
                        entry["start"],
                        entry["end"],
                        entry["description"],
                        entry["duration_hours"]
                    ])
        elif "tasks" in report_data:  # Project report
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Проект", report_data["name"]])
                writer.writerow(["Заказчик", report_data["customer"]])
                writer.writerow(["Общее время (ч)", report_data["total_hours"]])
                writer.writerow(["Общая стоимость", report_data["total_cost"]])
                writer.writerow([])
                writer.writerow(["Задача", "Тип", "Часы", "Стоимость", "Исполнители"])
                for task in report_data["tasks"]:
                    writer.writerow([
                        task["name"],
                        task["type"],
                        task["total_hours"],
                        task["total_cost"],
                        ", ".join(task["assigned_employees"])
                    ])

    def save_to_json(self, filename: str):
        """Сохранить все данные в JSON файл"""
        data = {
            "employees": [{
                "id": emp.employee_id,
                "name": emp.name,
                "role": emp.role.value,
                "hourly_rate": emp.hourly_rate,
                "time_entries": [entry.to_dict() for entry in emp.time_entries]
            } for emp in self.employees.values()],
            "customers": [{
                "id": cust.customer_id,
                "name": cust.name,
                "email": cust.email,
                "company": cust.company
            } for cust in self.customers.values()],
            "projects": [{
                "id": proj.project_id,
                "name": proj.name,
                "customer_id": proj.customer.customer_id
            } for proj in self.projects.values()],
            "tasks": [{
                "id": task.task_id,
                "name": task.name,
                "description": task.description,
                "type": task.task_type.value,
                "project_id": task.project.project_id,
                "assigned_employees": [emp.employee_id for emp in task.assigned_employees]
            } for task in self.tasks.values()]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_json(self, filename: str):
        """Загрузить данные из JSON файла"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Очищаем текущие данные
        self.employees.clear()
        self.customers.clear()
        self.projects.clear()
        self.tasks.clear()

        # Загружаем заказчиков
        for cust_data in data["customers"]:
            customer = Customer(cust_data["id"], cust_data["name"], cust_data["email"], cust_data["company"])
            self.customers[customer.customer_id] = customer
            if customer.customer_id >= self.next_customer_id:
                self.next_customer_id = customer.customer_id + 1

        # Загружаем сотрудников
        for emp_data in data["employees"]:
            role = next(r for r in EmployeeRole if r.value == emp_data["role"])
            employee = Employee(emp_data["id"], emp_data["name"], role, emp_data["hourly_rate"])
            self.employees[employee.employee_id] = employee
            if employee.employee_id >= self.next_employee_id:
                self.next_employee_id = employee.employee_id + 1

            # Восстанавливаем записи времени
            for entry_data in emp_data["time_entries"]:
                start_time = datetime.fromisoformat(entry_data["start"])
                end_time = datetime.fromisoformat(entry_data["end"])
                entry = TimeEntry(start_time, end_time, entry_data["description"])
                employee.time_entries.append(entry)

        # Загружаем проекты
        for proj_data in data["projects"]:
            customer = self.customers[proj_data["customer_id"]]
            project = Project(proj_data["id"], proj_data["name"], customer)
            self.projects[project.project_id] = project
            if project.project_id >= self.next_project_id:
                self.next_project_id = project.project_id + 1

        # Загружаем задачи
        for task_data in data["tasks"]:
            project = self.projects[task_data["project_id"]]
            task_type = next(t for t in TaskType if t.value == task_data["type"])
            task = Task(task_data["id"], task_data["name"], task_data["description"], task_type, project)
            self.tasks[task.task_id] = task
            if task.task_id >= self.next_task_id:
                self.next_task_id = task.task_id + 1

            # Восстанавливаем назначенных сотрудников
            for emp_id in task_data["assigned_employees"]:
                employee = self.employees[emp_id]
                task.assigned_employees.append(employee)

    def __str__(self):
        return (f"Система учета времени:\n"
                f"- Сотрудников: {len(self.employees)}\n"
                f"- Заказчиков: {len(self.customers)}\n"
                f"- Проектов: {len(self.projects)}\n"
                f"- Задач: {len(self.tasks)}")


def main():
    """Пример использования системы"""
    tracker = TimeTracker()

    # Добавляем сотрудников
    dev1 = tracker.add_employee("Иван Петров", EmployeeRole.DEVELOPER, 25.0)
    designer1 = tracker.add_employee("Анна Сидорова", EmployeeRole.DESIGNER, 20.0)
    manager1 = tracker.add_employee("Олег Иванов", EmployeeRole.MANAGER, 30.0)

    # Добавляем заказчиков
    customer1 = tracker.add_customer("Петр Николаев", "pn@company.com", "ООО ТехноПром")
    customer2 = tracker.add_customer("Мария Кузнецова", "mk@firma.ru", "АБС Консалтинг")

    # Добавляем проекты
    project1 = tracker.add_project("Разработка CRM системы", customer1.customer_id)
    project2 = tracker.add_project("Редизайн сайта", customer2.customer_id)

    # Добавляем задачи
    task1 = tracker.add_task("Проектирование архитектуры", "Спроектировать модули системы",
                             TaskType.DEVELOPMENT, project1.project_id)
    task2 = tracker.add_task("Создание макетов", "Разработать UI/UX дизайн",
                             TaskType.DESIGN, project2.project_id)
    task3 = tracker.add_task("Планирование проекта", "Составить план разработки",
                             TaskType.MEETING, project1.project_id)

    # Назначаем сотрудников на задачи
    tracker.assign_employee_to_task(dev1.employee_id, task1.task_id)
    tracker.assign_employee_to_task(designer1.employee_id, task2.task_id)
    tracker.assign_employee_to_task(manager1.employee_id, task3.task_id)

    # Добавляем записи времени
    now = datetime.now()
    tracker.add_time_entry(dev1.employee_id, task1.task_id,
                           now - timedelta(hours=4), now - timedelta(hours=2),
                           "Проектирование модуля пользователей")
    tracker.add_time_entry(dev1.employee_id, task1.task_id,
                           now - timedelta(hours=2), now,
                           "Проектирование модуля отчетов")
    tracker.add_time_entry(designer1.employee_id, task2.task_id,
                           now - timedelta(hours=3), now - timedelta(hours=1.5),
                           "Дизайн главной страницы")
    tracker.add_time_entry(manager1.employee_id, task3.task_id,
                           now - timedelta(hours=2), now - timedelta(hours=1),
                           "Совещание с заказчиком")

    # Генерируем отчеты
    print("\nОтчет по сотруднику:")
    emp_report = tracker.generate_employee_report(dev1.employee_id)
    print(f"{emp_report['name']} ({emp_report['role']})")
    print(f"Всего часов: {emp_report['total_hours']}")
    print(f"Всего стоимость: {emp_report['total_cost']}")
    print("Записи времени:")
    for entry in emp_report["entries"]:
        print(f"- {entry['start']} - {entry['end']}: {entry['description']} ({entry['duration_hours']} ч)")

    print("\nОтчет по проекту:")
    proj_report = tracker.generate_project_report(project1.project_id)
    print(f"{proj_report['name']} (Заказчик: {proj_report['customer']})")
    print(f"Всего часов: {proj_report['total_hours']}")
    print(f"Всего стоимость: {proj_report['total_cost']}")
    print("Задачи:")
    for task in proj_report["tasks"]:
        print(f"- {task['name']} ({task['type']}): {task['total_hours']} ч, {task['total_cost']} руб")

    # Сохраняем отчеты
    tracker.save_report_to_csv(emp_report, "employee_report.csv")
    tracker.save_report_to_csv(proj_report, "project_report.csv")

    # Сохраняем все данные
    tracker.save_to_json("time_tracker_data.json")

    # Демонстрация загрузки данных
    new_tracker = TimeTracker()
    new_tracker.load_from_json("time_tracker_data.json")
    print("\nДанные успешно загружены в новую систему:")
    print(new_tracker)





if __name__ == "__main__":
    main()