import os
import sys
import argparse
import yaml
import httpx


# Parse arguments
parser = argparse.ArgumentParser(description='Get datasource')
parser.add_argument('-r', '--repo', default='', nargs='?', help='Repo')
parser.add_argument('-t', '--token', default='', nargs='?', help='Token')
arguments = parser.parse_args()


# Create ops folders
ds_path = '/opt/datasources'
if not os.path.isdir(ds_path):
    os.mkdir(ds_path)
install_path = max([elem for elem in sys.path if elem.endswith('dist-packages')], key=len)
if not os.path.isdir(os.path.join(install_path, 'iort_datasources')):
    os.mkdir(os.path.join(install_path, 'iort_datasources'))


# Pull or clone repo
if arguments.repo and arguments.token:
    # Define repo auxiliar names
    full_repo_name = '.'.join(arguments.repo.split('https://github.com/')[1].split('.')[:-1])
    repo_name = '.'.join(arguments.repo.split('/')[-1].split('.')[:-1])

    # Clone into ops folder
    if os.path.isdir(os.path.join(ds_path, repo_name)):
        os.system('cd %s/%s && git pull origin main' % (ds_path, repo_name))
    else:
        os.system('git clone https://%s@github.com/%s %s/%s' % (arguments.token, full_repo_name, ds_path, repo_name))

    # Install datasource to be used
    if not os.path.islink(os.path.join(install_path, 'iort_datasources', repo_name)):
        os.system('ln -s %s/%s %s/iort_datasources/' % (ds_path, repo_name, install_path))
