import os
import sys
import argparse
import yaml
import httpx


# Parse arguments
parser = argparse.ArgumentParser(description='Build functions')
parser.add_argument('-r', '--repo', default='', nargs='?', help='Repo')
parser.add_argument('-t', '--token', default='', nargs='?', help='Token')
arguments = parser.parse_args()


# Create environments folder
envs_path = '/opt/environments'
if not os.path.isdir(envs_path):
    os.mkdir(envs_path)


# Pull or clone repo
if arguments.repo and arguments.token:
    # Define repo auxiliar names
    full_repo_name = '.'.join(arguments.repo.split('https://github.com/')[1].split('.')[:-1])
    repo_name = '.'.join(arguments.repo.split('/')[-1].split('.')[:-1])

    # Clone into environments folder
    if os.path.isdir(os.path.join(envs_path, repo_name)):
        os.system('cd %s/%s && git pull origin main' % (envs_path, repo_name))
    else:
        os.system('git clone https://%s@github.com/%s %s/%s' % (arguments.token, full_repo_name, envs_path, repo_name))

    # Get configuration
    url = 'https://%s@raw.githubusercontent.com/%s/main/config.yaml' % (arguments.token, full_repo_name)
    config = yaml.load(httpx.get(url).text, Loader=yaml.Loader)

    # Install apt packages
    requirements_apt = ' '.join(config.get('requirements_apt', []))
    if requirements_apt:
        os.system('apt-get update && apt-get install --no-install-recommends -q -y %s' % (requirements_apt))

    # Install pip packages
    requirements_pip = ' '.join(config.get('requirements_pip', []))
    if requirements_pip:
        os.system('pip3 install %s' % (requirements_pip))
        
    # Install ops
    for op in config.get('ops', []):
        os.system('curl -s https://raw.githubusercontent.com/iortio/get_op/main/get_op.py | sudo python3 - -r %s -t %s' % (op, arguments.token))
    
    # Install jobs
    for job in config.get('jobs', []):
        os.system('curl -s https://raw.githubusercontent.com/iortio/get_op/main/get_job.py | sudo python3 - -r %s -t %s' % (job, arguments.token))
    
