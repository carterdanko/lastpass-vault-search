import subprocess
import sys
from workflow import Workflow

def getPassword(wf):
    if len(wf.args):
        vaultId = wf.args[0]
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

    process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(processedInfo.get('Password').encode('utf-8').strip())

if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(getPassword))
