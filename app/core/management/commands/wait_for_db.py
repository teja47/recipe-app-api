"""
Django command to wait for the db(postgresql) to be avaiable

"""
import time
from psycopg2 import OperationalError as Psycop2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command to wait for db"""

    def handle(self,*args, **optional):
        """Entrypoint for command."""
        self.stdout.write('waiting for the db...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycop2OpError, OperationalError):
                self.stdout.write('db unavailable, waiting...')
                time.sleep(10)

        self.stdout.write(self.style.SUCCESS('db available now...'))