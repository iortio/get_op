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
    for op in job_config[0].get('ops', []):
        full_repo_name = '.'.join(op.split('https://github.com/')[1].split('.')[:-1])
        repo_name = '.'.join(op.split('/')[-1].split('.')[:-1])

        # Get configuration
        url = 'https://%s@raw.githubusercontent.com/%s/main/config.yaml' % (arguments.token, full_repo_name)
        config = yaml.load(httpx.get(url).text, Loader=yaml.Loader)

        if config[0].get('ops', []) == 'python':
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
            os.system('cd %s && make && make install && make clean' % (install_path))
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
            # Makefile installation
            install_path = '/opt/endpoints/%s' % (repo_name)
            # Get code
            if os.path.isdir(os.path.join(install_path, repo_name)):
                os.system('cd %s && git pull origin main' % (install_path))
            else:
                os.system('git clone https://%s@github.com/%s %s' % (arguments.token, full_repo_name, install_path))
