# -*- coding: utf-8 -*-
'''
    :synopsis: Unit Tests for Windows SNMP Module 'state.win_snmp'
    :platform: Windows
    :maturity: develop
    versionadded:: Nitrogen
'''

# Import Python Libs
from __future__ import absolute_import

# Import Salt Libs
from salt.states import win_snmp
import salt.ext.six as six

# Import Salt Testing Libs
from salttesting import TestCase, skipIf
from salttesting.helpers import ensure_in_syspath
from salttesting.mock import (
    MagicMock,
    patch,
    NO_MOCK,
    NO_MOCK_REASON,
)

ensure_in_syspath('../../')

# Globals
win_snmp.__salt__ = {}
win_snmp.__opts__ = {}


@skipIf(NO_MOCK, NO_MOCK_REASON)
class WinSnmpTestCase(TestCase):
    '''
    Test cases for salt.modules.win_snmp
    '''

    def test_agent_settings(self):
        '''
        Test - Manage the SNMP sysContact, sysLocation, and sysServices settings.
        '''
        kwargs = {'name': 'agent-settings', 'contact': 'TestContact',
                  'location': 'TestLocation', 'services': ['Internet']}
        ret = {
            'name': kwargs['name'],
            'changes': {},
            'comment': 'Agent settings already contain the provided values.',
            'result': True
        }
        # Using this instead of dictionary comprehension in order to make pylint happy.
        get_ret = dict((key, value) for (key, value) in six.iteritems(kwargs) if key != 'name')
        mock_value_get = MagicMock(return_value=get_ret)
        mock_value_set = MagicMock(return_value=True)
        with patch.dict(win_snmp.__salt__, {'win_snmp.get_agent_settings': mock_value_get,
                                            'win_snmp.set_agent_settings': mock_value_set}):
            with patch.dict(win_snmp.__opts__, {'test': False}):
                self.assertEqual(win_snmp.agent_settings(**kwargs), ret)

    def test_auth_traps_enabled(self):
        '''
        Test - Manage the sending of authentication traps.
        '''
        kwargs = {'name': 'auth-traps', 'status': True}
        ret = {
            'name': kwargs['name'],
            'changes': {
                'old': False,
                'new': True
            },
            'comment': 'Set EnableAuthenticationTraps to contain the provided value.',
            'result': True
        }
        mock_value_get = MagicMock(return_value=False)
        mock_value_set = MagicMock(return_value=True)
        with patch.dict(win_snmp.__salt__, {'win_snmp.get_auth_traps_enabled': mock_value_get,
                                            'win_snmp.set_auth_traps_enabled': mock_value_set}):
            with patch.dict(win_snmp.__opts__, {'test': False}):
                self.assertEqual(win_snmp.auth_traps_enabled(**kwargs), ret)
            with patch.dict(win_snmp.__opts__, {'test': True}):
                ret['comment'] = 'EnableAuthenticationTraps will be changed.'
                ret['result'] = None
                self.assertEqual(win_snmp.auth_traps_enabled(**kwargs), ret)

    def test_community_names(self):
        '''
        Test - Manage the SNMP accepted community names and their permissions.
        '''
        kwargs = {'name': 'community-names', 'communities': {'TestCommunity': 'Read Create'}}
        ret = {
            'name': kwargs['name'],
            'changes': {},
            'comment': 'Communities already contain the provided values.',
            'result': True
        }
        mock_value_get = MagicMock(return_value=kwargs['communities'])
        mock_value_set = MagicMock(return_value=True)
        with patch.dict(win_snmp.__salt__, {'win_snmp.get_community_names': mock_value_get,
                                            'win_snmp.set_community_names': mock_value_set}):
            with patch.dict(win_snmp.__opts__, {'test': False}):
                self.assertEqual(win_snmp.community_names(**kwargs), ret)


if __name__ == '__main__':
    from integration import run_tests  # pylint: disable=import-error
    run_tests(WinSnmpTestCase, needs_daemon=False)
