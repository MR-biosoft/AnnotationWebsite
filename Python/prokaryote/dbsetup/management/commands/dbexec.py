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

    @no_translations
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(Path(options["psql_script"][0]).read_text(encoding="utf-8"))
