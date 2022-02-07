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


# Pull or clone repo
if arguments.repo and arguments.token:
    # Define repo auxiliar names
    full_repo_name = '.'.join(arguments.repo.split('https://github.com/')[1].split('.')[:-1])
    repo_name = '.'.join(arguments.repo.split('/')[-1].split('.')[:-1])

    # Get configuration
    url = 'https://%s@raw.githubusercontent.com/%s/main/config.yaml' % (arguments.token, full_repo_name)
    config = yaml.load(httpx.get(url).text, Loader=yaml.Loader)

    # Install packages
    if config[0].get('platform', '') == 'python':
        # Python installation
        install_path = max([elem for elem in sys.path if elem.endswith('dist-packages')], key=len)
        if os.path.isdir(os.path.join(install_path, repo_name)):
            os.system('cd %s && git pull origin main' % (os.path.join(install_path, repo_name)))
        else:
            os.system('git clone https://%s@github.com/%s %s' % (arguments.token, full_repo_name, os.path.join(install_path, repo_name)))
    elif config[0].get('platform', '') == 'make':
        # Makefile installation
        install_path = '/opt/%s' % (repo_name)
        # Get code
        if os.path.isdir(os.path.join(install_path, repo_name)):
            os.system('cd %s && git pull origin main' % (install_path))
        else:
            os.system('git clone https://%s@github.com/%s %s' % (arguments.token, full_repo_name, install_path))
        # Execute make
        os.system('cd %s && make && make install' % (install_path))
            
