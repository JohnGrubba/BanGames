import json
import random, string
from expiringdict import ExpiringDict
from ezdatabase import db
from Emailer import send_mail

print("Initializing Databases")
tmpaccs = ExpiringDict(max_len=100, max_age_seconds=30)
accs_keys = db("accounts.json")
email_to_pswd = {}
for key in accs_keys:
    email_to_pswd[accs_keys[key]["email"]] = {
        "password": accs_keys[key]["password"],
        "key": key,
    }


def request_account(payl, base_url):
    try:
        email = payl["email"]
        password = payl["pswd"]
    except:
        return {"status": "error"}

    acc_key = "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(64)
    )
    tmpkey = "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(64)
    )
    tmpaccs[tmpkey] = {"email": email, "password": password, "key": acc_key}
    if send_mail(base_url + "confirm/" + tmpkey, email):
        return {"status": "ok"}
    else:
        return {"status": "error", "message": "Invalid Email"}


def activate_account(tmpkey):
    try:
        acc = tmpaccs[tmpkey]
    except KeyError:
        return "<h1>Expired or Invalid Key</h1>"
    accs_keys[acc["key"]] = acc
    email_to_pswd[acc["email"]] = {
        "password": acc["password"],
        "key": acc["key"],
    }
    del tmpaccs[tmpkey]
    return "<h1>Account Created Successfully</h1>"


def login(payl):
    try:
        email = payl["email"]
        password = payl["pswd"]
    except:
        return {"status": "error"}
    # Check Password
    try:
        if email_to_pswd[email]["password"] != password:
            return {"status": "error", "message": "Invalid Password"}
        else:
            key = email_to_pswd[email]["key"]
            return {"status": "ok", "data": key}
    except KeyError:
        return {"status": "error", "message": "Account doesn't exist"}
