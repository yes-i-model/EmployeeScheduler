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

def interpret_conflicts(conflict_description, employees):
    conflict_affected_employees = []
    for employee in employees:
        if employee['name'].lower() in conflict_description.lower():
            conflict_affected_employees.append(employee['name'])
    return conflict_affected_employees

def view_schedule(employees):
    conflicts_present = input("\nAre there any dynamic conflicts for this week? (yes/no): ").strip().lower()
    conflict_affected_employees = []
    if conflicts_present == 'yes':
        conflict_description = input("Please describe the conflicts affecting this week's schedule: ")
        conflict_affected_employees = interpret_conflicts(conflict_description, employees)

    # Rest of the view_schedule function (original content)...

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

    # Shuffle the lists
    random.shuffle(kitchen_shifts)
    random.shuffle(barista_shifts)

    max_shifts = {
        'full-time': 5,
        'part-time': 3
    }

    shifts_assigned = {emp['name']: 0 for emp in employees}

    for day in days_of_week:
        kitchen_morning = assign_shift(kitchen_shifts, max_shifts, shifts_assigned, conflict_affected_employees)
        kitchen_afternoon = assign_shift(kitchen_shifts, max_shifts, shifts_assigned, conflict_affected_employees)
        barista_morning = assign_shift(barista_shifts, max_shifts, shifts_assigned, conflict_affected_employees)
        barista_afternoon = assign_shift(barista_shifts, max_shifts, shifts_assigned, conflict_affected_employees)


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


def assign_shift(shifts, max_shifts, shifts_assigned, conflict_affected_employees):
    available_staffers = [s for s in shifts if s['name'] not in conflict_affected_employees]
    
    # If no staffers available due to conflicts, consider all staffers
    if not available_staffers:
        available_staffers = shifts

    # Try to assign a staffer who hasn't reached their max shifts first
    for staffer in available_staffers:
        if shifts_assigned[staffer['name']] < max_shifts[staffer['employment_time']]:
            shifts_assigned[staffer['name']] += 1
            return staffer

    # If all staffers have reached their max shifts, assign the least assigned staffer
    least_assigned_staffer = min(available_staffers, key=lambda s: shifts_assigned[s['name']])
    if least_assigned_staffer['name'] not in conflict_affected_employees:
        shifts_assigned[least_assigned_staffer['name']] += 1
        return least_assigned_staffer

    # If there are absolutely no suitable employees available, return a default value
    return {'name': 'None'}



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