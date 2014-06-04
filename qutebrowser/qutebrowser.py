# Copyright 2014 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""Early initialization and main entry pint."""


from argparse import ArgumentParser

from qutebrowser.utils.checkpyver import check_python_version
check_python_version()
import qutebrowser.utils.earlyinit as earlyinit


def _parse_args():
    """Parse command line options.

    Return:
        Argument namespace from argparse.
    """
    parser = ArgumentParser("usage: %(prog)s [options]")
    parser.add_argument('-l', '--loglevel', dest='loglevel',
                        help="Set loglevel", default='info')
    parser.add_argument('--logfilter',
                        help="Comma-separated list of things to be logged")
    parser.add_argument('-c', '--confdir', help="Set config directory (empty "
                        "for no config storage)")
    parser.add_argument('--debug', help="Turn on debugging options.",
                        action='store_true')
    parser.add_argument('--nocolor', help="Turn off colored logging.",
                        action='store_false', dest='color')
    parser.add_argument('-V', '--version', help="Show version and quit.",
                        action='store_true')
    # Note this will be checked hardcoded via sys.argv before _parse_args
    # is even run. That's also why we don't use --harfbuzz=(old|new).
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--system-harfbuzz', help="Force system harfbuzz "
                       "engine", action='store_true')
    group.add_argument('--new-harfbuzz', help="Force new harfbuzz engine",
                       action='store_true')
    group.add_argument('--old-harfbuzz', help="Force old harfbuzz engine",
                       action='store_true')
    parser.add_argument('command', nargs='*', help="Commands to execute on "
                        "startup.", metavar=':command')
    # URLs will actually be in command
    parser.add_argument('url', nargs='*', help="URLs to open on startup.")
    return parser.parse_args()


def main():
    """Main entry point for qutebrowser."""
    earlyinit.init_faulthandler()
    args = _parse_args()
    earlyinit.fix_harfbuzz()
    earlyinit.check_pyqt_core()
    earlyinit.check_pyqt_webkit()
    # We do these imports late as we need to do the early init first.
    import qutebrowser.utils.log as log
    from qutebrowser.app import Application
    log.init_log(args)
    app = Application(args)
    return app.exec_()
