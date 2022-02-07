import os
import argparse


# Parse arguments
parser = argparse.ArgumentParser(description='Build functions')
parser.add_argument('-r', '--repo', default='', nargs='?', help='Repo')
parser.add_argument('-t', '--token', default='', nargs='?', help='Token')
parser.add_argument('-p', '--path', default='.', nargs='?', help='Path to store op')
arguments = parser.parse_args()


# Create path
if arguments.path and arguments.repo and arguments.token:
    # Get code
    os.system('git clone https://%s@github.com/%s %s' % (arguments.token, arguments.repo, os.path.join(arguments.path, '.'.join(arguments.repo.split('/')[-1].split('.')[:-1]))))
