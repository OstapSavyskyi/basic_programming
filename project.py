from datetime import datetime

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
    def __init__(self, name, schedule, work_hours):
        self.name = name
        self.schedule = schedule
        self.schedule.barber = self  # Пов'язання з фахівцем
        self.employees = []  # Список працівників
        self.work_hours = work_hours  # Час роботи

    def add_employee(self, new_employee, employee_work_hours):
        self.employees.append(new_employee)
        self.work_hours[new_employee] = employee_work_hours

    def get_work_hours(self):
        return self.work_hours

class Schedule:
    def __init__(self, barber_name, appointments=[]):
        self.barber_name = barber_name
        self.appointments = appointments

    def add_appointment(self, appointment):
        self.appointments.append(appointment)

    def get_employees(self):
        return self.barber.employees  # Повертає список працівників фахівця

    def check_available_time(self, date_time):
        for appointment in self.appointments:
            if appointment.date_time == date_time:
                return False
        return True

def validate_datetime(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False

def main():
    barber_1_schedule = Schedule(barber_name="Сердж Танк'ян")
    barber_2_schedule = Schedule(barber_name="Ярослав Станіславський")
    
    barber_1_work_hours = {}
    barber_2_work_hours = {}

    barber_1 = Barber("Сердж Танк'ян", barber_1_schedule, barber_1_work_hours)
    barber_2 = Barber("Ярослав Станіславський", barber_2_schedule, barber_2_work_hours)

    available_barbers = {
        "Сердж Танк'ян": barber_1,
        "Ярослав Станіславський": barber_2
    }

    while True:
        print("1. Запис на обслуговування")
        print("2. Додати нового працівника")
        print("3. Переглянути списки фахівців та робочий час")
        print("4. Вихід")

        choice = input("Оберіть опцію: ")

        if choice == "1":
            name = input("Введіть і'мя клієнта: ")
            phone_number = input("Введіть номер телефону: ")

            customer = Customer(name, phone_number)

            service = input("Введіть послугу: ")

            print("Доступні фахівці:")
            print("1. Сердж Танк'ян")
            print("2. Ярослав Станіславський")

            barber_name = input("Введіть ім'я фахівця: ")
            barber = barber_1 if barber_name == "Сердж Танк'ян" else barber_2

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

        elif choice == "2":
            new_employee = input("Введіть і'мя нового працівника: ")
            employee_work_hours = input("Введіть години роботи працівника (наприклад, 9:00-17:00): ")
            barber_name = input("Введіть ім'я фахівця, до якого додати працівника: ")
            if barber_name in available_barbers:
                selected_barber = available_barbers[barber_name]
                selected_barber.add_employee(new_employee, employee_work_hours)
                print(f"Новий працівник {new_employee} доданий до {selected_barber.name} успішно!")
            else:
                print("Фахівець не знайдений.")
        
        elif choice == "3":
            for barber_name, barber in available_barbers.items():
                print(f"Фахівець: {barber_name}, Прaцівники: {barber.schedule.get_employees()}, Час роботи фахівця: {barber.get_work_hours()}")

        elif choice == "4":
            print("До побачення!")
            break
        else:
            print("Неправильний вибір. Будь ласка, виберіть правильну опцію.")

if __name__ == "__main__":
    main()
