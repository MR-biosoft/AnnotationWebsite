"""
"""

from pathlib import Path
import multiprocessing as mp

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError, no_translations
from django.db.utils import IntegrityError

# BioPython IO
from Bio import SeqIO

# Imports from our site
from annotation.parsing import save_protein


def _parallel_executor(protein):
    """Helper function to import proteins in parallel"""
    try:
        save_protein(protein)
    except ObjectDoesNotExist as _nil_obj:
        # print(
        #    f"protein FASTA entry with accession {protein.id} has no corresponding entry in Gene table, skipping"
        # )
        return True
    except IntegrityError as _i_e:
        _err_lines = ["Database Integrity Error:", f"{str(_i_e)}"]
        raise CommandError("\n".join(_err_lines)) from None

    return False


# TODO : add --parallel flag to switch between sequential and parallel processing
class Command(BaseCommand):
    help = "Read a FASTA file and save all proteins to the database (if their corresponding genes exist)"

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
            protein_iterator = SeqIO.parse(_file_handle, "fasta")

            # integrity check
            if not protein_iterator:
                _err_lines = [
                    "Gene files must contain at least one FASTA entry",
                    f"file {in_file}\n contains none:",
                    "Aborting.",
                ]
                raise CommandError("\n".join(_err_lines))

            print(f"Processing file {in_file}")
            with mp.Pool(mp.cpu_count()) as pool:
                _errs = pool.map(_parallel_executor, protein_iterator)

            print(f"There where {sum(_errs)} parsing errors.")
            # for protein in protein_iterator:
            #    try:
            #        save_protein(protein)
            #    except ObjectDoesNotExist as _nil_obj:
            #        print(
            #            f"protein FASTA entry with accession {protein.id} has no corresponding entry in Gene table, skipping"
            #        )
            #    except IntegrityError as _i_e:
            #        _err_lines = ["Database Integrity Error:", f"{str(_i_e)}"]
            #        raise CommandError("\n".join(_err_lines)) from None
