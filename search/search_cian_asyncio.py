import time
import traceback
import random
import os
import sys
from parser_manage_tools import *
import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from state_dict_class import MyGlobals
import subprocess
import multiprocessing as mp
from collections import Counter
    
class Crawler(object):
    """
    class for crawing cian
    :param page_id: integer, must be positive. Describes the id of the page, from which
    we should start crawling
    :param tbb_dir: string, the path to the tor-browser
    :return: None
    """
    def __init__(self, page_id, tbb_dir=None, loop=None):
        self.page_id = page_id
        self.tbb_dir = tbb_dir
        self.loop = loop
    def __call__(self):
        time.sleep(1*random.random())
        if self.page_id not in MyGlobals.state_dict.keys():
            MyGlobals.state_dict[self.page_id] = None
        loop.run_in_executor(executor, download_data, self.page_id, self.tbb_dir)
        print('Ad with number: ' + str(self.page_id) + ' finished parsing.')
if __name__=="__main__":
    #for automatic getting of current initial_id
    initial_id = int(subprocess.check_output(["./get_last_ad.sh"]))
    state_dict = {}
    N = 500
    executor = ThreadPoolExecutor(mp.cpu_count() * 2)
    loop = asyncio.get_event_loop()
    for ad in range(N):#100000
        if ad>=N-10:
            break
        crawler = Crawler(initial_id + ad, tbb_dir = "/home/alex/Alex/big_data/tor-browser_en-US", loop=loop)
        crawler()
    for _ in range(4):
        print('Counter(MyGlobals.state_dict.values())[None] is ', Counter(MyGlobals.state_dict.values())[None])
        if Counter(MyGlobals.state_dict.values())[None]>N/4:
            loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks(loop), return_exceptions=True))   

