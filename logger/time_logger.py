import time

def time_log(base_fn):
    def timed_fn(*args):
        print(f"\x1b[38;2;255;255;0mFunction: {base_fn.__name__} starting...\x1b[0m")
        start_time = time.time()
        data = base_fn(*args)
        end_time = time.time()
        print(f"\x1b[38;2;255;255;0mFunction: {base_fn.__name__} stopping...\n\x1b[38;2;0;64;255mExecution Time = {end_time - start_time} seconds.\x1b[0m\n\n")
        return data
    return timed_fn