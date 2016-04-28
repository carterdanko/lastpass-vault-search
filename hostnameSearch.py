import subprocess
import re
import sys
from fuzzywuzzy import process
from workflow.workflow import Workflow

vaultMap = dict()

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
    if hostname not in vaultMap:
        vaultMap[hostname] = hostId

def hostnameLookup(hostname):
    results = process.extract(hostname, vaultMap.keys(), limit=5)
    # spits back the top five results, this will have to be relayed to the workflow and then user selected
    # once it does we have the key for the map and we can get the id.

    #topChoice = some user choice always going to be results[X][0] for the index in the list of tuples and then the str and not the length
    for iterHost in results:
        wf.add_item(title=iterHost[0],
                    arg=vaultMap.get(iterHost[0]),
                    valid=True)

    wf.send_feedback()

if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(gethostIds))
