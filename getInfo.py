import subprocess
import sys
from workflow import Workflow

def parseArguments(wf):
    if len(wf.args):
        action = wf.args[0]
        vaultId = wf.args[1]
    else:
        vaultId = None

    processedInfo = dict()
    lpShow = '/usr/local/bin/lpass show {}'.format(vaultId)
    rawInfo = subprocess.check_output(lpShow, shell=True)
    for row in rawInfo.split('\n'):
        try:
            if row.split(":")[0] == 'Username' or row.split(":")[0] == 'Password':
                processedInfo[row.split(":")[0]] = row.split(":")[1]
        except:
            None

    if action == 'getPassword':
        process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(processedInfo.get('Password').encode('utf-8').strip())
    elif action == 'getUsername':
        process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(processedInfo.get('Username').encode('utf-8').strip())

if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(parseArguments))
