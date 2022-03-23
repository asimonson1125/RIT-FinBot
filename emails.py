import os
import imaplib
import email
from email.header import decode_header
import arrow
from dotenv import load_dotenv

load_dotenv('.env')


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

    headers = {
        "from": From,
        "subject": subject,
        "received": received,
        "msg": msg
    }
    return headers


def monthToNum(month):
    if month == "Jan":
        return "01"
    elif month == "Feb":
        return "02"
    elif month == "Mar":
        return "03"
    elif month == "Apr":
        return "04"
    elif month == "May":
        return "05"
    elif month == "Jun":
        return "06"
    elif month == "Jul":
        return "07"
    elif month == "Aug":
        return "08"
    elif month == "Sep":
        return "09"
    elif month == "Oct":
        return "10"
    elif month == "Nov":
        return "11"
    elif month == "Dec":
        return "12"
    else:
        raise Exception("Invalid month: " + month)


def getEmail(email_id):
    res, msg = emailClient.fetch(str(email_id), "(RFC822)")
    return msg


emailClient = mail_init()
messages = getMessages()  # message count
for i in range(messages):
    mail = getEmail(i + 1)
    headers = getHeaders(mail)
    From = "updates@vitalknowledge.net"
    if (headers["from"].__contains__(From)):
        print(headers["from"], headers["subject"])
        received = headers["received"][headers["received"].index(',') + 2:headers["received"].index('(') - 1]
        time = received.split(" ")
        time[1] = monthToNum(time[1])
        received = " ".join(time)
        print(arrow.get(received, "DD MM YYYY HH:mm:ss Z").to('local'))
        print("\n")
