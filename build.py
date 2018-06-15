#!/usr/bin/env python
import os
import shutil
import subprocess
import tarfile
from sys import argv
from getpass import getpass
import requests

splunk_app_name = os.path.basename(os.getcwd())


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(header):
    print('\n' + bcolors.OKBLUE + header + bcolors.ENDC + '\n')


print_header('Building {0} package...'.format(splunk_app_name))
os.mkdir(splunk_app_name)

print_header('Copying files...')

splunk_directory_skeleton = {'bin', 'default', 'metadata', 'README', 'appserver',
                             'static', 'local', 'lookups'}
dirs_present = set(os.listdir(os.getcwd()))
dirs_to_copy = splunk_directory_skeleton.intersection(dirs_present)
print(dirs_to_copy)
for directory in dirs_to_copy:
    shutil.copytree(directory, os.path.join(splunk_app_name, directory))

print_header('Installing Python dependencies...')
pip_proc = subprocess.Popen(['pip', 'install', '-r',
                             os.path.join('README', 'requirements.txt'),
                             '--target=' + os.path.join(splunk_app_name, 'bin')],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

pip_out, pip_err = pip_proc.communicate()
if pip_proc.returncode != 0:
    print(bcolors.FAIL + 'pip exited {}. Error:'.format(pip_proc.returncode) + bcolors.ENDC)
    print(pip_err)
    exit(pip_proc.returncode)

print_header('Cleaning up...')
for root, dirs, files in os.walk(os.path.join(splunk_app_name, 'bin')):
    for name in files:
        if '.pyc' in name or '.pyo' in name:
            os.remove(os.path.join(root, name))

print_header('Compressing package...')
with tarfile.open(name='{0}.tar.gz'.format(splunk_app_name), mode='w:gz') as tar:
    tar.add(splunk_app_name)

print_header('Cleaning up...')
shutil.rmtree(splunk_app_name)

print_header('Created {0}.tar.gz successfully!'.format(splunk_app_name))

if len(argv) >= 2 and argv[1] == '--install-local':
    print_header('Installing to local Splunk server...')
    tar_path = os.path.abspath('{}.tar.gz'.format(splunk_app_name))
    if len(argv) < 3:
        splunk_username = raw_input('Splunk Username:\t')
    else:
        splunk_username = argv[2]
    if len(argv) < 4:
        splunk_password = getpass('Splunk Password:\t')
    else:
        splunk_password = argv[3]
    requests.post('https://localhost:8089/services/apps/local', auth=(splunk_username, splunk_password), data={
        'name': tar_path,
        'update': 'true',
        'filename': 'true'
    }, verify=False)

    if '--restart' in argv:
        print_header('Restarting Splunkd...')
        requests.post('https://localhost:8089/services/server/control/restart', auth=(splunk_username, splunk_password),
                      verify=False)
        print_header('App will be available once Splunkd finishes restarting!')
