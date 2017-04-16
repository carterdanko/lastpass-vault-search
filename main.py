from __future__ import unicode_literals
from collections import defaultdict
from distutils.version import StrictVersion
import json
import os
import re
import subprocess
from subprocess import CalledProcessError
import sys
import urllib
from distutils.version import StrictVersion

import requests

from config_properties import configs
import hostnameSearch
import usernameSearch
from workflow.workflow import Workflow


vaultHostMap = defaultdict(list)
vaultUsernameMap = defaultdict(list)
wf = Workflow()


class VersionMismatch(Exception):
    def __init__(self, installed_lpass_version, required_min_version):
        Exception.__init__(self, "Found LastPass CLI Version {0}, Min Required Version {1}".format(
            installed_lpass_version, required_min_version))


def main(wf):

    precheck()

    if len(wf.args) == 1:
        query = wf.args[0]
    elif len(wf.args) > 1:
        lookup_by, query = wf.args
    else:
        query = None

    if 'upgrade' in query:
        url = 'https://api.github.com/repos/carterdanko/lastpass-vault-search/releases/latest'
        current_version = StrictVersion(configs.get('version'))
        response = requests.get(url)
        if response.ok:
            j_data = json.loads(response.content)
            release_version = StrictVersion(j_data.get('tag_name'))
            download_name = 'MyLastPass_v{}.alfredworkflow'.format(release_version)
            downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads', download_name)
            if current_version < release_version:
                urllib.urlretrieve("https://github.com/carterdanko/lastpass-vault-search/releases/download/0.5/"
                                   "MyLastPass.alfredworkflow", downloads_dir)
                wf.add_item(title="New Workflow Downloaded",
                            subtitle='Find in ~/Downloads/MyLastPass.alfredworkflow',
                            icon='icon.png',
                            valid=True)
                send_feedback()
            else:
                wf.add_item(title="You are currently on the most up to date",
                            icon='icon.png',
                            valid=True)
                send_feedback()
        else:
            wf.add_item(title="API FAILURE",
                        subtitle='Github api has failed, check status',
                        icon='icon.png',
                        valid=True)
            send_feedback()
        sys.exit(0)

    if query in ('--updateCache', '-U'):
        wf._items = []
        wf.add_item(title='Updating Cache Now',
                    subtitle="Please Wait for completion",
                    icon='icon.png',
                    valid=True)
        update_caches()
        wf._items = []
        wf.add_item(title='Cache Has Been Updated',
                    subtitle="Restart Query To Get Results",
                    icon='icon.png',
                    valid=True)
        send_feedback()
        sys.exit(0)
    else:
        if lookup_by == 'hostname':
            hostnameSearch.hostname_lookup(query)
        elif lookup_by == 'username':
            usernameSearch.username_lookup(query)


def precheck():
    try:
        installed_lpass_version = subprocess.check_output('/usr/local/bin/lpass --version', shell=True)
        required_min_version = configs.get('lpass')
        installed_lpass_version = re.search(r'([\d.]*\d+)', installed_lpass_version)
        installed_lpass_version = installed_lpass_version.group()
        if StrictVersion(installed_lpass_version) < StrictVersion(required_min_version):
            raise VersionMismatch(installed_lpass_version, required_min_version)
    except CalledProcessError:
        wf.add_item(title='Unable to read output from lpass --version',
                        subtitle="You probably need to upgrade your last pass cli",
                        icon='icon.png',
                        valid=True)
        send_feedback()
        sys.exit(0)

    try:
        subprocess.check_output('/usr/local/bin/lpass status', shell=True)
    except CalledProcessError:
        wf.add_item(title='You are not logged into lpass-cli',
                    subtitle="Press Enter to open terminal to login",
                    icon='icon.png',
                    arg="lpass-cli_login",
                    valid=True)
        send_feedback()
        sys.exit(0)


def update_caches():
    vault_raw = subprocess.check_output('/usr/local/bin/lpass ls -l', shell=True)

    for row in vault_raw.split('\n'):
        if row != '(none)':
            try:
                hostname = row.split('/')[1].split(' [id:')[0]
                host_id = row.split(' [id: ')[1].split('] ')[0]
                username = row.split(' [username: ')[1].split(']')[0]
                add_to_host_cache(hostname, host_id, username)
                add_to_username_cache(hostname, host_id, username)
            except:
                None

    wf.cache_data('hostIdList', vaultHostMap)
    wf.cache_data('usernameList', vaultUsernameMap)


def add_to_host_cache(hostname, host_id, username):
    vaultHostMap[hostname].append([host_id, username])


def add_to_username_cache(hostname, host_id, username):
    vaultUsernameMap[username].append([host_id, hostname])


def send_feedback():
    wf.send_feedback()

if __name__ == u"__main__":
    sys.exit(wf.run(main))