

def show_progress(cur_num, tot_num, intvl, msg=''):

    if cur_num and tot_num and (cur_num % intvl == 0 or cur_num >= tot_num):
        percent = round(float(cur_num) * 100.0 / float(tot_num), 2)
        print (str(percent) + "% finished. " + msg)
        return True

    return False
