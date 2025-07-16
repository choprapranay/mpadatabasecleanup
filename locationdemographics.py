import pandas as pd

# Load CSV File
df = pd.read_csv("MPA Final Database.csv")

# Initialize variables
milton_count = 0
haltonhills_count = 0
southern_halton_count = 0
other_count = 0
invalid_count = 0
count = 0
manual_count = 0

# Locate addresses column and iterate through the column
locations = df["Address"]

for location in locations:
    location = str(location)
    location = location.strip().lower()

    if "milton" in location:
        milton_count += 1
    elif "oakville" in location:
        southern_halton_count += 1
    elif "burlington" in location:
        southern_halton_count += 1
    elif "halton hills" in location:
        haltonhills_count += 1
    elif "nan" in location:
        invalid_count += 1
    else:
        manual_count += 1
        print(location) #manually find these

print(milton_count)
print(haltonhills_count)
print(southern_halton_count)
print(invalid_count)
print(manual_count)
print(count)