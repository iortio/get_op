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

    # Create jobs folder and links
    if not os.path.isdir('/opt/jobs'):
        os.mkdir('/opt/jobs')
    python_path = max([elem for elem in sys.path if elem.endswith('dist-packages')], key=len)
    if not os.path.islink(os.path.join(python_path, 'iort_jobs')):
        os.system('ln -s /opt/jobs %s' % (os.path.join(python_path, 'iort_jobs')))
        
    # Clone job repo
    install_path = '/opt/jobs'
    if os.path.isdir(os.path.join(install_path, job_repo_name)):
        os.system('cd %s/%s && git pull origin main' % (install_path, job_repo_name))
    else:
        os.system('git clone https://%s@github.com/%s %s/%s' % (arguments.token, job_full_repo_name, install_path, job_repo_name))
