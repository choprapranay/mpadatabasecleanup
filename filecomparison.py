import pandas as pd

# Load CSV
db = pd.read_csv("MPA Final Database.csv",  encoding='latin1')
comparer_file = pd.read_csv("August clinic list.csv")

# Compare Emails
email_db = db["Email Address"].str.strip().str.lower()
email_comparer_file = comparer_file["Email"].str.strip().str.lower()

matching_emails = set(email_comparer_file).intersection(set(email_db))
not_matching_emails = set(email_comparer_file) - set(email_db)

#
for email in matching_emails:
    print(f" Matching emails: {email}")
for email in not_matching_emails:
    print(f" Not Matching emails: {email}")


#Send Mailchimp email
