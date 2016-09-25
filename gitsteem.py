#!/usr/bin/env python3
import sys
import json
import re
import subprocess
from time import sleep
from piston.steem import Steem

s = Steem()

if len(sys.argv) < 2:
    print('Please specify an action.')
    print('Actions:')

    print('\tclone - clones a specified project')
    print('\t\t{} clone someguy123/steem-value'.format(sys.argv[0]))
    print('\t\t(with protocol) {} clone ssh someguy123/steem-value'.format(sys.argv[0]))

    print('\tremote - adds the specified project to your projects remotes')
    print('\t\t{} remote someguy123/steem-value'.format(sys.argv[0]))
    print('\t\t(with protocol) {} remote ssh someguy123/steem-value'.format(sys.argv[0]))
    exit()

action = sys.argv[1]


#
# Converts a "someguy123/steem" project
# and returns (account,project_name) tuple
#
def split_project(data):
    project_data = data.split('/')
    if len(project_data) != 2:
        print('Invalid project')
        exit()
    project_name = project_data[1]
    account = project_data[0]
    return (account, project_name)

#
# Connects to STEEM and obtains
# a project URL via the users JSON Metadata
#
def get_project_url(account, project_name, protocol):

    account_data = s.rpc.get_accounts([account])

    if(len(account_data) < 1):
        print('Account not found')
        exit()
    account_data = account_data[0]
    try:
        j = json.loads(account_data['json_metadata'])
    except:
        print('Error parsing JSON Metadata')
        exit()
    if 'git' not in j:
        print('No git projects on this account')
        exit()

    projects = j['git']

    if type(projects) != dict:
        print('Invalid git data on account (error: not a dict)')
        exit()

    if project_name not in projects:
        print('User has git repos, but project not found')
        exit()
    pdata = projects[project_name]
    if protocol is None:
        if 'https' in pdata:
            protocol = 'https'
        else:
            protocol = list(pdata.keys())[0]
    if protocol not in pdata or 'value' not in pdata[protocol]:
        print("Error: Couldn't find a repository URL for that protocol")
        exit()
    url_validate = r'^(https?://[a-z0-9-.]+/[A-Za-z0-9-/._]+)$|^([A-Za-z0-9-]+@[A-Za-z0-9-.]+:[A-Za-z0-9-/._]+)$'
    r = re.compile(url_validate)
    url = pdata[protocol]['value']
    if len(r.findall(url)) < 1:
        print('Uh oh... this is a strange URL.')
        print("For your safety, we won't run anything for this URL.")
        print("The URL is: {}".format(url))
        exit()
    return url

def clone():
    if len(sys.argv) > 3:
        protocol = sys.argv[2]
        project = sys.argv[3]
    elif len(sys.argv) > 2:
        project = sys.argv[2]
        protocol = None
    else:
        print('Usage: {} clone username/projectname'.format(sys.argv[0]))
        exit()
    account, project_name = split_project(project)
    project_url = get_project_url(account, project_name, protocol)
    print("Cloning:", project_url)
    out = subprocess.Popen(["git","clone",project_url], stdout=subprocess.PIPE)
    # on some systems git likes to fork into the background
    # so wait a tiny bit...
    sleep(2)
    # print(out)
    return

def remote():
    remotename = "gitsteem"
    if len(sys.argv) > 4:
        remotename = sys.argv[4]
        protocol = sys.argv[2]
        project = sys.argv[3]
    elif len(sys.argv) > 3:
        protocol = sys.argv[2]
        project = sys.argv[3]
    elif len(sys.argv) > 2:
        project = sys.argv[2]
        protocol = None
    else:
        print('Usage: {} remote [protocol] username/projectname {remotename}'.format(sys.argv[0]))
        exit()
    account, project_name = split_project(project)
    project_url = get_project_url(account, project_name, protocol)
    print("Adding remote as {}: {}".format(remotename,project_url))
    out = subprocess.Popen(["git","remote","add",remotename,project_url], stdout=subprocess.PIPE)
    # on some systems git likes to fork into the background
    # so wait a tiny bit...
    sleep(2)

actions = {
    'clone': clone,
    'remote': remote
}

if action not in actions:
    print('Invalid action. Try {} clone user/project'.format(sys.argv[0]))

actions[action]()

