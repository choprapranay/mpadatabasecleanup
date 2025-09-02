import hashlib
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
audience_list_id = APIKeys.audience_list_id_missing_information

df = pd.read_csv("MPA Final Database.csv")

df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df.replace({"": np.nan, " ": np.nan, "N/A": np.nan, "n/a": np.nan, "NA": np.nan}, inplace=True)

def phone_missing(val):
    if pd.isna(val):
        return True
    if isinstance(val, str) and val.strip() == "":
        return True
    return False

missing_phone_df = df[df["Phone Number"].apply(phone_missing)].copy()

added, updated, skipped_no_email = 0, 0, 0

for _, row in missing_phone_df.iterrows():
    email = (row.get("Email Address") or "").strip().lower()
    if not email:
        skipped_no_email += 1
        continue

    merge_fields = {
        "FNAME": row.get("Given Name", "") or "",
        "LNAME": row.get("Surname", "") or "",
        "MISSING": "Phone Number"
    }

    subscriber_hash = hashlib.md5(email.encode("utf-8")).hexdigest()
    body = {
        "email_address": email,
        "status_if_new": "subscribed",
        "merge_fields": merge_fields
    }

    try:
        member = mailchimp.lists.set_list_member(audience_list_id, subscriber_hash, body)
        if member.get("unique_email_id"):
            updated += 1
        else:
            added += 1
        print(f"UPSERTED {email} — missing: {merge_fields['MISSING']}")
    except ApiClientError as e:
        print(f"[ERROR] {email}: {e.text}")

print(f"\nSummary: targeted={len(missing_phone_df)}, upserted={added+updated}, skipped_no_email={skipped_no_email}")

campaign = mailchimp.campaigns.create({
    "type": "regular",
    "recipients": {"list_id": audience_list_id},
    "settings": {
        "subject_line": "We’re Missing Some Info From You",
        "title": "Missing Info Campaign",
        "from_name": "Milton Pickleball Association",
        "reply_to": "membership@miltonpickleball.com"
    }
})

campaign_id = campaign["id"]
print(f"Campaign created: {campaign_id}")

mailchimp.campaigns.set_content(campaign_id, {
        "html": """
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
      <p>Hi <strong>*|FNAME|*</strong>,</p>
      <p>We noticed we may be missing the following detail from your profile:</p>
      <p style="background-color: #ffecec; padding: 10px; border-left: 4px solid #cc0000;">
        <strong>*|MISSING|*</strong>
      </p>
      <p>Please reply with your phone number when you can, or email <a href="mailto:programs@miltonpickleball.com">programs@miltonpickleball.com</a>.</p>
      <p>Thanks!<br><em>Milton Pickleball Association</em></p>
    </body>
"""})

# Send Email
