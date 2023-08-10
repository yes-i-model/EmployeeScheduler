import json
import random

# Loading data functions
def load_data():
    try:
        with open('employee_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(employees):
    with open('employee_data.json', 'w') as f:
        json.dump(employees, f)

# Employee Management functions
def edit_employees(employees):
    while True:
        print("\n1. Add Employee")
        print("2. Modify Employee")
        print("3. Delete Employee")
        print("4. Return to Main Menu")
        choice = input("Please select an option (1-4): ")

        if choice == '1':
            add_employee(employees)
        elif choice == '2':
            modify_employee(employees)
        elif choice == '3':
            delete_employee(employees)
        elif choice == '4':
            return
        else:
            print("Invalid option, please try again.")

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

def modify_employee(employees):
    name = input('Enter the name of the employee to modify: ')
    employee = next((e for e in employees if e['name'] == name), None)
    if not employee:
        print(f'Employee {name} not found.')
        return
    new_role = input(f'Enter new role for {name} (kitchen or barista): ').strip().lower()
    new_employment_time = input(f'Enter new employment time for {name} (full-time or part-time): ').strip().lower()
    if new_role not in ['kitchen', 'barista'] or new_employment_time not in ['full-time', 'part-time']:
        print('Invalid role or employment time. Please enter valid details.')
        return
    employee['role'] = new_role
    employee['employment_time'] = new_employment_time
    print(f'Employee {name} modified successfully!')
    save_data(employees)

def delete_employee(employees):
    name = input('Enter the name of the employee to delete: ')
    employee = next((e for e in employees if e['name'] == name), None)
    if not employee:
        print(f'Employee {name} not found.')
        return
    employees.remove(employee)
    print(f'Employee {name} deleted successfully!')
    save_data(employees)

def view_employees(employees):
    print('\nList of Employees:')
    for employee in employees:
        print(f"Name: {employee['name']}, Role: {employee['role']}, Employment Time: {employee['employment_time']}")

# Schedule functions
def view_schedule(employees):
    print("\nShift Schedule:".center(80, '-'))
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours = {}
    
    header = "| Day of Week | Role     | Morning (8 AM - 12 PM) | Afternoon (12 PM - 5 PM) |"
    separator = "+-------------+----------+-----------------------+--------------------------+"
    
    print(separator)
    print(header)
    print(separator)
    
    kitchen_shifts = [emp for emp in employees if emp['role'] == 'kitchen']
    barista_shifts = [emp for emp in employees if emp['role'] == 'barista']

    for day in days_of_week:
        kitchen_morning = kitchen_shifts.pop(0) if kitchen_shifts else {'name': 'None'}
        kitchen_afternoon = kitchen_shifts.pop(0) if kitchen_shifts else {'name': 'None'}
        barista_morning = barista_shifts.pop(0) if barista_shifts else {'name': 'None'}
        barista_afternoon = barista_shifts.pop(0) if barista_shifts else {'name': 'None'}

        print(f"| {day.center(13)} | {'Kitchen'.center(8)} | {kitchen_morning['name'].center(23)} | {kitchen_afternoon['name'].center(24)} |")
        print(separator)
        print(f"| {day.center(13)} | {'Barista'.center(8)} | {barista_morning['name'].center(23)} | {barista_afternoon['name'].center(24)} |")
        print(separator)
        
        for staffer in [kitchen_morning, kitchen_afternoon]:
            if staffer['name'] != 'None':
                hours[staffer['name']] = hours.get(staffer['name'], 0) + 4
        for staffer in [barista_morning, barista_afternoon]:
            if staffer['name'] != 'None':
                hours[staffer['name']] = hours.get(staffer['name'], 0) + 5

    print("\nEmployee Hours:".center(80, '-'))
    for employee, worked_hours in hours.items():
        print(f"{employee}: {worked_hours} hours")

def main():
    employees = load_data()

    while True:
        print("\nEmployee Scheduler Menu:")
        print("1. Edit Employees")
        print("2. View Schedule")
        print("3. View Employees")
        print("4. Quit")
        
        choice = input("\nEnter your choice: ")

        if choice == '1':
            edit_employees(employees)
        elif choice == '2':
            view_schedule(employees)
        elif choice == '3':
            view_employees(employees)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
