import requests
import os
import sys
import time
import asyncio
import multiprocessing as mp
from subprocess import Popen, PIPE, STDOUT
from termcolor import colored
from pyfiglet import Figlet

path = '/home/ali/Desktop/bagher.conf'
ovpns = []
dc_time = None
# def connect_ovpn(i: int):
async def connect_ovpn(i: int):
    global ovpns

    ovpn = Popen(['openvpn', '--auth-nocache', '--config', path], stdout=PIPE, stderr=STDOUT)
    """
    ['__class__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', 
    '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', 
    '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', 
    '__str__', '__subclasshook__', '__weakref__', '_check_timeout', '_child_created', '_close_pipe_fds', 
    '_closed_child_pipe_fds', '_communicate', '_communication_started', '_execute_child', '_get_devnull', '_get_handles', 
    '_handle_exitstatus', '_input', '_internal_poll', '_posix_spawn', '_remaining_time', '_save_input', 
    '_sigint_wait_secs', '_stdin_write', '_translate_newlines', '_try_wait', '_wait', '_waitpid_lock', 'args', 
    'communicate', 'encoding', 'errors', 'kill', 'pid', 'poll', 'returncode', 'send_signal', 'stderr', 'stdin', 
    'stdout', 'terminate', 'text_mode', 'universal_newlines', 'wait']
    """
    print(f'OVPN {i} Connect Successfully')
    ovpns.append(ovpn)


async def main(number: int):
    global dc_time
    # try:
    #     n = int(sys.argv[1])
    # except ValueError:
    #     print(f'"{sys.argv[1]}" is not a valid number')
    #     return
    # except IndexError:
    #     print('please enter a number of ovpn you want to connect')
    #     return

    print('\n* ----------- Connecting ----------- * \n')
    for c in list(map(connect_ovpn, [i+1 for i in range(number)])):
        await c
    while True:
        if dc_time is not None:
            time.sleep(dc_time)
            raise KeyboardInterrupt
        else:
            time.sleep(100)

def init() -> number:
    global dc_time
    f = Figlet(font='standard')
    print(colored(f.renderText('OVPN Spammer'), 'green'))
    print(colored('Created by github.com/AliRn76\n', 'blue'))

    valid_number = False
    while not valid_number:
        try:
            number = int(input(colored('How many connection do you want ?', 'yellow')))
            valid_number = True
        except ValueError:
            pass

    dc = None
    while dc not in ['n', 'N', 'y', 'Y']:
        dc = input(colored('Do you want connections disconnect automatically ? (y/n) ', 'yellow'))

    if dc in ['y', 'Y']:
        valid_t = False
        while not valid_t:
            try:
                dc_time = int(input(colored('Disconnect after how many seconds ? ', 'yellow')))
                valid_t = True
            except ValueError:
                pass
    return number


try:
    n = init()
    asyncio.run(main(n))
except KeyboardInterrupt:
    print('\n* --------- Disconnecting ---------- * \n')
    for i, o in enumerate(ovpns):
        o.kill()
        print(f'OVPN {i+1} Killed Successfully')
    print('\n* -------------- Done -------------- * \n')
