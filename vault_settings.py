import sys
import subprocess
from workflow import Workflow

import utility
wf = Workflow()


def parse(wf):
    if len(wf.args) == 1:
        arg = wf.args[0]
    else:
        arg = None
        sys.exit(0)

    if arg == 'lastpass-login':
        log.debug('Executing command: lastpass-login')
        if util.is_logged_in():
            wf.add_item(
                'You are already logged in.',
                'The entirety of LastPass Vault Manager is open to you.',
                valid=False,
                icon='icons/warning.png')
            wf.send_feedback()
        else:
            subprocess.call([
                '/usr/bin/python',
                wf.workflowfile('execute_settings.py'),
                'login'
            ])
        sys.exit(0)




if __name__ == u"__main__":
    log = wf.logger
    util = utility.VaultSearchUtilities(wf)
    sys.exit(wf.run(parse))