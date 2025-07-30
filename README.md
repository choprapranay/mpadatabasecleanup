# 🧹 MPA Database Cleanup

A Python-based automation script designed to help the **Milton Pickleball Association (MPA)** maintain a clean and complete membership database.

This tool:
- Scans through BookWhen's and Mailchimp's contact CSV exports
- Detects missing fields such as phone number, city, or emergency contact
- Filters and outputs a list of affected members
- Sends customized follow-up emails using the Mailchimp API
- Optionally enriches address data using Google Maps API

### 💡 Why This Exists

Managing community memberships can get messy — especially when people leave fields blank during registration. This script helps automate that cleanup process, reduce manual checking, and speed up member communications.

### 🔗 Integrations
- ✅ **BookWhen** / **Mailchimp** — for importing contact CSVs
- ✅ **Mailchimp API** — to send automated emails to members (with a big use case of incomplete info)
- ✅ **Google Maps API** — to determine missing city info based on street addresses

### 📊 Output

- Filtered CSV of members missing required fields
- Summary in CSV's of how many members are missing each field
- Optional email notifications for missing information
- Supplementary data exports to support grant applications and reporting

**Built for internal use at the **Milton Pickleball Association** — but adaptable for any organization managing membership data.**
