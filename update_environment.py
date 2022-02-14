import os
import sys
import argparse
import yaml
import httpx


# Parse arguments
parser = argparse.ArgumentParser(description='Build functions')
parser.add_argument('-o', '--op', default='', nargs='?', help='Op repo')
parser.add_argument('-j', '--job', default='', nargs='?', help='Job repo')
parser.add_argument('-t', '--token', default='', nargs='?', help='Token')
arguments = parser.parse_args()


# Create environments folder
envs_path = '/opt/environments'
if not os.path.isdir(envs_path):
    os.mkdir(envs_path)

repo_path = '/opt/repos'
if not os.path.isdir(repo_path):
    os.mkdir(repo_path)

# Get name of repo
if arguments.op:
    repo = arguments.op
elif arguments.job:
    repo = arguments.job
else:
    repo = None


# Pull or clone repo
if arguments.token and repo:
    # Define repo auxiliar names
    full_repo_name = '.'.join(repo.split('https://github.com/')[1].split('.')[:-1])
    repo_name = '.'.join(repo.split('/')[-1].split('.')[:-1])

    # Clone into repos folder
    if os.path.isdir(os.path.join(repo_path, repo_name)):
        os.system('cd %s/%s && git pull origin main' % (repo_path, repo_name))
    else:
        os.system('git clone https://%s@github.com/%s %s/%s' % (arguments.token, full_repo_name, repo_path, repo_name))

    # Read configuration
    config = yaml.load(open('%s/%s/config.yaml' % (repo_path, repo_name)), Loader=yaml.Loader)

    # Iterate over environments
    for environment in config[0].get('environments', []):
        # Define repo auxiliar names
        full_env_name = '.'.join(environment.split('https://github.com/')[1].split('.')[:-1])
        env_name = '.'.join(environment.split('/')[-1].split('.')[:-1])
        # Clone environment
        if os.path.isdir(os.path.join(envs_path, env_name)):
            os.system('cd %s/%s && git pull origin main' % (envs_path, env_name))
        else:
            os.system('git clone https://%s@github.com/%s %s/%s' % (arguments.token, full_env_name, envs_path, env_name))
        # Read env configuration
        env_config = yaml.load(open('%s/%s/config.yaml' % (envs_path, env_name)), Loader=yaml.Loader)
        update_environment = False
        # Add op to config if required
        if arguments.op and arguments.op not in env_config.get('ops', []):
            if not 'ops' in env_config: env_config['ops'] = []
            env_config['ops'].append(arguments.op)
            update_environment = True
        # Add job to config if required
        if arguments.job and arguments.job not in env_config.get('jobs', []):
            if not 'jobs' in env_config: env_config['jobs'] = []
            env_config['ops'].append(arguments.job)
            update_environment = True

        if update_environment:
            # Save config
            open('%s/%s/config.yaml' % (envs_path, env_name), 'w').write(yaml.dump(config))

            # Update repo
            os.system('cd %s/%s && git add . && git commit -m "Environment updated"  && git push origin main' % (envs_path, env_name))

