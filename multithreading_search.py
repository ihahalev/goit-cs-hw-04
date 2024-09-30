from threading import Thread, Lock
import time
from collections import defaultdict
from typing import Callable
from find_keywords import find_keywords
from print_results import print_results

def worker(callback:Callable, *args):
    """worker that will call provided function

    Args:
        callback (Callable): function to call
    """
    callback(args[0], args[1], args[2], thread_lock=args[3])

def start_threds(files:list[str], keywords:list[str], num_threads:int):
    """starts threads that will process search function

    Args:
        files list[str): list of pathes to files
        keywords (list[str): list of keyword to be searched
        num_threads (int): number of threads to start
    """
    start_time = time.time()
    
    chunk_size = len(files) // num_threads
    threads = []
    result_dict = defaultdict(list)
    lock = Lock()

    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i != num_threads - 1 else len(files)
        thread_files = files[start_index:end_index]
        thread = Thread(target=worker, args=(find_keywords, thread_files, keywords, result_dict, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    time_multithreading = time.time() - start_time
    
    print_results(time_multithreading, result_dict, "Time Multithreading: ")
