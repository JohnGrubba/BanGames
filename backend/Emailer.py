import smtplib, ssl


print("Initializing Email Server")
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
context = ssl.create_default_context()
server = smtplib.SMTP_SSL(smtp_server, port, context=context)
sender_email = "nicjontrickshots@gmail.com"  # Enter your address
password = open("EMAILKEY.env", "r").read()
server.login(sender_email, password)


def send_mail(url, receiver):
    message = f"""\
    Subject: Confirm your Account Creation

    Click on this Link to Create your Account for BAN Games: {url}"""
    try:
        server.sendmail(sender_email, receiver, message)
    except smtplib.SMTPRecipientsRefused:
        return False
    return True
