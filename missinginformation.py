import pandas as pd
import numpy as np

# Load CSV file
df = pd.read_csv("MPA Final Database.csv")
df.replace(" ", np.nan, inplace=True)

# Find missing values in file with its associated email address
for row_idx, col_idx in zip(*np.where(df.isna())):
    print(f"EMAIL FOR MISSING VALUE:{df.iloc[row_idx,0]}, DATA THAT IS MISSING: '{df.columns[col_idx]}'")

# TO-DO:
# - use emails to send a mail on mailchimp to get all the missing information.
