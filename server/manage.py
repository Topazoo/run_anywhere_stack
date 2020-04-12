#!/usr/bin/env python3.7
''' Utilities for managing the application '''

import argparse, subprocess, os

class Interface:

    def add_command_line_args(self):
        [self.parser.add_argument(cla, action=self.UTILITIES[cla]['action'], default=self.UTILITIES[cla]['default']) for cla in self.UTILITIES]


    def __init__(self):
        self.UTILITIES = {
            '--run-server': {
                'action': 'store_true',
                'default': False,
                'logic': self.run
            },
            '--run': {
                'action': 'store_true',
                'default': False,
                'logic': self.run
            },
            '--status': {
                'action': 'store_true',
                'default': False,
                'logic': self.status
            },
            '--build': {
                'action': 'store_true',
                'default': False,
                'logic': self.build
            },
            '--kill': {
                'action': 'store_true',
                'default': False,
                'logic': self.kill
            },
            '--force_kill': {
                'action': 'store_true',
                'default': False,
                'logic': self.force_kill
            },
        }
        self.parser = argparse.ArgumentParser(description='Utilities for managing the server')
        self.add_command_line_args()


    def build(self):
        ''' Build the application [./manage.py --build] '''

        os.system('docker-compose build --no-cache')


    def run(self):
        ''' Run the application [./manage.py --run] '''

        try:
            os.system('docker-compose up --force-recreate')

        except Exception:
            print('Failed to start application - Is the server already running?')


    def connect(self):
        ''' Connect to a running application '''

        # TODO - Possible?


    def kill(self):
        ''' Kill a running application [./manage.py --kill] '''

        subprocess.check_output('docker-compose down'.split())


    def force_kill(self):
        ''' Force kill a running application [./manage.py --kill] '''

        for container in self._get_running_containers():
            subprocess.check_output(('docker kill ' + container[0]).split())
            print('Killed ' + container[0])


    def status(self):
        ''' View running applications'''

        for container in self._get_running_containers():
            print(f'Running application: [{container[0]}] ({container[1]})')


    def parse_args(self):
        ''' Adapter '''

        for arg,val in vars(self.parser.parse_args()).items():
            if val: self.UTILITIES["--"+arg]['logic']()


    def _get_running_containers(self) -> list:
        ''' Get running containers '''

        containers = subprocess.check_output('docker ps'.split()).decode().split('\n')
        containers.remove('')

        if len(containers) > 1: return [(container.split()[0], container.split()[1]) for container in containers[1:]]

        else: print('No running applications')
        
        return []


if __name__ == '__main__':
    try:
        Interface().parse_args()
    except KeyboardInterrupt:
        Interface().kill()