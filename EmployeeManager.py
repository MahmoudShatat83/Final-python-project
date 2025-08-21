# The code consists of the following sections:
# 1. OOP with class to deal with records; the class contains five user-interactive method; they are:
# 2. Add employee method
# 3. View employees records method
# 4. Update employee method
# 5. Delete employee record method
# 6. search employee method
# beside another two internal methods to exchande data between the in-memory and csv files; they are:
# 7. Load_employee method
# 8. Save_employee method
# and another two:
# 9. Display_menu method: to display the main menu
# 10. run method: to run the code
# Moreover, two lib with different objectives; they are:
# 11. csv
# 12. os 
# I put also validation on salary (numeric values) and email (must contain @ sign)
##=====================================================================================================================================================================


import csv  # to interact with CSV files
import os   # to be able to check the existance of CSV file

class EmployeeManager:
    # class to deal with employee records.

    def __init__(self, filename='employees.csv'): 
        
        # Initializes the EmployeeManager.
        # filename: employee.csv _ the CSV file to store employees data.
        
        self.filename = filename  # path/name of the CSV file (default: employees.csv).
        self.employees = {}       # new dictionary to store the records in Python memory
        self.load_employees()     # this is to call the method load_employees() exactly at start up

    # The method responsible for retrieving data from CSV file into python memory {dictionary created above}

    def load_employees(self):
        
        if not os.path.exists(self.filename):
            return            # If the file doesn’t exist yet, it simply returns

        with open(self.filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.employees[row['ID']] = row

                # csv.DictReader read rows as dictionary using the header row for keys

   

    # The method responsible for saving data from python memory {dictionary created above} into CSV file 

    def save_employees(self):        
        
        if not self.employees:
            # If no employees, create an empty file with headers and creates an empty file with headers

            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)                                         # creates csv writer
                writer.writerow(['ID', 'Name', 'Position', 'Salary', 'Email'])    # write one raw; that is the header only
            return

        fieldnames = ['ID', 'Name', 'Position', 'Salary', 'Email']    # to define the columns names; matches the keys in python dictionary
        with open(self.filename, mode='w', newline='') as file:       # overwrite also the old csv
            writer = csv.DictWriter(file, fieldnames=fieldnames)      # write the dictionary as row in csv, I use fieldnames as ordered  
            writer.writeheader()                                      # write the header
            writer.writerows(self.employees.values())                 # each employee is a dictionary, all employees is a list of dictionaries keyed by ID, and this will be written as row in csv



    # The method responsible for collecting from the user a new record for an employee and store in self.employees dict 

    def add_employee(self):
       
        print("\n--- Add New Employee ---")                                        # user instruction
        while True:                                                                # using while true to keep asking the user until enter a valid number
            emp_id = input("Enter Employee ID: ")
            if not emp_id.isdigit():
                print("Invalid input. Employee ID must contain only numbers.")
                continue                                                           # break out the loop and continue to the rest
            if emp_id in self.employees:                                           # put a condition to check the ID is not duplicated (ID is unique)
                print(f"Error: Employee with ID {emp_id} already exists.")
                continue
            break                                                                  # exit the loop

        name = input("Enter Employee Name: ")                                      # collect name
        position = input("Enter Position: ")                                       # collect position
        
        while True:                                                                # using while true to keep asking the user until enter a valid number 
            try:
                salary = float(input("Enter Salary: "))                            # float: convert the input into floating-point number
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
        
         
        while True:                                                                # another validation for email
            email = input("Enter Email: ")
            if "@" not in email:
                    print("Invalid email string.")
                    continue
            break

        self.employees[emp_id] = {                          # add a new dictionary of one employee details in the parent dictionary {key:ID, value:{employee details}}
            'ID': emp_id,
            'Name': name,
            'Position': position,
            'Salary': salary,
            'Email': email
        }
        self.save_employees()                                                      # call the method (save employees)
        print(f"Employee with ID {emp_id} added successfully.")

    # The method responsible for displaying all employees 
    def view_all_employees(self):
        
        print("\n--- All Employees ---")
        if not self.employees:                                                     # if there is no employees print below message
            print("No employees found.")
            return                                                                 # exit early, don't run the rest of code

        for emp in self.employees.values():                                        # extract only the values of the parent dictionary (output: each employee record)
            print("-" * 30)
            for key, value in emp.items():                                         # items to return both key and values
                print(f"{key}: {value}")
        print("-" * 30)

    # The method responsible for updating the details of an existing employee by his/her ID
    def update_employee(self):
       
        print("\n--- Update Employee ---")
        emp_id = input("Enter the ID of the employee to update: ")                 # to ask the user for the ID
        if emp_id not in self.employees:                                           # if ID does not exist print error message
            print(f"Error: Employee with ID {emp_id} not found.")
            return                                                                 # exit early

        emp = self.employees[emp_id]                                               # get the employee record from self.employee
        print(f"Updating details for Employee ID: {emp_id}")

        name = input(f"Enter new Name (current: {emp['Name']}): ")                 # ask the user for an updated record while showing the current for help
        if name:
            emp['Name'] = name                                                     # overwrite the current value

        position = input(f"Enter new Position (current: {emp['Position']}): ")     # same like Name
        if position:
            emp['Position'] = position

        while True:                                                                
            salary_input = input(f"Enter new Salary (current: {emp['Salary']}): ")
            if not salary_input:
                break
            try:
                emp['Salary'] = float(salary_input)
                break
            except ValueError:
                print("Invalid input. Please enter a number or leave it blank.")
                
        while True:
            email = input(f"Enter new Email (current: {emp['Email']}): ").strip()
            if not email:   
                break
            if "@" not in email:
                print("Invalid email string.")
                continue
            emp['Email'] = email
            break


        self.save_employees()
        print(f"Employee with ID {emp_id} updated successfully.")

    # The method responsible for deleting an employee by his/her ID
    def delete_employee(self):
    
        print("\n--- Delete Employee ---")
        emp_id = input("Enter the ID of the employee to delete: ")
        if emp_id in self.employees:
            del self.employees[emp_id]                                             # deletes the record for this ID
            self.save_employees()                                                  # update the csv without this ID record
            print(f"Employee with ID {emp_id} deleted successfully.")
        else:
            print(f"Error: Employee with ID {emp_id} not found.")

    # The method responsible for searching for an employee by his/her ID and displaying his/her details
    def search_employee(self):
      
        print("\n--- Search Employee ---")
        emp_id = input("Enter the ID of the employee: ")
        if emp_id in self.employees:
            emp = self.employees[emp_id]
            print("-" * 30)
            for key, value in emp.items():
                print(f"{key}: {value}")
            print("-" * 30)
        else:
            print(f"Error: Employee with ID {emp_id} not found.")

    # The method responsible for displaying the main menu of the program
    def display_menu(self):
        
        print("\n===== Employee Data Management System =====")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Search Employee")
        print("6. Exit")
        print("=" * 45)

    # The method responsible for running the program, dealing with user inputs and main menu
    def run(self):
        
        while True:                                                             # infinite loop
            self.display_menu()
            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                self.add_employee()
            elif choice == '2':
                self.view_all_employees()
            elif choice == '3':
                self.update_employee()
            elif choice == '4':
                self.delete_employee()
            elif choice == '5':
                self.search_employee()
            elif choice == '6':
                print("Exiting the program. Goodbye!")
                break                                                           # exit the while true loop
            else:                                                               # any other input rather than 1 to 6, will fall in else branch
                print("Invalid choice. Please enter a number between 1 and 6.") 

if __name__ == "__main__":
    manager = EmployeeManager()                                                 # creates an object of EmployeesManager class

    manager.run()                                                               # call run method

