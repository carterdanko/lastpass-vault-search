import subprocess
import sys
from workflow import Workflow


def parse_arguments(wf):
    vault_id = None
    action = None

    if wf.args:
        action, vault_id = wf.args

    if vault_id == "lpass-cli_login":
        subprocess.check_output('/usr/bin/osascript TerminalLoginLaunch', shell=True)
        sys.exit(1)

    processed_info = dict()
    lp_show = '/usr/local/bin/lpass show {}'.format(vault_id)
    raw_info = subprocess.check_output(lp_show, shell=True)
    for row in raw_info.split('\n'):
        try:
            if "Username:" in row:
                processed_info["Username"] = row.split("Username:")[1].strip()
            elif "Password" in row:
                processed_info["Password"] = row.split("Password:")[1].strip()
        except:
            None

    if action == 'getPassword':
        process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(processed_info.get('Password').encode('utf-8').strip())
    elif action == 'getUsername':
        process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(processed_info.get('Username').encode('utf-8').strip())


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(parse_arguments))
