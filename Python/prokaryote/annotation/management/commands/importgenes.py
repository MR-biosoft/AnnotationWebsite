"""
"""

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError, no_translations
from django.db.utils import IntegrityError

# BioPython IO
from Bio import SeqIO

# Imports from our site
from annotation.parsing import save_gene, MissingChromosomeField

class Command(BaseCommand):
    help = "Read a FASTA file and save all genes to the database"

    def add_arguments(self, parser):
        # Named arguments
        parser.add_argument(
            "FASTA_file",
            help="Path to the FASTA file to be parsed and imported to the database",
        )


    @no_translations
    def handle(self, *args, **options):
        in_file = options["FASTA_file"]
        # read file
        with open(in_file, "r", encoding="utf-8") as _file_handle:
            gene_iterator = SeqIO.parse(_file_handle, "fasta")
        
            # integrity check
            if not gene_iterator:
                _err_lines = [
                    "Gene files must contain at least one FASTA entry",
                    f"file {in_file}\n contains none:",
                    "Aborting.",
                ]
                raise CommandError("\n".join(_err_lines))

            for gene in gene_iterator:
                try:
                    save_gene(gene)
                except MissingChromosomeField as _missing_chromosome:
                    print(f"FASTA entry with accession {gene.id} has no 'chromosome' annotation, skipping.")
                except IntegrityError as _i_e:
                    _err_lines = ["Database Integrity Error:", f"{str(_i_e)}"]
                    raise CommandError("\n".join(_err_lines)) from None
