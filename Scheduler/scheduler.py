import json
import random

def load_data():
    try:
        with open('employee_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(employees):
    with open('employee_data.json', 'w') as f:
        json.dump(employees, f)

def add_employee(employees):
    name = input('Enter the employee name: ')
    role = input('Enter the role (kitchen or barista): ').strip().lower()
    employment_time = input('Enter the employment time (full-time or part-time): ').strip().lower()
    if role not in ['kitchen', 'barista'] or employment_time not in ['full-time', 'part-time']:
        print('Invalid role or employment time. Please enter valid details.')
        return
    employees.append({'name': name, 'role': role, 'employment_time': employment_time})
    print(f'Employee {name} added successfully!')

def schedule_shift(shifts, role):
    if not shifts:
        return 'None', 'None'

    morning_shift = shifts.pop(0)
    afternoon_shift = morning_shift

    if role == 'barista' and random.random() < 0.8:
        if shifts: # Ensure that there is another staff member for the afternoon shift
            afternoon_shift = shifts.pop(0)
    elif role == 'kitchen' and random.random() < 0.5:
        if shifts: # Ensure that there is another staff member for the afternoon shift
            afternoon_shift = shifts.pop(0)

    # Append them back to the end of the list so they can be considered for future shifts
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

        # Calculate hours
        for staffer in [kitchen_staffer_morning, kitchen_staffer_afternoon, barista_morning, barista_afternoon]:
            if staffer != 'None':
                if staffer == kitchen_staffer_morning or staffer == barista_morning:
                    scheduled_hours[staffer] += 4 # Morning shift
                if staffer == kitchen_staffer_afternoon or staffer == barista_afternoon:
                    scheduled_hours[staffer] += 5 # Afternoon shift

    print('\nEmployee Scheduled Hours:')
    for name, hours in scheduled_hours.items():
        print(f"{name}: {hours} hours")

    for employee in employees:
        if employee['employment_time'] == 'full-time':
            shifts = [employee['name']] * 5
        else: # part-time
            shifts = [employee['name']] * 2

        if employee['role'] == 'kitchen':
            kitchen_shifts.extend(shifts)
        else: # barista
            barista_shifts.extend(shifts)

    for day in days_of_week:
        print(day)
        kitchen_staffer_morning, kitchen_staffer_afternoon = schedule_shift(kitchen_shifts, 'kitchen')
        barista_morning, barista_afternoon = schedule_shift(barista_shifts, 'barista')

        print(f"  Kitchen Staffer: {kitchen_staffer_morning} - 8 AM to 12 PM, {kitchen_staffer_afternoon} - 12 PM to 5 PM")
        print(f"  Barista: {barista_morning} - 8 AM to 12 PM, {barista_afternoon} - 12 PM to 5 PM")

def main():
    employees = load_data()
    while True:
        print('\nMenu:')
        print('1. Add Employee')
        print('2. View Schedule')
        print('3. Exit')
        choice = input('Please select an option (1-3): ')
        if choice == '1':
            add_employee(employees)
        elif choice == '2':
            view_schedule(employees)
        elif choice == '3':
            save_data(employees)
            print('Data saved. Goodbye!')
            break
        else:
            print('Invalid option, please try again.')

if __name__ == '__main__':
    main()


