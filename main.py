import os
import subprocess
import time
import sys
import logging

DEFAULT_EXE_PATH = r'C:\ProgramData\MEGAsync\MEGAsync.exe'

def create_cache_file(path:str) -> str:
    
    # Create if doesn't exist
    if not os.path.exists(path):
        logger.info("Cache not found. Creating new.")
        with open(path, 'w') as f:
            f.write(DEFAULT_EXE_PATH)
            logger.info(f"Cache created on {path}.")
    else:
        # Populate with default if exists but it's empty
        with open(path, 'r+') as f:
            contents = f.read()
            if contents == '':
                logger.info("Empty cache found. Setting default.")
                f.write(DEFAULT_EXE_PATH)
            else:
                logger.info("Existing cached value found.")

def extract_valid_exe_path(cache_file_path:str) -> str:
    with open(cache_file_path, 'r') as f:
        f_lines = f.readlines()
        exe_path = f_lines[0]

        # Validate cached exe path
        while not os.path.exists(exe_path) or not os.path.basename(exe_path).endswith('.exe'):
            exe_path = input("The specified file does not exists or is invalid. Try again or press q to exit: ")
            if exe_path == 'q':
                quit()
            with open(cache_file_path, 'w') as f:
                f.write(exe_path)

        logger.info("Valid path provided.")
        return exe_path

def initialize_process(validated_path:str):
    logger.info("Initializing process...")
    os.popen(validated_path)

def terminate_process():

    logger.info('Locating process to terminate...')
    subps = subprocess.Popen(['powershell', 'get-process'], stdout=subprocess.PIPE)
    output, _ = subps.communicate()

    for line in output.splitlines():
        if 'MEGAsync' in str(line):
            pid_int = int(line.split(None)[5])
            logger.info(f'Process found at number {pid_int}.')
            logger.info('Killing it.')
            os.kill(pid_int, 9)
            logger.info('Process ended.')
    
def wait_x_minutes(x_value:int):
    logger.info("Awaiting program.")
    for x in range(x_value):
        time.sleep(60)
        logger.info(f'{x+1} minute(s) have passed.')

def prompt_for_minutes() -> int:
    minutes = ''
    while not minutes.isnumeric():
        minutes = input("Enter the number of minutes you want the program to run: ")
    return int(minutes)

def prompt_for_verbose_arg():
    response = input("Do you want the console to output data about the state of the script (Y/N): ")
    if response.upper() == 'Y':
        logging.basicConfig(level=logging.INFO)

def optional_skip():
    response = input("Do you want to run MegaSync backups? (Y/N): ")
    if response.upper() == 'N':
        quit()

if __name__ == "__main__":

    # Initialize logger
    logger = logging.getLogger(__name__)

    # Argument handler - minutes, verbose output, prompt parameters
    run_minutes = 5
    if len(sys.argv) > 1:
        try:
            arg_minutes = int(sys.argv[1])
            run_minutes = arg_minutes
        except:
            pass
        if len(sys.argv) > 2:
            if '-v' in sys.argv:
                logging.basicConfig(level=logging.INFO)
            if '-a'  in sys.argv:
                optional_skip()
                run_minutes = prompt_for_minutes()
                prompt_for_verbose_arg()
        
    cache_path = os.path.join(os.path.dirname(__file__), 'cache.txt')
    create_cache_file(cache_path)
    valid_exe_path = extract_valid_exe_path(cache_path)
    initialize_process(valid_exe_path)
    wait_x_minutes(run_minutes)
    terminate_process()
