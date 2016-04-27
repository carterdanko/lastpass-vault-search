import subprocess
import re
from fuzzywuzzy import process


vaultMap = dict()

def vaultLocalRefresh():

    vaultRaw = subprocess.check_output('/usr/local/bin/lpass ls', shell=True)

    for row in vaultRaw.split('/'):
        if row != '(none)':
            try:
                hostname=row.split(' [id: ')[0]
                hostId=re.sub('[^0-9]', '', row.split(' [id: ')[1])
                addToLocal(hostname, hostId)
            except:
                None


def addToLocal(hostname, hostId):
    if hostname not in vaultMap:
        vaultMap[hostname] = hostId

def hostnameLookup(hostname):
    results = process.extract(hostname, vaultMap.keys(), limit=5)
    # spits back the top five results, this will have to be relayed to the workflow and then user selected
    # once it does we have the key for the map and we can get the id.

    #topChoice = some user choice always going to be results[X][0] for the index in the list of tuples and then the str and not the length
    selection = results[0][0]
    hostId = vaultMap.get(selection)
    getPassword(hostId)


def getPassword(hostId):
    processedInfo = dict()
    lpShow = '/usr/local/bin/lpass show {}'.format(hostId)
    rawInfo = subprocess.check_output(lpShow, shell=True)
    for row in rawInfo.split('\n'):
        try:
            if row.split(":")[0] == 'Username' or row.split(":")[0] == 'Password':
                processedInfo[row.split(":")[0]] = row.split(":")[1]
        except:
            None
    print 'hello'


if __name__ == '__main__':
    vaultLocalRefresh()
    hostnameLookup('google')