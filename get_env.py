import os
import sys
import argparse
import yaml
import httpx


# Parse arguments
parser = argparse.ArgumentParser(description='Get environment')
parser.add_argument('-r', '--repo', default='', nargs='?', help='Repo')
parser.add_argument('-t', '--token', default='', nargs='?', help='Token')
arguments = parser.parse_args()


# Create ops folder
envs_path = '/opt/environments'
if not os.path.isdir(envs_path):
    os.mkdir(envs_path)


# Pull or clone repo
if arguments.repo and arguments.token:
    # Define repo auxiliar names
    full_repo_name = '.'.join(arguments.repo.split('https://github.com/')[1].split('.')[:-1])
    repo_name = '.'.join(arguments.repo.split('/')[-1].split('.')[:-1])

    # Clone into ops folder
    if os.path.isdir(os.path.join(envs_path, repo_name)):
        os.system('cd %s/%s && git pull origin main' % (envs_path, repo_name))
    else:
        os.system('git clone https://%s@github.com/%s %s/%s' % (arguments.token, full_repo_name, envs_path, repo_name))
