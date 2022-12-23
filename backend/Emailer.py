import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


print("Initializing Email Server")
server = smtplib.SMTP("smtp.office365.com", 587)
sender_email = "bangames@outlook.de"
password = open("EMAILKEY.env", "r").read()
server.starttls()
server.login(sender_email, password)


def send_mail(url, receiver) -> bool:
    server.login(sender_email, password)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Confirm your Account Creation for BanGames"
    msg["From"] = sender_email
    msg["To"] = receiver
    with open("confirm_email.html", "r") as f:
        html = f.read()
        html = html.replace("{CONFIRMATION_LINK}", url)
        message = MIMEText(html, "html")
    msg.attach(message)
    try:
        server.sendmail(sender_email, receiver, msg.as_string())
    except smtplib.SMTPRecipientsRefused:
        return False
    print("Email Sent")
    return True
