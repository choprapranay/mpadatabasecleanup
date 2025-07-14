import pandas as pd
import numpy as np

# Load CSVs
mailchimp_file = "mailchimp member list paid 2025.csv"
bookwhen_file = "bookwhen 2025 members.csv"

df_mailchimp = pd.read_csv(mailchimp_file)
df_bookwhen = pd.read_csv(bookwhen_file)

# Organize and refactor files for only necessary columns
mailchimp_drop_cols = [
    "Renewing Payment 2024", "New Member Payment 2024", "Electronic Signature",
    "Form Submission Date", "Notes", "Elec Sig 2022", "Date (up to 2022)",
    "Date (up to 2021)", "Elec Sig 2021", "PAYMENT CONFIRMATION",
    "Payment Reminder", "MEMBER_RATING", "OPTIN_TIME", "OPTIN_IP",
    "CONFIRM_TIME", "CONFIRM_IP", "LATITUDE", "LONGITUDE", "GMTOFF",
    "DSTOFF", "TIMEZONE", "CC", "REGION", "New Member #", "New Member Payment 2024.1", "Renewing Payment 2024.1", "LAST_CHANGED",
    "LEID", "EUID", "NOTES", "TAGS", "Age"

]

bookwhen_drop_cols = [
    "Email status", "CustomerID", "Title", "First booking", "Latest booking",
    "First attendance", "Latest attendance", "Total bookings",
    "Total attendances", "Total confirmed attendances", "Cancelled tickets",
    "Transferred tickets", "Currency", "Bookings value", "Outstanding value",
    "Passes bought", "Pass uses remaining", "Pass expires at", "Thanks for volunteering.  When/how did you volunteer?",
    "Will you attend in person or online virtually?", "Child Attendee Name", "Child", "Full name"
]

df_mailchimp.drop(columns=[col for col in mailchimp_drop_cols if col in df_mailchimp.columns], inplace=True)
df_mailchimp.replace(0, np.nan, inplace=True) #helps account for birth years in the future

df_bookwhen.drop(columns=[col for col in bookwhen_drop_cols if col in df_bookwhen.columns], inplace=True)

# Merge the two files into one
merged_df = pd.merge(df_mailchimp, df_bookwhen, on="Email Address", how="outer", suffixes=('_mailchimp', '_bookwhen'))

# Function to merge two columns, as there duplicates from the files
def merge_columns(row, col_mailchimp, col_bookwhen):
    val = row.get(col_mailchimp)
    if pd.notna(val):
        return val
    return row.get(col_bookwhen)

# New column to consolidate birth years
merged_df["Birth Year_data"] = merged_df["Birthdate"].str[:4]

# List of column pairs to merge
column_pairs = [
    ("Phone Number_mailchimp", "Phone Number_bookwhen", "Phone Number"),
    ("Gender_mailchimp", "Gender_bookwhen", "Gender"),
    ("First Name", "First name", "Given Name"),
    ("Last Name", "Last name", "Surname"),
    ("City_mailchimp", "City", "City"),
    ("Volunteer_mailchimp", "Volunteer_bookwhen", "Volunteer"),
    ("Include my likeness on Association social media_mailchimp", "Include my likeness on Association social media_bookwhen", "Include my likeness on Association social media"),
    ("Address_mailchimp", "Address_bookwhen", "Address"),
    ("Year of Birth", "Birth Year_data", "Birth Year")
]

# Merge selected column pairs
for col1, col2, new_col in column_pairs:
    if col1 in merged_df.columns and col2 in merged_df.columns:
        merged_df[new_col] = merged_df.apply(lambda row: merge_columns(row, col1, col2), axis=1)

# Merge names
merged_df["Full Name"] = merged_df["Given Name"] + " " + merged_df["Surname"]

# Drop old versions of merged columns
cols_to_drop = []
for col1, col2, _ in column_pairs:
    if col1 in merged_df.columns:
        cols_to_drop.append(col1)
    if col2 in merged_df.columns:
        cols_to_drop.append(col2)
merged_df.drop(columns=cols_to_drop, inplace=True)

# Save final dataset
merged_df.to_csv("MPA FINAL Database.csv", index=False)