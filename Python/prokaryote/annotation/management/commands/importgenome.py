"""
"""

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError, no_translations
from django.db.utils import IntegrityError

# BioPython IO
from Bio import SeqIO

# Imports from our site
from annotation.parsing import save_genome


class Command(BaseCommand):
    help = "Read a genome in FASTA format and saves it to the database"

    def add_arguments(self, parser):
        # Named arguments
        parser.add_argument(
            "FASTA_file",
            help="Path to the FASTA file to be parsed and imported to the database",
        )

        parser.add_argument(
            "--specie",
            help="(optional) name of the specie",
        )
        parser.add_argument(
            "--strain",
            help="(optional) name of the strain",
        )

    @no_translations
    def handle(self, *args, **options):
        in_file = options["FASTA_file"]
        # read file
        with open(in_file, "r", encoding="utf-8") as _file_handle:
            _fasta_entries = list(SeqIO.parse(_file_handle, "fasta"))
        # integrity check
        if len(_fasta_entries) != 1:
            _err_lines = [
                "Genome files must contain at most one FASTA entry",
                f"file {in_file} \ncontains {len(_fasta_entries)}",
                "Aborting.",
            ]
            raise CommandError("\n".join(_err_lines))
        # parse optional specie and strain
        _call_kw = {}
        _expected_kw = ["specie", "strain"]
        for option in options:
            if option in _expected_kw:
                _call_kw.update({option: options[option]})
        # print(f"save_genome({_fasta_entries[0]}, {_call_kw})")
        try:
            save_genome(*_fasta_entries, **_call_kw)
        except IntegrityError as _i_e:
            _err_lines = ["Database Integrity Error:", f"{str(_i_e)}"]
            raise CommandError("\n".join(_err_lines)) from None
