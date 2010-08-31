# Copyright (C) 2007-2010 Samuel Abels.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""
The default driver that is used when the OS is not recognized.
"""
import re, string
from driver import Driver

_flags          = re.I
_printable      = re.escape(string.printable)
_unprintable    = r'[^' + _printable + r']'
_unprintable_re = re.compile(_unprintable)
_ignore         = r'[\x1b\x07\x00]'
_nl             = r'[\r\n]'
_prompt_start   = _nl + r'(?:' + _unprintable + r'*|' + _ignore + '*)'
_prompt_chars   = r'[\-\w\(\)@:~]'
_filename       = r'(?:[\w\+\-\._]+)'
_path           = r'(?:(?:' + _filename + r')?(?:/' + _filename + r')*/?)'
_any_path       = r'(?:' + _path + r'|~' + _path + r'?)'
_host           = r'(?:[\w+\-\.]+)'
_user           = r'(?:[\w+\-]+)'
_user_host      = r'(?:(?:' + _user + r'\@)?' + _host + r')'
prompt_re       = re.compile(_prompt_start                 \
                           + r'[\[\<]?'                    \
                           + r'\w+'                        \
                           + _user_host + r'?'             \
                           + r':?'                         \
                           + _any_path + r'?'              \
                           + r'[: ]?'                      \
                           + _any_path + r'?'              \
                           + r'(?:\(' + _filename + '\))?' \
                           + r'[\]\-]?'                    \
                           + r'[#>%\$\]] ?'                \
                           + _unprintable + r'*'           \
                           + r'\Z', _flags)

_user_re    = re.compile(r'(user ?name|user|login): *$', _flags)
_pass_re    = re.compile(r'password:? *$',               _flags)
_skey_re    = re.compile(r'(?:s\/key|otp-md4) (\d+) (\S+)')
_errors     = [r'error',
               r'invalid',
               r'incomplete',
               r'unrecognized',
               r'unknown command',
               r'connection timed out',
               r'[^\r\n]+ not found']
_error_re   = re.compile(r'^%?\s*(?:' + '|'.join(_errors) + r')', _flags)
_login_fail = [r'bad secrets',
               r'denied',
               r'invalid',
               r'too short',
               r'incorrect',
               r'connection timed out',
               r'failed']
_login_fail_re = re.compile(_nl          \
                          + r'[^\r\n]*'  \
                          + r'(?:' + '|'.join(_login_fail) + r')', _flags)

class GenericDriver(Driver):
    def __init__(self):
        Driver.__init__(self, 'generic')
        self.prompt = prompt_re
