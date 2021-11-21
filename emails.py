import os
import imaplib
import email
from email.header import decode_header

def mail_init():
    user = os.getenv("email")
    app_password = os.getenv("gmailAppPass")
    gmail_host = 'imap.gmail.com'
    emailClient = imaplib.IMAP4_SSL(gmail_host)
    emailClient.login(user, app_password)
    return emailClient


def close():
    emailClient.close()
    emailClient.logout()


def getMessages():
    status, emails = emailClient.select("INBOX")
    if (not status):
        raise Exception("Email server connection failed")
    emails = int(emails[0])
    return emails


def getHeaders(response):
    # parse a bytes email into a message object
    msg = email.message_from_bytes(response[0][1])
    # decode the email subject
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        # if it's a bytes, decode to str
        subject = subject.decode(encoding)
    # decode email sender
    From, encoding = decode_header(msg.get("From"))[0]
    if isinstance(From, bytes):
        From = From.decode(encoding)
    received, encoding = decode_header(msg.get("Received"))[0]
    if isinstance(received, bytes):
        received = received.decode(encoding)
    return msg, subject, From, received


def getEmail(email_id):
    res, msg = emailClient.fetch(str(email_id), "(RFC822)")
    return msg


from dotenv import load_dotenv
load_dotenv('.env')
emailClient = mail_init()
messages = getMessages()  # message count
for i in range(messages):
    mail = getEmail(i + 1)
    content, mailSub, mailFrom, received = getHeaders(mail)
    print(mailFrom, mailSub)
    received = received[received.index(',') + 2:]
    received = received[:received.index('-') - 1]  # This will break if local timezone is not behind UDT
    print(received)  # the time that the message was received in local time
    print("\n" * 3)
