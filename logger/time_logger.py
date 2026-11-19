import time
from logger.colors import *

def time_log(base_fn):
    def timed_fn(*args):
        print(f"{yellow}Function: {base_fn.__name__} starting...{reset}")
        start_time = time.time()
        data = base_fn(*args)
        end_time = time.time()
        print(f"{yellow}Function: {base_fn.__name__} stopping...")
        print(f"{blue}Execution Time = {end_time - start_time} seconds.{reset}\n\n")
        return data
    return timed_fn