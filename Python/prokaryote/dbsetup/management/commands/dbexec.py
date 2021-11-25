"""
"""

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError, no_translations
from django.db import connection


class Command(BaseCommand):
    help = "Reads a file and executes it within the site's DB connection."

    def add_arguments(self, parser):
        # Named arguments
        parser.add_argument(
            "psql_script",
            nargs=1,
            help="Path to the PSQL script to be parsed and executed.",
        )

    ## old handle, fragile approach
    # @no_translations
    # def handle(self, *args, **options):
    #    with open(options["psql_script"][0], "r", encoding="utf-8") as f:
    #        with connection.cursor() as cursor:
    #            for line in f.readlines():
    #                _query = line.strip()
    #                if len(_query) > 0 and not _query.startswith("--"):
    #                    cursor.execute(line.strip())
    #            # for line in cursor.fetchall():
    #            #    self.stdout.write(type(line))

    @no_translations
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(Path(options["psql_script"][0]).read_text(encoding="utf-8"))
