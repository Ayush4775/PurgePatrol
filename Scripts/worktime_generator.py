import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker and set number of rows
fake = Faker()
num_rows = 5000

# Define the range for employee and project IDs
employee_id_range = range(1001, 4001)
project_id_range = range(1, 501)


# Function to generate worktimes
def generate_worktime():
    # Randomly choose if the employee was absent
    absent = random.choice([True, False])

    if absent:
        return {
            "work_date": fake.date_this_year(),
            "start_time": None,
            "end_time": None,
            "break_duration": None,
            "hours_worked": 0,
            "overtime": 0,
            "absent": True,
            "shift_type": None,
        }
    else:
        # Generate realistic start and end times
        start_hour = random.randint(6, 10)  # Work starts between 6 AM and 10 AM
        start_time = datetime.combine(fake.date_this_year(), datetime.min.time()) + timedelta(hours=start_hour,
                                                                                              minutes=random.randint(0,
                                                                                                                     59))

        # Normal shift duration (8-10 hours), with potential overtime
        end_time = start_time + timedelta(hours=8 + random.randint(0, 3), minutes=random.randint(0, 59))

        # Calculate hours worked and overtime
        total_hours_worked = (end_time - start_time).total_seconds() / 3600
        regular_hours = 8
        overtime = max(0, total_hours_worked - regular_hours)

        # Simulate break duration (typically between 30 min and 1 hour)
        break_duration = random.randint(30, 60)  # break in minutes

        # Determine shift type based on start time
        shift_type = "morning" if start_hour < 9 else "day" if start_hour < 12 else "evening"

        return {
            "work_date": start_time.date(),
            "start_time": start_time.time(),
            "end_time": end_time.time(),
            "break_duration": break_duration,
            "hours_worked": round(total_hours_worked, 2),
            "overtime": round(overtime, 2),
            "absent": False,
            "shift_type": shift_type,
        }


# Generate data
data = {
    "employee_id": [random.choice(employee_id_range) for _ in range(num_rows)],
    "project_id": [random.choice(project_id_range) for _ in range(num_rows)],
    **{
        key: [generate_worktime()[key] for _ in range(num_rows)]
        for key in
        ["work_date", "start_time", "end_time", "break_duration", "hours_worked", "overtime", "absent", "shift_type"]
    },
    "remarks": [fake.sentence(nb_words=8) for _ in range(num_rows)],  # Additional column for notes
}

# Create DataFrame and save as CSV
df = pd.DataFrame(data)
df.to_csv("employee_worktimes.csv", index=False)

# Display the first few rows of the dataset
print(df.head())
