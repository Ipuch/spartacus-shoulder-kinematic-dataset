from itertools import product
import csv

# Update the risk values
categories_updated = [
    {
        'name': 'Medical Imagery',
        'options': [
            ('Yes', 0),
            ('No', 2)
        ]
    },
    {
        'name': 'Intracortical Pins',
        'options': [
            ('Without Imagery', 2),
            ('With Imagery', 0)
        ]
    },
    {
        'name': 'Thoraco-humeral Angle',
        'options': [
            ('Euler Angles', 0),
            ('Projected Angle', 4),
            ('User Controlled Angle', 9),
        ]
    },
    {
        'name': 'Parent Segment Frame',
        'options': [
            ('ISB', 0),
            ('ISB-like', 2),
            ('Literature Correction', 2),
            ('ISB-like and Literature Correction', 9),
        ]
    },
    {
        'name': 'Child Segment Frame',
        'options': [
            ('ISB', 0),
            ('ISB-like', 2),
            ('Literature Correction', 2),
            ('ISB-like and Literature Correction', 9),
        ]
    }
]

# Generate all possible combinations of options
combinations_updated = product(*(category['options'] for category in categories_updated))

# Calculate cumulative risk for each combination and sort by risk
sorted_combinations_updated = sorted(
    ((comb, sum(option[1] for option in comb)) for comb in combinations_updated),
    key=lambda x: x[1]
)

# Display a sample of the sorted combinations
print("Individual risks: ", sorted_combinations_updated[0])
# cumulative risk
print("Cumulative risk: ", sorted_combinations_updated[0][1])

# Prepare data for CSV
csv_data = []
headers = [category['name'] for category in categories_updated] + ['Cumulative Risk']

for comb, risk in sorted_combinations_updated:
    row = [option[0] for option in comb] + [risk]
    csv_data.append(row)

# Save data to CSV file
file_path = "risk_combinations.csv"
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(csv_data)

