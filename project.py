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
    def __init__(self, name, schedule):
        self.name = name
        self.schedule = schedule

class Schedule:
    def __init__(self, barber, appointments=[]):
        self.barber = barber
        self.appointments = appointments

    def add_appointment(self, appointment):
        self.appointments.append(appointment)

    def check_available_time(self, date_time):
        for appoitment in self.appointments:
            if appoitment.date_time == date_time:
                return False
        return True

def validate_datetime(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False

def main():
    barber_1 = Barber("John Doe", Schedule(barber="John Doe"))
    barber_2 = Barber("Jane Smith", Schedule(barber="Jane Smith"))

    while True:
        print("1. Запис на обслуговування")
        print("2. Вихід")

        choice = input("Оберіть опцію: ")

        if choice == "1":
            name = input("Введіть і'мя клієнта: ")
            phone_number = input("Введіть номер телефону: ")

            customer = Customer(name, phone_number)

            service = input("Введіть послугу: ")

            print("Доступні фахівці:")
            print("1. John Doe")
            print("2. Jane Smith")

            barber_name = input("Введіть ім'я фахівця: ")
            barber = barber_1 if barber_name == "John Doe" else barber_2

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
            print("До побачення!")
            break


        else:
            print("Неправильний вибір. Будь ласка, виберіть правильну опцію.")

if __name__ == "__main__":
    main()
