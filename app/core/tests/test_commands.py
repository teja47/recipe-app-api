"""
test custom django management commands

"""
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error  # this error throws by psycopg2 when db is not ready
from django.core.management import call_command
from django.db.utils import OperationalError # this error throws by django when db is not ready
from django.test import SimpleTestCase

@patch('core.management.commands.wait_for_db.Command.check') #mocking the check.
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """test waiting for db is ready"""
        patched_check.return_value  = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep') #mocking the sleep.
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """test waiting for db when getting operationalError."""
        patched_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])