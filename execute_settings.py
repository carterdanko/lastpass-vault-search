from __future__ import unicode_literals
from workflow import Workflow
import utility
import sys

def main(wf):
    arg = wf.args[0]

    if arg == 'login':
        log.debug('Executing command: login')
        util.login_to_lastpass()
        # util.print_utf8('Hit ENTER to login to LastPass.')
        sys.exit(0)



if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger

    util = utility.VaultSearchUtilities(wf)
    sys.exit(wf.run(main))