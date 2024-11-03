#!/usr/bin/env python

import os
import subprocess
import time

SERVICE_NAME = 'expressvpn'

def waitForService(keyword: str, timeout: int = 10):
    ddl = time.time() + timeout

    def check():
        result = subprocess.run([
            'systemctl', f'is-{keyword}', SERVICE_NAME, 
        ], capture_output=True, text=True, check=True)
        return keyword in result.stdout
    
    wait = 0.1
    while time.time() < ddl:
        if check():
            return
        time.sleep(wait)
        wait *= 2
    if check():
        return
    raise TimeoutError()

def main():
    if os.geteuid() != 0:
        print('Error: sudo required')
        return
    
    subprocess.run([
        'systemctl', 'restart', SERVICE_NAME, 
    ], check=True)
    waitForService('active')
    subprocess.run([
        'systemctl', 'enable', SERVICE_NAME, 
    ], check=True)
    waitForService('enabled')
    subprocess.run(['expressvpn', 'connect', 'smart'], check=True)
    try:
        while True:
            print('Press Ctrl+C to disconnect from ExpressVPN...')
            input('> ')
            print('>>>>>> Current status')
            subprocess.run(['expressvpn', 'status'])
            print('<<<<<<')
    except (KeyboardInterrupt, EOFError):
        print('bye.')
    finally:
        subprocess.run(['expressvpn', 'disconnect'], check=True)

if __name__ == '__main__':
    main()
