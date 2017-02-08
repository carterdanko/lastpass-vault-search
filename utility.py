from __future__ import unicode_literals
import subprocess
import urllib
import json
import re
from subprocess import CalledProcessError
from distutils.version import StrictVersion

import config_properties
import os
import sys
import cache
from workflow.workflow import Workflow

ALFRED_LASTPASS_LOGIN = 'tell application "Alfred 3" to search ">{} login {}"'
LPASS_PATH = '/usr/local/bin/lpass'

class VaultSearchUtilities:
    def __init__(self, wf):
        self.wf = wf
        self.log = wf.logger

        self.set_config_defaults()


    def copy_value_to_clipboard(self, string):
        process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(string.encode('utf-8'))

    def is_logged_in(self):
        try:
            subprocess.check_output(
                [self.wf.settings['lastpass']['path'], 'ls']
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def set_config_defaults(self):
        """
        Configure some default options (unless they already exist).
        """
        self.wf.settings.setdefault('general', {})
        self.wf.settings['general'].setdefault('cache_bust', 3600)

        self.wf.settings.setdefault('lastpass', {})
        self.wf.settings['lastpass'].setdefault('path', LPASS_PATH)
        self.wf.settings['lastpass'].setdefault('username', '')

    def login_to_lastpass(self):
        """
        Uses a special Alfred search to initiate a LastPass login.
        """
        cmd = ALFRED_LASTPASS_LOGIN.format(
            self.wf.settings['lastpass']['path'],
            self.wf.settings['lastpass']['username'])

        self.log.debug('Executing Applescript: {}'.format(cmd))
        subprocess.call([
            'osascript',
            '-e',
            cmd
        ])

class VersionMismatch(Exception):
    def __init__(self, installed_lpass_version, required_min_version):
        Exception.__init__(self, "Found LastPass CLI Version {0}, Min Required Version {1}".format(
            installed_lpass_version, required_min_version))

wf = Workflow()

def parse_utility(query):
    if 'upgrade' in query:
        upgrade()
    if 'update_cache':
        update_cache()

def update_cache():
    wf._items = []
    wf.add_item(title='Updating Cache Now',
                subtitle="Please Wait for completion",
                icon='icon.png',
                valid=True)
    cache.update_caches()
    wf._items = []
    wf.add_item(title='Cache Has Been Updated',
                subtitle="Restart Query To Get Results",
                icon='icon.png',
                valid=True)
    send_feedback()


def upgrade():
    url = 'https://api.github.com/repos/carterdanko/lastpass-vault-search/releases/latest'
    current_version = float(config_properties.version)
    response = requests.get(url)
    if response.ok:
        j_data = json.loads(response.content)
        release_version = float(j_data.get('tag_name'))
        download_name = 'MyLastPass_v{}.alfredworkflow'.format(release_version)
        downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads', download_name)
        if current_version < release_version:
            urllib.urlretrieve("https://github.com/carterdanko/lastpass-vault-search/releases/download/0.5/"
                               "MyLastPass.alfredworkflow", downloads_dir)
            wf.add_item(title="New Workflow Downloaded",
                        subtitle='Find in ~/Downloads/MyLastPass.alfredworkflow',
                        icon='icon.png',
                        valid=True)
            send_feedback()
        else:
            wf.add_item(title="You are currently on the most up to date",
                        icon='icon.png',
                        valid=True)
            send_feedback()
    else:
        wf.add_item(title="API FAILURE",
                    subtitle='Github api has failed, check status',
                    icon='icon.png',
                    valid=True)
        send_feedback()
    sys.exit(0)


def precheck():
    try:
        installed_lpass_version = subprocess.check_output('/usr/local/bin/lpass --version', shell=True)
        required_min_version = config_properties.lpass
        installed_lpass_version = re.search(r'([\d.]*\d+)', installed_lpass_version)
        installed_lpass_version = installed_lpass_version.group()
        if StrictVersion(installed_lpass_version) < StrictVersion(required_min_version):
            raise VersionMismatch(installed_lpass_version, required_min_version)
    except CalledProcessError:
        wf.add_item(title='Unable to read output from lpass --version',
                        subtitle="You probably need to upgrade your last pass cli",
                        icon='icon.png',
                        valid=True)
        send_feedback()
        sys.exit(0)

    try:
        subprocess.check_output('/usr/local/bin/lpass status', shell=True)
    except CalledProcessError:
        wf.add_item(title='You are not logged into lpass-cli',
                    subtitle="Please login through the terminal to continue",
                    icon='icon.png',
                    valid=True)
        send_feedback()
        sys.exit(0)


def send_feedback():
    wf.send_feedback()