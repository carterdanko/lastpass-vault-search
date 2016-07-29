from __future__ import unicode_literals
import subprocess
import re
import sys
import hostnameSearch
import usernameSearch
from collections import defaultdict
from fuzzywuzzy import process
from workflow.workflow import Workflow

vaultHostMap = defaultdict(list)
vaultUsernameMap = defaultdict(list)
UPDATE_INTERVAL = 3600 * 3
wf = Workflow()

def main(wf):

    if len(wf.args):
        lookupBy = wf.args[0]
        query = wf.args[1]
    else:
        query = None

    if query in ('--update', '-U'):
        wf._items = []
        wf.add_item(title='Updating Cache Now',
                    subtitle="Please Wait for completion",
                    icon='icon.png',
                    valid=True)
        updateCaches()
        wf._items = []
        wf.add_item(title='Cache Has Been Updated',
                    subtitle="Restart Query To Get Results",
                    icon='icon.png',
                    valid=True)
        sendFeedback()
    else:
        if lookupBy=='hostname':
            hostnameSearch.hostnameLookup(query)
        elif lookupBy=='username':
            usernameSearch.usernameLookup(query)


def updateCaches():
    vaultRaw = subprocess.check_output('/usr/local/bin/lpass ls -l', shell=True)

    for row in vaultRaw.split('\n'):
        if row != '(none)':
            try:
                hostname = row.split('/')[1].split(' [id:')[0]
                hostId = row.split(' [id: ')[1].split('] ')[0]
                username = row.split(' [username: ')[1].split(']')[0]
                addToHostCache(hostname, hostId, username)
                addToUsernameCache(hostname, hostId, username)
            except:
                None

    wf.cache_data('hostIdList', vaultHostMap)
    wf.cache_data('usernameList', vaultUsernameMap)


def addToHostCache(hostname, hostId, username):
    vaultHostMap[hostname].append([hostId,username])

def addToUsernameCache(hostname, hostId, username):
    vaultUsernameMap[username].append([hostId, hostname])

def sendFeedback():
    wf.send_feedback()

if __name__ == u"__main__":
    sys.exit(wf.run(main))