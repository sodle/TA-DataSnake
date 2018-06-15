#!/usr/bin/env python
import os
import shutil
import subprocess
import tarfile

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
