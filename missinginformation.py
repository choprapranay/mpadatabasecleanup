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
audience_list_id = "[NEED A NEW KEY]"

# Load CSV file
df = pd.read_csv("MPA Final Database.csv")
df.replace(" ", np.nan, inplace=True)


important_fields = ["Phone Number", "Address", "Birthdate"]

# Find the missing fields and relate it back to user email
for index, row in df.iterrows():
    missing_columns = [col for col in important_fields if pd.isna(row.get(col))]

    if missing_columns:
        email = row["Email Address"]

        merge_fields = {
            "FNAME": row.get("Given Name", ""),
            "LNAME": row.get("Surname", ""),
            "MISSING": ", ".join(missing_columns) #TO-DO: NEED TO ADD IN MAILCHIMP
        }

        member_info = {
            "email_address": email,
            "status_if_new": "subscribed",
            "merge_fields": merge_fields
        }

# Add emails to a mailchimp audience
        try:
            response = mailchimp.lists.add_list_member(audience_list_id, member_info)
            print(f"Added {email} — missing: {merge_fields['MISSING']}")
        except ApiClientError as error:
            print(f"Error with {email}: {error.text}")


# Create a Mailchimp campign
campaign = mailchimp.campaigns.create({
    "type": "regular",
    "recipients": {
        "list_id": audience_list_id
    },
    "settings": {
        "subject_line": "We’re Missing Some Info From You",
        "title": "Missing Info Campaign",
        "from_name": "Milton Pickleball Association",
        "reply_to": "pranaychopra6@gmail.com"
    }
})

campaign_id = campaign["id"]
print(f"Campaign created: {campaign_id}")

# Create email content
mailchimp.campaigns.set_content(campaign_id, {
    "html":
    """
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <p>Hi <strong>*|FNAME|*</strong>,</p>

    <p>We hope you're enjoying being part of the Milton Pickleball Association (MPA) and that your experience with us has been a great one so far!</p>

    <p>As part of a recent update to our member records, we noticed that a few key details are still missing from your file:</p>

    <p style="background-color: #ffecec; padding: 10px; border-left: 4px solid #cc0000;">
      <strong>*|MISSING|*</strong>
    </p>

    <p>This isn’t urgent, but it would really help our team (and future communication) if you could provide this information at your convenience.</p>

    <p>You can simply:</p>
    <ul>
      <li>Reply directly to this email with the missing info</li>
      <li>Or email us at <a href="mailto:programs@miltonpickleball.com">programs@miltonpickleball.com</a></li>
    </ul>

    <p>Thanks so much for being part of MPA—we’re grateful to have you in our community!</p>

    <p>Warm regards,</p>

    <p><em>[Your Name]<br>
    [Your Title/Role]<br>
    Milton Pickleball Association</em></p>

    <p style="font-size: 12px; color: #888;">
      Sent on behalf of <a href="mailto:programs@miltonpickleball.com">programs@miltonpickleball.com</a> and <a href="mailto:treasurer@miltonpickleball.com">treasurer@miltonpickleball.com</a>
    </p>
  </body>
    """
})

# Send Email
