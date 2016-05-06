from __future__ import unicode_literals
import subprocess
import re
import sys
from collections import defaultdict
from fuzzywuzzy import process
from workflow.workflow import Workflow

# vaultMap = dict()
vaultMap = defaultdict(list)

def gethostIds(wf):

    if len(wf.args):
        query = wf.args[0]
    else:
        query = None

    vaultRaw = subprocess.check_output('/usr/local/bin/lpass ls', shell=True)

    for row in vaultRaw.split('/'):
        if row != '(none)':
            try:
                hostname=row.split(' [id: ')[0]
                hostId=re.sub('[^0-9]', '', row.split(' [id: ')[1])
                addToLocal(hostname, hostId)
            except:
                None

    hostnameLookup(query)


def addToLocal(hostname, hostId):
    vaultMap[hostname].append(hostId)

def hostnameLookup(hostname):
    results = process.extract(hostname, vaultMap.keys(), limit=5)
    # spits back the top five results, this will have to be relayed to the workflow and then user selected
    # once it does we have the key for the map and we can get the id.

    #topChoice = some user choice always going to be results[X][0] for the index in the list of tuples and then the str and not the length
    for iterHost in results:
        for hostId in vaultMap.get(iterHost[0]):
            lpShow = '/usr/local/bin/lpass show {}'.format(hostId)
            rawInfo = subprocess.check_output(lpShow, shell=True)
            username = 'NO USERNAME'
            url = ''
            if rawInfo.__contains__('Username') and rawInfo.__contains__('URL'):
                username = rawInfo.split('\n')[1].split('Username:')[1].strip()
                url = rawInfo.split('\n')[3].split('URL:')[1].strip()
            wf.add_item(title=iterHost[0],
                        subtitle=username+' '+url+' \u2318-Click to copy username; ',
                         modifier_subtitles={
                            'cmd': '\u2318-Click to copy username.'
                        },
                        arg=hostId,
                        icon='icon.png',
                        valid=True)

    wf.send_feedback()

if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(gethostIds))
