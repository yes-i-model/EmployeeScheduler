import json
import random
import signal

def load_data():
    try:
        with open('employee_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(employees):
    with open('employee_data.json', 'w') as f:
        json.dump(employees, f)

def save_on_terminate(signum, frame):
    global employees
    save_data(employees)
    print("Data saved. Exiting...")
    exit(0)

def add_employee(employees):
    name = input('Enter the employee name: ')
    role = input('Enter the role (kitchen or barista): ').strip().lower()
    employment_time = input('Enter the employment time (full-time or part-time): ').strip().lower()
    if role not in ['kitchen', 'barista'] or employment_time not in ['full-time', 'part-time']:
        print('Invalid role or employment time. Please enter valid details.')
        return
    employees.append({'name': name, 'role': role, 'employment_time': employment_time})
    print(f'Employee {name} added successfully!')
    save_data(employees)

def schedule_shift(shifts, role):
    if not shifts:
        return 'None', 'None'
    morning_shift = shifts.pop(0)
    afternoon_shift = morning_shift
    if role == 'barista' and random.random() < 0.8:
        if shifts:
            afternoon_shift = shifts.pop(0)
    elif role == 'kitchen' and random.random() < 0.5:
        if shifts:
            afternoon_shift = shifts.pop(0)
    shifts.append(morning_shift)
    if morning_shift != afternoon_shift:
        shifts.append(afternoon_shift)
    return morning_shift, afternoon_shift

def view_schedule(employees):
    print('\nShift Schedule:')
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    kitchen_shifts = [employee['name'] for employee in employees if employee['role'] == 'kitchen']
    barista_shifts = [employee['name'] for employee in employees if employee['role'] == 'barista']
    scheduled_hours = {employee['name']: 0 for employee in employees}

    for day in days_of_week:
        print(day)
        kitchen_staffer_morning, kitchen_staffer_afternoon = schedule_shift(kitchen_shifts, 'kitchen')
        barista_morning, barista_afternoon = schedule_shift(barista_shifts, 'barista')
        print(f"  Kitchen Staffer: {kitchen_staffer_morning} - 8 AM to 12 PM, {kitchen_staffer_afternoon} - 12 PM to 5 PM")
        print(f"  Barista: {barista_morning} - 8 AM to 12 PM, {barista_afternoon} - 12 PM to 5 PM")

        for staffer in [kitchen_staffer_morning, kitchen_staffer_afternoon, barista_morning, barista_afternoon]:
            if staffer != 'None':
                if staffer == kitchen_staffer_morning or staffer == barista_morning:
                    scheduled_hours[staffer] += 4
                if staffer == kitchen_staffer_afternoon or staffer == barista_afternoon:
                    scheduled_hours[staffer] += 5

    print('\nEmployee Scheduled Hours:')
    for name, hours in scheduled_hours.items():
        print(f"{name}: {hours} hours")

def view_employees(employees):
    print('\nList of Employees:')
    for employee in employees:
        print(f"Name: {employee['name']}, Role: {employee['role']}, Employment Time: {employee['employment_time']}")
    print()

def main():
    global employees
    employees = load_data()
    signal.signal(signal.SIGINT, save_on_terminate)

    while True:
        print('\nMenu:')
        print('1. Add Employee')
        print('2. View Schedule')
        print('3. View Employees')
        print('4. Exit')
        choice = input('Please select an option (1-4): ')
        if choice == '1':
            add_employee(employees)
        elif choice == '2':
            view_schedule(employees)
        elif choice == '3':
            view_employees(employees)
        elif choice == '4':
            save_data(employees)
            print('Data saved. Goodbye!')
            break
        else:
            print('Invalid option, please try again.')

if __name__ == '__main__':
    main()
