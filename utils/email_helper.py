# utils/email_helper.py
import imaplib
import email
from email.policy import default
import re
import time

def get_activation_link(username, password, retries=5, delay=15):
    activation_link = None
    for attempt in range(retries):
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(username, password)
            mail.select("inbox")

            result, data = mail.search(None, '(UNSEEN SUBJECT "Activate Patient Account")')
            if result == "OK":
                for num in data[0].split():
                    result, msg_data = mail.fetch(num, "(RFC822)")
                    if result == "OK":
                        msg = email.message_from_bytes(msg_data[0][1], policy=default)
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/html":
                                    body = part.get_payload(decode=True).decode()
                                    match = re.search(r'href="(https?://\S+)"', body)
                                    if match:
                                        activation_link = match.group(1)
                                        break
                        else:
                            body = msg.get_payload(decode=True).decode()
                            match = re.search(r'href="(https?://\S+)"', body)
                            if match:
                                activation_link = match.group(1)
                    if activation_link:
                        break
            mail.logout()
            if activation_link:
                break
        except imaplib.IMAP4.error as e:
            print(f"Attempt {attempt + 1}/{retries} failed with error: {e}")
        if not activation_link:
            print(f"Email not found. Retrying in {delay} seconds...")
            time.sleep(delay)
    return activation_link
