import os
import subprocess
import time
import sys

DEFAULT_EXE_PATH = r'C:\ProgramData\MEGAsync\MEGAsync.exe'

def create_cache_file(path:str) -> str:
    
    # Create if doesn't exist
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write(DEFAULT_EXE_PATH)
    else:
        # Populate with default if exists but it's empty
        with open(path, 'r+') as f:
            contents = f.read()
            if contents == '':
                f.write(DEFAULT_EXE_PATH)

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

        return exe_path

def initialize_process(validated_path:str):
    os.popen(validated_path)

def terminate_process():

    subps = subprocess.Popen(['powershell', 'get-process'], stdout=subprocess.PIPE)
    output, _ = subps.communicate()

    for line in output.splitlines():
        if 'MEGAsync' in str(line):
            pid_int = int(line.split(None)[5])
            os.kill(pid_int, 9)
    
def wait_x_minutes(x_value:int):
    for x in range(x_value):
        time.sleep(60)
        print(f'{x+1} minute(s) have passed.')

if __name__ == "__main__":

    # Argument handler
    run_minutes = 5
    if len(sys.argv) > 1:
        try:
            arg_minutes = int(sys.argv[1])
            run_minutes = arg_minutes
        except:
            pass
        
    cache_path = os.path.join(os.path.dirname(__file__), 'cache.txt')
    create_cache_file(cache_path)
    valid_exe_path = extract_valid_exe_path(cache_path)
    initialize_process(valid_exe_path)
    wait_x_minutes(run_minutes)
    terminate_process()
