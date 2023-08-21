import json
import random
import re
import sys

# Global username-password dictionary for simplicity. In reality, this should be encrypted and stored securely.
USER_CREDENTIALS = {
    'admin': 'password123',
    'manager': 'managerpass',
    '1' : '1'
}

def login():
    print("Please login to access the Employee Scheduler Menu.")
    tries = 3
    while tries:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            return username
        else:
            tries -= 1
            if tries:
                print(f"Incorrect username or password. You have {tries} {'try' if tries == 1 else 'tries'} left.")
            else:
                print("Incorrect username or password. Exiting program.")
                return None

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
    if role not in ['kitchen', 'barista', 'both'] or employment_time not in ['full-time', 'part-time']:
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
    if new_role not in ['kitchen', 'barista', 'both'] or new_employment_time not in ['full-time', 'part-time']:
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
    if not employees:
        print("\nNo employees added yet.")
        return

    # Define headers and separator for the table
    headers = ["Name", "Role", "Employment Time"]
    max_lengths = {
        "Name": max(len(emp['name']) for emp in employees) + 2,
        "Role": max(len(emp['role']) for emp in employees) + 2,
        "Employment Time": max(len(emp['employment_time']) for emp in employees) + 2
    }
    
    separator = "+".join("-" * max_lengths[header] for header in headers)
    
    print("\nList of Employees:")
    print(f"+{separator}+")
    print("|", end="")
    for header in headers:
        print(f" {header.center(max_lengths[header])} |", end="")
    print("\n+" + separator + "+")

    # Print employee details in the table
    for employee in employees:
        print("|", end="")
        print(f" {employee['name'].center(max_lengths['Name'])} |", end="")
        print(f" {employee['role'].center(max_lengths['Role'])} |", end="")
        print(f" {employee['employment_time'].center(max_lengths['Employment Time'])} |", end="")
        print()
    print(f"+{separator}+")



def interpret_input(description, employees):
    permissions = {}
    restrictions = {}
    
    days_pattern = r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
    days = re.findall(days_pattern, description, re.IGNORECASE)
    
    shifts = []
    if "morning" in description.lower():
        shifts.append("morning")
    if "afternoon" in description.lower():
        shifts.append("afternoon")
    
    # If no specific shift is mentioned, assume both shifts are affected
    if not shifts:
        shifts = ["morning", "afternoon"]
    
    for employee in employees:
        employee_name = employee['name'].lower()
        if employee_name in description.lower():
            shifts_for_employee = [f"{day.lower()}-{shift}" for day in days for shift in shifts]
            if "cannot work" in description.lower():
                restrictions[employee_name] = shifts_for_employee
            else:
                permissions[employee_name] = shifts_for_employee
            break

    return permissions, restrictions


def view_schedule(employees):
    permissions = {}
    restrictions = {}
    
    conflicts_present = input("\nAre there any dynamic conflicts for this week? (yes/no): ").strip().lower()
    while conflicts_present == 'yes':
        description = input("Please describe the conflicts or permissions for an employee (or type 'done' to finish): ")
        if description.lower() == 'done':
            break
        perms, restricts = interpret_input(description, employees)
        permissions.update(perms)
        restrictions.update(restricts)

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
    both_shifts = [emp for emp in employees if emp['role'] == 'both']

    # Shuffle the lists
    random.shuffle(kitchen_shifts)
    random.shuffle(barista_shifts)
    random.shuffle(both_shifts)

    max_shifts = {
        'full-time': 5,
        'part-time': 3
    }

    shifts_assigned = {emp['name'].lower(): 0 for emp in employees}
    daily_assigned = {}
    morning_staff = {'name': 'None'}

    for day in days_of_week:
        roles = ['kitchen', 'barista']
        shift_times = ['morning', 'afternoon']
        random.shuffle(roles)  # Randomly order the roles
        random.shuffle(shift_times)  # Randomly order the shift times
        
        for role in roles:
            for shift_time in shift_times:
                current_shifts = kitchen_shifts if role == 'kitchen' else barista_shifts
                staffer = assign_shift(role, current_shifts, both_shifts, max_shifts, shifts_assigned, daily_assigned, permissions, restrictions, day, shift_time)
                
                # Print the scheduled staffer
                if shift_time == 'morning':
                    morning_staff = staffer
                else:
                    print(f"| {day.center(13)} | {role.capitalize().center(8)} | {morning_staff['name'].center(23)} | {staffer['name'].center(24)} |")
                    print(separator)
                    
                # Update hours for each shift
                if staffer['name'] != 'None':
                    hours[staffer['name']] = hours.get(staffer['name'], 0) + (4 if shift_time == 'morning' else 5)
    
    print("\nEmployee Hours:".center(80, '-'))
    for employee, worked_hours in hours.items():
        print(f"{employee}: {worked_hours} hours")




def assign_shift(role, shifts, both_shifts, max_shifts, shifts_assigned, daily_assigned, permissions, restrictions, day, shift_time):
    shift_key = f"{day.lower()}-{shift_time}"
    
    # First, check if there's an available staffer from the 'both' role list
    for staffer in both_shifts:
        staffer_name = staffer['name'].lower()
        
        # Check if staffer is already assigned for the day
        if staffer_name in daily_assigned and day in daily_assigned[staffer_name]:
            continue
        
        # Check permissions and restrictions
        if staffer_name in permissions and shift_key not in permissions[staffer_name]:
            continue
        if staffer_name in restrictions and shift_key in restrictions[staffer_name]:
            continue
        
        # If staffer hasn't exceeded max shifts, assign them immediately
        if shifts_assigned[staffer_name] < max_shifts[staffer['employment_time']]:
            shifts_assigned[staffer_name] += 1
            if staffer_name not in daily_assigned:
                daily_assigned[staffer_name] = []
            daily_assigned[staffer_name].append(day)
            return staffer

    # If no 'both' staffer is available, proceed with the usual logic
    available_staffers = [s for s in shifts]
    best_staffer = None
    min_shifts_so_far = float('inf')
    
    for staffer in available_staffers:
        staffer_name = staffer['name'].lower()
        
        # Check permissions and restrictions
        if staffer_name in permissions and shift_key not in permissions[staffer_name]:
            continue
        if staffer_name in restrictions and shift_key in restrictions[staffer_name]:
            continue
        
        # If staffer hasn't exceeded max shifts, assign them immediately
        if shifts_assigned[staffer_name] < max_shifts[staffer['employment_time']]:
            shifts_assigned[staffer_name] += 1
            return staffer
        
        # Keep track of staffer with least shifts to possibly assign later
        if shifts_assigned[staffer_name] < min_shifts_so_far:
            min_shifts_so_far = shifts_assigned[staffer_name]
            best_staffer = staffer

    # If we found a staffer with the least shifts, assign them
    if best_staffer:
        shifts_assigned[best_staffer['name'].lower()] += 1
        return best_staffer

    # If no staffers available, return 'None'
    return {'name': 'None'}





def main():
    # Call the login function
    user = login()

    if user is None:
        return

    print(f"\nWelcome, {user}!")
    
    while True:
        employees = load_data()

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
            sys.exit(0)

        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()