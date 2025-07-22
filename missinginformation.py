import pandas as pd
import numpy as np
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import APIKeys

# Mailchimp API Integration
mailchimp = Client()
mailchimp.set_config({
    "api_key": APIKeys.api_key_mailchimp,
    "server": "us4"
})

# Load CSV file
df = pd.read_csv("MPA Final Database.csv")
df.replace(" ", np.nan, inplace=True)

# Add emails for indivuals with missing values to mailchimp audience
tag_name = "missing_information"
audience_list_id = "c6c4104aba"

#REFACTOR CODE COMPLETELY.
for index, row in df.iterrows():
    missing_columns = row[row.isna()].index.tolist()

    if missing_columns:
        email = row.iloc[0]  # assuming first column is email
        merge_fields = {
            "FNAME": row.get("Given Name", ""),
            "LNAME": row.get("Surname", ""),
        }

        member_info = {
                "email_address": email,
                "status": "subscribed",
                "merge_fields": merge_fields
        }

        # try:
        #     response = mailchimp.lists.add_list_member(audience_list_id, member_info)
        #     print("response: {}".format(response))
        # except ApiClientError as error:
        #     print("An exception occurred: {}".format(error.text))


# campaign = mailchimp.campaigns.create({
#     "type": "regular",
#     "recipients": {
#         "list_id": audience_list_id  # sends to the whole audience
#     },
#     "settings": {
#         "subject_line": "We’re Missing Some Info From You",
#         "title": "Missing Info Campaign",
#         "from_name": "Your Name or Organization",
#         "reply_to": "youremail@example.com"
#     }
# })
#
# campaign_id = campaign["id"]
# print(f"✅ Campaign created: {campaign_id}")
