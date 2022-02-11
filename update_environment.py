import os
import sys
import argparse
import yaml
import httpx


# Parse arguments
parser = argparse.ArgumentParser(description='Build functions')
parser.add_argument('-e', '--environment', default='', nargs='?', help='Environment repo')
parser.add_argument('-o', '--op', default='', nargs='?', help='Op repo')
parser.add_argument('-j', '--job', default='', nargs='?', help='Job repo')
parser.add_argument('-t', '--token', default='', nargs='?', help='Token')
arguments = parser.parse_args()


# Create environments folder
envs_path = '/opt/environments'
if not os.path.isdir(envs_path):
    os.mkdir(envs_path)


# Pull or clone repo
if arguments.environment and arguments.token and (arguments.op or arguments.job):
    # Define repo auxiliar names
    full_repo_name = '.'.join(arguments.environment.split('https://github.com/')[1].split('.')[:-1])
    repo_name = '.'.join(arguments.environment.split('/')[-1].split('.')[:-1])

    # Clone into environments folder
    if os.path.isdir(os.path.join(envs_path, repo_name)):
        os.system('cd %s/%s && git pull origin main' % (envs_path, repo_name))
    else:
        os.system('git clone https://%s@github.com/%s %s/%s' % (arguments.token, full_repo_name, envs_path, repo_name))

    # Get configuration
    config = yaml.load(open('%s/%s/config.yaml' % (envs_path, repo_name)), Loader=yaml.Loader)

    update_environment = False
    # Add ops
    if arguments.op:
        if not config.get('ops', []): config['ops'] = []
        if not arguments.op in config['ops']:
            config['ops'].append(arguments.op)
            update_environment = True

    # Add jobs
    if arguments.job:
        if not config.get('jobs', []): config['jobs'] = []
        if not arguments.job in config['jobs']:
            config['jobs'].append(arguments.job)
            update_environment = True

    if update_environment:
        # Save config
        open('%s/%s/config.yaml' % (envs_path, repo_name), 'w').write(yaml.dump(config))

        # Update repo
        os.system('cd %s/%s && git add . && git commit -m "Environment updated"  && git push origin main' % (envs_path, repo_name))
