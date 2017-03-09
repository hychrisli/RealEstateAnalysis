from random import randint
import time


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
