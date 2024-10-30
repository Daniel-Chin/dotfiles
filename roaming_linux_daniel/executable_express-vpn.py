#!/usr/bin/env python

import os
import subprocess
import time

SERVICE_NAME = 'expressvpn'

def waitForService(timeout=10):
    for _ in range(timeout):
        result = subprocess.run([
            'systemctl', 'is-active', SERVICE_NAME, 
        ], capture_output=True, text=True, check=True)
        if 'active' in result.stdout:
            return
        time.sleep(1)
    raise TimeoutError()

def main():
    if os.geteuid() != 0:
        print('Error: sudo required')
        return
    
    subprocess.run([
        'systemctl', 'restart', SERVICE_NAME, 
    ], check=True)
    waitForService()
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
