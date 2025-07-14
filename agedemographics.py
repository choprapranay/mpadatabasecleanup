import pandas as pd

# Load CSV File
df = pd.read_csv("MPA Final Database.csv")

preschool_count = 0
children_count = 0
youth_count = 0
adult_count = 0
older_adult_count = 0
no_data_count = 0
curr_year = 2025

# Locate birth year column and iterate through the column
birthyears = df["Birth Year"]

for year in birthyears:
    if curr_year - year >= 55:
        older_adult_count += 1
    elif 18 <= curr_year - year < 55:
        adult_count += 1
    elif 13 <= curr_year - year < 18:
        youth_count += 1
    elif 6 <= curr_year - year < 13:
        children_count += 1
    elif 0 < curr_year - year < 6:
        preschool_count += 1
    else:
        no_data_count += 1

data = {
    "older adults": [older_adult_count],
    "adults": [adult_count],
    "youths": [youth_count],
    "children": [children_count],
    "preschools": [preschool_count],
    "no data": [no_data_count]
}

# Create new data frame using the above data and export it as a CSV
new_df = pd.DataFrame(data)
new_df.to_csv("Age Demographics.csv", index=False)