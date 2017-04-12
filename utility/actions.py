from random import randint
import time
import httplib, urllib
import smtplib
from email.mime.text import MIMEText
import os
import logging
from utility.constants import REA_ROOT_LOGGER

logger = logging.getLogger(REA_ROOT_LOGGER + '.ACTIONS')


def show_progress(cur_num, tot_num, intvl, msg=''):
    if cur_num and tot_num:
        if cur_num > tot_num:
            cur_num = tot_num

        if cur_num % intvl == 0 or cur_num == tot_num:
            percent = round(float(cur_num) * 100.0 / float(tot_num), 2)
            logger.info(str(percent) + "% finished. " + msg)
            return True

    return False


def get_hms(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)


def rand_wait(msg, min_wait=10, max_wait=30):
    wait_time = randint(min_wait, max_wait)
    print (str(msg) + " | Waiting " + str(wait_time) + "s ...")
    time.sleep(wait_time)


def except_response(err_msg):
    print(err_msg)
    print("Exception thrown. Continue? Y/N ")
    try:
        send_email("Exception", err_msg)
    except smtplib.SMTPAuthenticationError:
        print ("Failed to send email notification")

    valid = {"yes": True, "y": True, "ye": True}
    choice = raw_input().lower()
    if choice in valid:
        return
    else:
        exit(0)


def push_notification(msg):
    token = os.environ['PUSHOVER_APP_TOKEN']
    user = os.environ['PUSHOVER_USER_KEY']
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urllib.urlencode({
                     "token": token,
                     "user": user,
                     "message": msg,
                 }), {"Content-type": "application/x-www-form-urlencoded"})
    conn.getresponse()


def send_email(msg_subject, msg_body):
    app_user = os.environ['APP_USER']
    app_pass = os.environ['GOGL_APP_PASS']
    email = os.environ['EMAIL']
    msg = MIMEText(msg_body)
    msg['Subject'] = 'RET ALERT: ' + msg_subject

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(app_user, app_pass)
    server.sendmail(email, email, msg.as_string())
    server.quit()
