

def show_progress(cur_num, tot_num, invtl, msg):

    if cur_num and tot_num and cur_num % invtl == 0:
        percent = round(float(cur_num) * 100.0 / float(tot_num), 2)
        print (str(percent) + "% finished: " + msg)
