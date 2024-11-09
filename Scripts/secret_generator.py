import pandas as pd
import random
import string

# Load employee data from CSV
employee_data = pd.read_csv("employee_data.csv")

# Select the first 25 rows of data from employee_data.csv
employee_sample = employee_data.head(25).copy()

# Function to generate a SecretSequence with five sequences of 10 random characters each
def generate_secret_sequence():
    return "-".join(
        "".join(random.choices(string.ascii_letters + string.digits, k=10))
        for _ in range(5)
    )

# Add the SecretSequence column to the employee_sample DataFrame
employee_sample["SecretSequence"] = [generate_secret_sequence() for _ in range(len(employee_sample))]

# Rearrange columns to place SecretSequence after EmpID, matching the order you specified
final_columns_order = [
    "EmpID", "SecretSequence", "FirstName", "LastName", "StartDate", "ExitDate", "Title", "Supervisor", "ADEmail",
    "BusinessUnit", "EmployeeStatus", "EmployeeType", "PayZone", "EmployeeClassificationType", "TerminationType",
    "TerminationDescription", "DepartmentType", "Division", "DOB", "State", "JobFunctionDescription", "GenderCode",
    "LocationCode", "RaceDesc", "MaritalDesc", "Performance Score", "Current Employee Rating"
]
employee_sample = employee_sample[final_columns_order]

# Display the first few rows of the final dataset to confirm
print(employee_sample.head())

# Optionally, save the new dataset to a CSV file
employee_sample.to_csv("secret_data.csv", index=False)
