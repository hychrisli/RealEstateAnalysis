from random import randint
import time
import httplib, urllib
import os


def show_progress(cur_num, tot_num, intvl, msg=''):
    if cur_num and tot_num:
        if cur_num > tot_num:
            cur_num = tot_num

        if cur_num % intvl == 0 or cur_num == tot_num:
            percent = round(float(cur_num) * 100.0 / float(tot_num), 2)
            print (str(percent) + "% finished. " + msg)
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


def except_response(e):
    print(e)
    print("Exception thrown. Continue? Y/N ")

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