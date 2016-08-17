from __future__ import unicode_literals
import subprocess
import re
import sys
import hostnameSearch
import usernameSearch
import os
from collections import defaultdict
import config_properties
import urllib
import requests
import json
import sys
from workflow.workflow import Workflow

vaultHostMap = defaultdict(list)
vaultUsernameMap = defaultdict(list)
UPDATE_INTERVAL = 3600 * 3
wf = Workflow()

def main(wf):

    precheck()


    if len(wf.args) == 1:
        query = wf.args[0]
    elif len(wf.args) > 1:
        lookupBy = wf.args[0]
        query = wf.args[1]
    else:
        query = None

    if query in ('upgrade'):
        url = 'https://api.github.com/repos/carterdanko/lastpass-vault-search/releases/latest'
        currentVersion = float(config_properties.version)
        response = requests.get(url)
        if response.ok:
            jData = json.loads(response.content)
            releaseVersion = float(jData.get('tag_name'))
            downloadName= 'MyLastPass_v%s.alfredworkflow' % releaseVersion
            downloadsDir = os.path.join(os.path.expanduser('~'), 'Downloads',downloadName)
            if currentVersion < releaseVersion:
                urllib.urlretrieve("https://github.com/carterdanko/lastpass-vault-search/releases/download/0.5/MyLastPass.alfredworkflow", downloadsDir)
                wf.add_item(title="New Workflow Downloaded",
                            subtitle='Find in ~/Downloads/MyLastPass.alfredworkflow',
                            icon='icon.png',
                            valid=True)
                sendFeedback()
            else:
                wf.add_item(title="You are currently on the most up to date",
                            icon='icon.png',
                            valid=True)
                sendFeedback()
        else:
            wf.add_item(title="API FAILURE",
                        subtitle='Github api has failed, check status',
                        icon='icon.png',
                        valid=True)
            sendFeedback()
        sys.exit(0)

    if query in ('--updateCache', '-U'):
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
        sys.exit(0)
    else:
        if lookupBy=='hostname':
            hostnameSearch.hostnameLookup(query)
        elif lookupBy=='username':
            usernameSearch.usernameLookup(query)


def precheck():
    try:
        subprocess.check_output('/usr/local/bin/lpass status', shell=True)
    except:
        wf.add_item(title='You are not logged into lpass-cli',
                    subtitle="Please login through the terminal to continue",
                    icon='icon.png',
                    valid=True)
        sendFeedback()
        sys.exit(0)

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