import time
import traceback
import random
import os
from parser_manage_tools import *
import multiprocessing as mp

import subprocess
    
def crawler(page_id, tbb_dir=None, stop_trying_treshhold=12):
    print('start crawler')
    time.sleep(1*random.random())
    stop_trying = 0
    start_time = time.process_time()
    while(stop_trying < stop_trying_treshhold):
        data = download_data(page_id, tbb_dir)
        if data==0:
            break
        elif data==1:
            print('error occured on ' + str(stop_trying + 1) + ' attempt in ' + str(page_id))
            #traceback.print_exc is for bebug
            # traceback.print_exc()
            stop_trying += 1
        else: 
            print('capcha')
            print('error occured on ' + str(stop_trying + 1) + ' attempt in ' + str(page_id))
            stop_trying += 1
        if (time.process_time() - start_time>3*60):
            print('took time more than 5 mins')
            break
    print('time is ', str(time.process_time() - start_time))
    print('Ad with number: ' + str(page_id) + ' finished parsing.')
    
    ''' increment the global counter, do something with the input '''

if __name__=="__main__":
    #for automatic getting of current initial_id
    initial_id = int(subprocess.check_output(["./get_last_ad.sh"]))

    # today_date = datetime.today().strftime('%Y-%m-%d')
    num_of_cores = 1#mp.cpu_count()-2
    print('Start execution with ' + str(num_of_cores) + ' cores.')
    pool = mp.Pool(num_of_cores)
    N = 500
    tbb_dir = "/home/alex/Alex/big_data/tor-browser_en-US"
    for ad in range(N):#100000
        if ad>=N-10:
            break
        pool.apply_async(crawler, args=(initial_id + ad, tbb_dir))
    pool.close()
    pool.join()

    print('Parsing is done!!!')

