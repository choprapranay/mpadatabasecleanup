from email.quoprimime import header_length

import pandas as pd

# #TO-DO:
#  - clean up files according to helen
#  - make merge nicer
#  - new file for birthday groupings after the new database is completely updated
#



mailchimp_file = "mailchimp member list paid 2025.csv"
bookwhen_file = "bookwhen 2025 members.csv"

df_mailchimp = pd.read_csv(mailchimp_file)
df_bookwhen = pd.read_csv(bookwhen_file)

new_data = pd.merge(df_bookwhen, df_mailchimp, on='Email Address')
new_data.to_csv('MPA FINAL Database.csv', index=False)
