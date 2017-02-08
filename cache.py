from __future__ import unicode_literals
import subprocess
from collections import defaultdict
from workflow import Workflow

wf = Workflow()
vaultHostMap = defaultdict(list)
vaultUsernameMap = defaultdict(list)

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
