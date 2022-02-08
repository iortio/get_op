import os
import sys
import argparse
import yaml
import httpx


# Parse arguments
parser = argparse.ArgumentParser(description='Build Job')
parser.add_argument('-r', '--repo', default='', nargs='?', help='Job repo')
parser.add_argument('-t', '--token', default='', nargs='?', help='Token')
arguments = parser.parse_args()


# Pull or clone repo
if arguments.repo and arguments.token:
    # Define repo auxiliar names
    job_full_repo_name = '.'.join(arguments.repo.split('https://github.com/')[1].split('.')[:-1])
    job_repo_name = '.'.join(arguments.repo.split('/')[-1].split('.')[:-1])

    # Get configuration
    url = 'https://%s@raw.githubusercontent.com/%s/main/config.yaml' % (arguments.token, job_full_repo_name)
    job_config = yaml.load(httpx.get(url).text, Loader=yaml.Loader)
    
    # Clone job repo
    if not os.path.isdir('/opt/jobs'):
        os.mkdir('/opt/jobs')
    install_path = '/opt/jobs'
    if os.path.isdir(os.path.join(install_path, job_repo_name)):
        os.system('cd %s/%s && git pull origin main' % (install_path, job_repo_name))
    else:
        os.system('git clone https://%s@github.com/%s %s' % (arguments.token, job_full_repo_name, install_path))

    # Install packages
    for op_repo in job_config[0].get('ops', []):
        os.system('curl -s https://raw.githubusercontent.com/iortio/get_op/main/get_op.py | sudo python3 - -r %s -t %s' % (op_repo, arguments.token))
