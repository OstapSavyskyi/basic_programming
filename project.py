from datetime import datetime
import json
import atexit

class Customer:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

class Appointment:
    def __init__(self, customer, service, barber, date_time):
        self.customer = customer
        self.service = service
        self.barber = barber
        self.date_time = date_time

class Barber:
    def __init__(self, name, schedule, work_hours, services=[]):
        self.name = name
        self.schedule = schedule
        self.schedule.barber = self
        self.employees = []
        self.work_hours = work_hours
        self.services = services

    def add_employee(self, new_employee, start_time, end_time):
        self.employees.append(new_employee)
        self.work_hours[new_employee] = {'start_time': start_time, 'end_time': end_time}

    def get_work_hours(self):
        return self.work_hours

    def add_service(self, service):
        self.services.append(service)

    def get_services(self):
        return self.services

    def add_employee_hours(self, employee_name, start_time, end_time):
        self.employees.append(employee_name)
        self.work_hours[employee_name] = {'start_time': start_time, 'end_time': end_time}

    def save_to_json(self, filename):
        barber_data = {
            'name': self.name,
            'employees': self.employees,
            'work_hours': self.work_hours
        }
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(barber_data, file, ensure_ascii=False)

    @staticmethod
    def load_from_json(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            barber_data = json.load(file)
        name = barber_data['name']
        employees = barber_data['employees']
        work_hours = barber_data['work_hours']
        barber = Barber(name, employees, work_hours)
        return barber


class Schedule:
    def __init__(self, barber_name, appointments=[]):
        self.barber_name = barber_name
        self.appointments = appointments

    def add_appointment(self, appointment):
        self.appointments.append(appointment)

    def get_employees(self):
        return self.barber.employees

    def check_available_time(self, date_time):
        for appointment in self.appointments:
            if appointment.date_time == date_time:
                return False
        for employee in self.barber.employees:
            work_hours = self.barber.work_hours.get(employee)
            if work_hours:
                start_time = datetime.strptime(work_hours['start_time'], '%H:%M')
                end_time = datetime.strptime(work_hours['end_time'], '%H:%M')
                if start_time.time() <= date_time.time() <= end_time.time() and start_time.date() <= date_time.date():
                    return True
        return False

def validate_datetime(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False

def save_employees(employees, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(employees, file, ensure_ascii=False)

def load_employees(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def main():
    employees = load_employees('employees.json')

    barber_1_schedule = Schedule(barber_name="Сердж Танк'ян")
    barber_2_schedule = Schedule(barber_name="Ярослав Станіславський")
    
    barber_1_work_hours = {}
    barber_2_work_hours = {}

    barber_1 = Barber("Сердж Танк'ян", barber_1_schedule, barber_1_work_hours, services=["Стрижка", "Гоління"])
    barber_2 = Barber("Ярослав Станіславський", barber_2_schedule, barber_2_work_hours, services=["Пропозиції для дітей", "Укладання", "Корекція вусів із бородою"])


    available_barbers = {
        "Сердж Танк'ян": barber_1,
        "Ярослав Станіславський": barber_2
    }

    @atexit.register
    def save_employees_on_exit():
        save_employees(employees, 'employees.json')

        # Збереження змін у файлі barber_data.json при виході
        for barber_name, barber in available_barbers.items():
            barber.save_to_json('barber_data.json')

    while True:
        print("1. Запис на обслуговування")
        print("2. Додати нового працівника")
        print("3. Переглянути списки фахівців та робочий час")
        print("4. Вихід")

        choice = input("Оберіть опцію: ")

        if choice == "1":
            name = input("Введіть ім'я клієнта: ")
            phone_number = input("Введіть номер телефону: ")
            customer = Customer(name, phone_number)

            print("Доступні послуги:")
            for service in selected_barber.services:
                print(service)

            service = input("Виберіть послугу: ")

            print("Доступні фахівці:")
            for barber_name in available_barbers:
                print(barber_name)

            barber_name = input("Введіть ім'я фахівця: ")
            if barber_name in available_barbers:
                barber = available_barbers[barber_name]

                date_time_str = input("Введіть дату та час у форматі YYYY-MM-DD HH:MM: ")
                if validate_datetime(date_time_str):
                    date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
                    if barber.schedule.check_available_time(date_time):
                        appointment = Appointment(customer, service, barber, date_time)
                        barber.schedule.add_appointment(appointment)
                        print("Запис додано успішно!")
                    else:
                        print("Обраний час не доступний для запису.")
                else:
                    print("Неправильний формат часу.")
            else:
                print("Фахівець не знайдений.")

        elif choice == "2":
            new_employee = input("Введіть і'мя нового працівника: ")
            start_time = input("Введіть годину початку робочого дня (HH:MM): ")
            end_time = input("Введіть годину закінчення робочого дня (HH:MM): ")
            selected_barber = None
            barber_name = input("Введіть ім'я фахівця, до якого додати працівника: ")
            if barber_name in available_barbers:
                selected_barber = available_barbers[barber_name]
                selected_barber.add_employee(new_employee, start_time, end_time)

                selected_barber.save_to_json('barber_data.json')

                print(f"Новий працівник {new_employee} доданий до {selected_barber.name} успішно!")
            else:
                print("Фахівець не знайдений.")
        
        elif choice == "3":
            print("Список працівників та їх робочий час:")
            for barber_name, barber in available_barbers.items():
                print(f"{barber_name}: {barber.get_work_hours()}")

        elif choice == "4":
            print("До побачення!")
            break
        else:
            print("Неправильний вибір. Будь ласка, виберіть правильну опцію.")

if __name__ == "__main__":
    main()
