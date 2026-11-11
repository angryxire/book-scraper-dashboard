import json
import urllib.request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

def send_discord_alert(title, price, link_url):

	webhook_url = "https://discord.com/api/webhooks/1569017429814939721/_6rf34IQTI5dqWVrYKVjMh6h-a8TZtoN2WzbTa4Umn7EI9yrROnAaaLTNMAKPVK0mb-t"

	message_content = (
		f" **NEW DEAL FOUND BELOW THRESHOLD!**\n"
		f"**Listing:** {title}\n"
		f"**Price:** ${price}\n"
		f" **deep Link:** {link_url}\n"
		f"-----------------------------------------"
	)
	payload = json.dumps({"content": "".join(message_content)}).encode("utf-8")
	req = urllib.request.Request(
		webhook_url,
		data=payload,
		headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
	)

	try:
		# with urllib.request.urlopen(req) as response:
		urllib.request.urlopen(req)
		print(f"   [discord Alert Triggered] Lead found: {title[:15]}...")

	except Exception as e:
		print(f"   [discord Alert Triggered] silent block hit: {e}.")

def send_email_alert(title, price, link_url):

	msg = MIMEText(
		f" **NEW DEAL FOUND BELOW THRESHOLD!**\n"
		f"**Listing:** {title}\n"
		f"**Price:** ${price}\n"
		f" **deep Link:** {link_url}\n"
		f"-----------------------------------------"
	)
	msg['Subject'] = f" Market Alert: Low Price Found (${price})"
	msg['From'] = config.SENDER_EMAIL
	msg['To'] = config.RECEIVER_EMAIL

	try:

		with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
			server.login(config.SENDER_EMAIL, config.APP_PASSWORD)
			server.sendmail(config.SENDER_EMAIL,config.RECEIVER_EMAIL , msg.as_string())

	except Exception as email_error:
		print(f"  [Email Pipeline] Silent block hit: {email_error}.")


