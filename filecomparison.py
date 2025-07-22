import pandas as pd
from mailchimp_marketing.api_client import ApiClientError
import APIKeys
from mailchimp_marketing import Client


# Initialize Mailchimp
mailchimp = Client()
mailchimp.set_config({
    "api_key": APIKeys.api_key_mailchimp,
    "server": "us4"
})
audience_list_id = APIKeys.audience_id_key_filecomparison
#campaign_id = APIKeys.campaign_id_filecomparsion

# Load CSV
db = pd.read_csv("MPA Final Database.csv",  encoding='latin1')
comparer_file = pd.read_csv("August clinic list.csv")

# Compare Emails
email_db = db["Email Address"].str.strip().str.lower()
email_comparer_file = comparer_file["Email"].str.strip().str.lower()

matching_emails = set(email_comparer_file).intersection(set(email_db))
not_matching_emails = set(email_comparer_file) - set(email_db)


# Add emails to a mailchimp audience
for email in not_matching_emails:
    try:
        mailchimp.lists.add_list_member(audience_list_id, {
            "email_address": email,
            "status": "subscribed",

        })
        print(f"Added: {email}")
    except ApiClientError as error:
        print(f"Error with {email}: {error.text}")

#Create a mailchimp campagin in order to send email
campaign = mailchimp.campaigns.create({
    "type": "regular",
    "recipients": {
        "list_id": audience_list_id,
    },
    "settings": {
        "subject_line": "Thank You for Your Interest in MPA and Our Pickleball Clinics",
        "title": "MPA Newsletter",
        "from_name": "Milton Pickleball Association",
        "reply_to": "pranaychopra6@gmail.com"
    }
})
campaign_id = campaign["id"]

mailchimp.campaigns.set_content(campaign_id, {
    "html": """
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <p>Hi <strong>*|FNAME|*</strong>,</p>

    <p>Thank you so much for your interest in the <strong>Milton Pickleball Association (MPA)</strong> and for signing up for one (or both!) of our upcoming clinics. We’re always excited to welcome players into our community—whether you're new to the sport or looking to take your game to the next level.</p>

    <p>You are receiving this email because you registered for:</p>

    <p><strong>Pickleball Clinic for 55+ Players</strong><br>
    📅 Monday, August 12 at 10:00 AM<br>
    💲 $65 for non-MPA members<br>
    🔗 <a href="https://bookwhen.com/miltonpickleball/e/ev-s7id-20250812100000" target="_blank">View Details / Register</a></p>

    <p><strong>or</strong></p>

    <p><strong>Advancing from 3.0 to 3.5 Clinic</strong><br>
    📅 Tuesday, August 27 at 6:00 PM<br>
    💲 $70 for non-MPA members<br>
    🔗 <a href="https://bookwhen.com/miltonpickleball/e/ev-stxn-20250827180000" target="_blank">View Details / Register</a></p>

    <p>If you’d prefer not to become a full MPA member, you can simply pay the $15 difference between the member and non-member clinic rate by sending an e-transfer to:<br>
    📧 <a href="mailto:treasurer@miltonpickleball.com">treasurer@miltonpickleball.com</a></p>

    <p>Alternatively, becoming an MPA member for just $25/year gives you access to all of our programs at reduced rates and connects you to a vibrant and welcoming pickleball community here in Milton.</p>

    <p><strong>👉 <a href="https://bookwhen.com/miltonpickleball/e/ev-sl9j-20250101000000" target="_blank">Become an MPA Member – $25/year</a></strong></p>

    <p>If you have any questions, feel free to reach out—we’re happy to help.</p>

    <p>Looking forward to seeing you on the courts,</p>

    <p><em>Pranay Chopra<br>
    Summer Intern<br>
    Milton Pickleball Association</em></p>

    <p style="font-size: 12px; color: #888;">
      Sent on behalf of <a href="mailto:programs@miltonpickleball.com">programs@miltonpickleball.com</a> and <a href="mailto:treasurer@miltonpickleball.com">treasurer@miltonpickleball.com</a>
    </p>
  </body>
    """
})

try:
    response = mailchimp.campaigns.send_test_email(
        campaign_id,
        body={
            "test_emails": ["pranaychopra6@gmail.com"],
            "send_type": "html"
        }
    )
    print("Test email sent successfully!")
except ApiClientError as error:
    print(f"Error sending test email: {error.text}")
