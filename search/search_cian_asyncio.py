import time
import traceback
import random
import os
from parser_manage_tools import *
import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from state_dict_class import MyGlobals
import subprocess
import multiprocessing as mp
from collections import Counter
    
def crawler(page_id, tbb_dir=None, stop_trying_treshhold=12, loop=None):
    print('start crawler')
    time.sleep(1*random.random())
    if page_id not in MyGlobals.state_dict.keys():
        MyGlobals.state_dict[page_id] = None
    # download_data(page_id, tbb_dir)
    loop.run_in_executor(executor, download_data, page_id, tbb_dir)
    print('Ad with number: ' + str(page_id) + ' finished parsing.')
    
    ''' increment the global counter, do something with the input '''
if __name__=="__main__":
    #for automatic getting of current initial_id
    initial_id = int(subprocess.check_output(["./get_last_ad.sh"]))
    state_dict = {}
    N = 500
    executor = ThreadPoolExecutor(mp.cpu_count() * 2)
    tbb_dir = "/home/alex/Alex/big_data/tor-browser_en-US"
    loop = asyncio.get_event_loop()
    for ad in range(N):#100000
        if ad>=N-10:
            break
        crawler(initial_id + ad, tbb_dir, loop=loop)
    for _ in range(4):
        print('Counter(MyGlobals.state_dict.values())[None] is ', Counter(MyGlobals.state_dict.values())[None])
        if Counter(MyGlobals.state_dict.values())[None]>N/4:
            loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks(loop), return_exceptions=True))   
    # print('Parsing is done!!!')

