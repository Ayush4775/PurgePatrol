import pandas as pd
from faker import Faker
import random
from datetime import timedelta

# Initialize Faker and set number of rows
fake = Faker()
num_rows = 500

# List of specified project leaders
project_leaders = [
    "Myriam Givens", "Dheepa Nguyen", "Bartholemew Khemmich", "Xana Potts",
    "Prater Jeremy", "Kaylah Moon", "Kristen Tate", "Bobby Rodgers",
    "Reid Park", "Hector Dalton", "Mariela Schultz", "Angela Molina",
    "Gerald Preston", "Reilly Moyer", "Carlee French", "Jaydon Blackburn",
    "Bridger Carter", "Leon Beard", "Charity Miranda", "Axel Howe"
]

# Define the range for employee IDs and the maximum number per project
employee_id_range = range(1001, 4001)
max_employees_per_project = 30

# Function to generate random employee IDs for each project
def random_employees():
    # Choose a random number of unique employee IDs up to the max allowed
    employee_ids = random.sample(employee_id_range, random.randint(1, max_employees_per_project))
    # Convert to a comma-separated string
    return ",".join(map(str, employee_ids))

# Generate data
data = {
    "id": range(1, num_rows + 1),
    "billing_date": [fake.date_this_decade() for _ in range(num_rows)],
    "due_date": [(fake.date_this_decade() + timedelta(days=random.randint(30, 180))) for _ in range(num_rows)],
    "status": [random.choice(["active", "completed", "pending", "on hold"]) for _ in range(num_rows)],
    "project_leader": [random.choice(project_leaders) for _ in range(num_rows)],  # Randomly select from the specified project leaders
    "total_hours": [random.randint(50, 500) for _ in range(num_rows)],
    "start_date": [fake.date_this_decade() for _ in range(num_rows)],
    "finish_date": [fake.date_this_decade() if random.choice([True, False]) else None for _ in range(num_rows)],
    "employees": [random_employees() for _ in range(num_rows)],
    "description": [fake.sentence(nb_words=6) for _ in range(num_rows)],
    "budget": [random.randint(5000, 50000) for _ in range(num_rows)],
    "client": [fake.company() for _ in range(num_rows)],
}

# Create DataFrame and save as CSV
df = pd.DataFrame(data)
df.to_csv("project_data.csv", index=False)

# Display the first few rows of the dataset
print(df.head())
