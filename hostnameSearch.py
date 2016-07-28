from __future__ import unicode_literals
import subprocess
import re
import sys
from collections import defaultdict
from fuzzywuzzy import process
from workflow.workflow import Workflow

vaultMap = defaultdict(list)
UPDATE_INTERVAL = 3600 * 3

def gethostIds(wf):

    if len(wf.args):
        query = wf.args[0]
    else:
        query = None

    if query in ('--update', '-U'):
        wf._items = []
        wf.add_item(title='Updating Cache Now',
                    subtitle="Please Wait for completion",
                    icon='icon.png',
                    valid=True)
        updateIdCache()
        wf._items = []
        wf.add_item(title='Cache Has Been Updated',
                    subtitle="Restart Query To Get Results",
                    icon='icon.png',
                    valid=True)
        sendFeedback()
    else:
        hostnameLookup(query)

def updateIdCache():

    vaultRaw = subprocess.check_output('/usr/local/bin/lpass ls -l', shell=True)

    for row in vaultRaw.split('\n'):
        if row != '(none)':
            try:
                hostname=row.split('/')[1].split(' [id:')[0]
                hostId=row.split(' [id: ')[1].split('] ')[0]
                username=row.split(' [username: ')[1].split(']')[0]
                addToLocal(hostname, hostId, username)
            except:
                None

    wf.cache_data('hostIdList', vaultMap)

def addToLocal(hostname, hostId, username):
    vaultMap[hostname].append([hostId, username])

def hostnameLookup(hostname):
    if not wf.cached_data_fresh('hostIdList', max_age=UPDATE_INTERVAL) or wf.cached_data('hostIdList') == None:
        updateIdCache()
    localCache = wf.cached_data('hostIdList')
    results = process.extract(hostname, localCache.keys(), limit=3)
    # spits back the top five results, this will have to be relayed to the workflow and then user selected
    # once it does we have the key for the map and we can get the id.

    for host in results:
        info=localCache.get(host[0])
        hostId=info[0][0]
        username=info[0][1]
        wf.add_item(title=host[0],
                    subtitle=username + ' ' + ' \u2318-Click to copy username; ',
                    modifier_subtitles={
                        'cmd': '\u2318-Click to copy username.'
                    },
                    arg=hostId,
                    icon='icon.png',
                    valid=True)

    sendFeedback()

def sendFeedback():
    wf.send_feedback()

if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(gethostIds))
