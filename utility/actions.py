from random import randint

import time


def show_progress(cur_num, tot_num, intvl, msg=''):
    if cur_num and tot_num:
        if cur_num > tot_num:
            cur_num = tot_num

        if cur_num % intvl == 0:
            percent = round(float(cur_num) * 100.0 / float(tot_num), 2)
            print (str(percent) + "% finished. " + msg)

        return True

    return False


def rand_wait(msg, min_wait=10, max_wait=30):
    wait_time = randint(min_wait, max_wait)
    print (str(msg) + " | Waiting " + str(wait_time) + "s ...")
    time.sleep(wait_time)
