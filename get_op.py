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


# Create ops folder
ops_path = '/opt/ops'
if not os.path.isdir(ops_path):
    os.mkdir(ops_path)


# Pull or clone repo
if arguments.repo and arguments.token:
    # Define repo auxiliar names
    full_repo_name = '.'.join(arguments.repo.split('https://github.com/')[1].split('.')[:-1])
    repo_name = '.'.join(arguments.repo.split('/')[-1].split('.')[:-1])

    # Clone into ops folder
    if os.path.isdir(os.path.join(ops_path, repo_name)):
        os.system('cd %s/%s && git pull origin main' % (ops_path, repo_name))
    else:
        os.system('git clone https://%s@github.com/%s %s/%s' % (arguments.token, full_repo_name, ops_path, repo_name))

    # Get configuration
    url = 'https://%s@raw.githubusercontent.com/%s/main/config.yaml' % (arguments.token, full_repo_name)
    config = yaml.load(httpx.get(url).text, Loader=yaml.Loader)

    # Install packages
    if config[0].get('platform', '') == 'python':
        # Link into dist library folder
        install_path = max([elem for elem in sys.path if elem.endswith('dist-packages')], key=len)
        if not os.path.islink(os.path.join(install_path, repo_name)):
            os.system('ln -s %s/%s %s' % (ops_path, repo_name, install_path))
    elif config[0].get('platform', '') == 'make':
        # Execute make
        os.system('cd %s/%s && make && make install && make clean' % (ops_path, repo_name))
    elif config[0].get('platform', '') == 'docker':
        # Pull image
        try: os.system('docker pull ghcr.io/%s:main' % (full_repo_name))
        except: pass
        # Stop container
        try: os.system('docker stop %s' % (repo_name))
        except: pass
        # Remove container
        try: os.system('docker rm %s' % (repo_name))
        except: pass
        # Run image
        try: os.system('docker run -p 0.0.0.0:%d:5001/tcp -d --name %s ghcr.io/%s:main' % (config[0].get('port', 5001), repo_name, full_repo_name))
        except: pass
    elif config[0].get('platform', '') == 'fastapi':
        # Create endpoints directory if it does not exist
        if not os.path.isdir('/opt/endpoints'):
            os.mkdir('/opt/endpoints')
        # Link installation
        install_path = '/opt/endpoints/%s' % (repo_name)
        if not os.path.islink(os.path.join(install_path, repo_name)):
            os.system('ln -s %s/%s %s' % (ops_path, repo_name, install_path))
