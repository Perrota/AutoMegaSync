import argparse
import logging
import subprocess
import time
from pathlib import Path

import psutil

logger = logging.getLogger(__name__)

DEFAULT_EXE_PATH = r'C:\ProgramData\MEGAsync\MEGAsync.exe'

def ensure_cache_file_existence(path:Path) -> None:
    if not path.exists():
        logger.info("Cache not found. Creating new.")
        with path.open(mode='w+', encoding='utf-8') as f:
            f.write(DEFAULT_EXE_PATH)
            logger.info(f"Cache created on {path}.")

def extract_valid_exe_path(cache_file_path:Path) -> str:
    with cache_file_path.open('r', encoding='utf-8') as f:
        f_lines = f.readlines()

        if f_lines:
            exe_path = f_lines[0].strip()
        else:
            exe_path = DEFAULT_EXE_PATH

        # Validate cached exe path
        while not Path(exe_path).exists() or not Path(exe_path).name.endswith('.exe'):
            exe_path = input("The specified file does not exist or is invalid. Try again or press q to exit: ")
            if exe_path == 'q':
                quit()
        with cache_file_path.open('w', encoding='utf-8') as f:
            f.write(exe_path)

        logger.info("Valid path provided.")
        return exe_path

def initialize_process(validated_path:str) -> int:
    logger.info("Initializing process...")
    proc = subprocess.Popen([validated_path])
    return proc.pid

def terminate_process(pid: int) -> None:

    logger.info('Terminating process...')
    try:
        psutil.Process(pid).kill()
        logger.info('Process ended.')
    except psutil.NoSuchProcess:
        logger.error(f'Process with PID {pid} does not exist or has already been terminated.')
    except RuntimeError as e:
        logger.error(f'An error occurred while terminating the process: {e}')

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

def optional_skip():
    response = input("Do you want to run MegaSync backups? (Y/N): ")
    if response.upper() == 'Y':
        return
    else:
        quit()

if __name__ == "__main__":

    # Argument handler - minutes, verbose output, prompt parameters
    parser = argparse.ArgumentParser(description="This file runs MegaSync and turns it off automatically.")
    parser.add_argument('minutes', nargs='?', default=5, type=int, help='The amount of minutes the app will run.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Activates extra output from the console.')
    parser.add_argument('-a', '--arguments', action='store_true', help='Will take you through the wizard.')

    args = parser.parse_args()

    run_minutes = args.minutes
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.arguments:
        optional_skip()
        run_minutes = prompt_for_minutes()

    # Main code process
    cache_path = Path(__file__).parent / 'cache.txt'
    ensure_cache_file_existence(cache_path)
    valid_exe_path = extract_valid_exe_path(cache_path)
    pid = initialize_process(valid_exe_path)
    wait_x_minutes(run_minutes)
    terminate_process(pid)
