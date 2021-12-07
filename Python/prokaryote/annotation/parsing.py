"""
    Helper module built around BioPython.SeqIO
    to load biological data into our prokaryote genome
    annotation tool.

    Parse BLAST files, extracting accessions, annotations (if any)
    and sequences.
"""

import json
from datetime import datetime
from typing import Dict, Optional, Tuple, Callable, NoReturn
import regex
from Bio import Seq

from django.core.exceptions import ObjectDoesNotExist

# Imports from our module
from annotation.models import Genome, GeneProtein, GeneSeq, ProteinSeq, Annotation
from annotation import bioregex


class MissingChromosomeField(ValueError):
    """Custom exception to represent a parsing error."""


def _get_start_end_positions(start_end_match: str) -> Tuple[int, int]:
    """Helper function, not to be called directly."""
    start_str, stop_str = start_end_match.split(":")
    return (int(start_str), int(stop_str))


DEFAULT_CDS_HELPERS: Dict[str, Callable] = {"start_end": _get_start_end_positions}


class FASTAParser:
    """FASTA parser to retrieve relevant fields
    from a Bio.SeqRecord.SeqRecord object (BioPython)
    once built with a dictionary of regex.

    Once initialised with the regex dictionary,
    the resulting object is a callable (function)
    which can be used to retrieve fields of interest
    from the description within a Bio.Seq.description.

    The regex dictionary must contain named groups.
    A named group is :
        (?P<identifier>regex)

    For more information see : https://docs.python.org/3.8/library/re.html

    An example of this dictionary is :
    {
        "chromosome": r"(?P<chromosome>(?<=chromosome:)[\d|\D]*(?=:Chromosome))"
    }
    """

    def __init__(self, parsing_regex_dict: Dict[str, str]):
        self._re_dict = parsing_regex_dict

    def __repr__(self):
        return f"FASTAParser({', '.join(self._re_dict.keys())})"

    def __call__(self, record: Seq.Seq):
        hits = {}
        for _regex in self._re_dict.values():
            _match = regex.search(_regex, record.description)
            if _match:
                hits.update(_match.groupdict())
        return hits


def save_genome(
    record: Seq.Seq, specie: Optional[str] = None, strain: Optional[str] = None
) -> NoReturn:
    """Save a FASTA record (Bio.Seq.Seq) representing a Genome
    to the database. Specie and Strain are optional arguments
    as these might be unknown when saving a novel genome which
    has not been annotated.
    """
    parse = FASTAParser(bioregex.DEFAULT_GENOME)
    fields = parse(record)
    _start, stop = _get_start_end_positions(fields["start_end"])
    genome = Genome(
        chromosome=fields["chromosome"],
        specie=specie,
        strain=strain,
        sequence=str(record.seq),
        length=stop,
    )
    genome.save(force_insert=True)


def save_gene(record: Seq.Seq, update: bool = False):
    """
    Save gene into the following tables (in order):

    """
    # parse the FASTA record
    parse = FASTAParser(bioregex.DEFAULT_CDS)
    parsed_fields = parse(record)
    # This exception will be used to skip plasmids
    if "chromosome" not in parsed_fields:
        raise MissingChromosomeField(
            f"Missing annotation in FASTA record with id {record.id}"
        )

    # Conditionally prepare values before object instantiation
    reading_frame = (
        int(parsed_fields["reading_frame"])
        if "reading_frame" in parsed_fields
        else None
    )
    if "start_end" in parsed_fields:
        start, end = _get_start_end_positions(parsed_fields["start_end"])
    else:
        start, end = None, None

    _ptm = {"Accession": record.id}
    _ptm.update(parsed_fields)
    with open("ptm.jsonl", "a", encoding="utf-8") as f:
        f.write(f"{json.dumps(_ptm)}\n")
    # create Dicts for different tables
    ## [field.name for field in GeneProtein._meta.fields]
    try:
        chromosome = Genome.objects.only("chromosome").get(
            chromosome=parsed_fields["chromosome"]
        )
        gene_protein_fields = {
            "accession_number": record.id,
            "dna_length": len(record.seq),
            "start_position": start,
            "end_position": end,
            "reading_frame": reading_frame,
            "aa_length": None,
            "chromosome": chromosome,
            "isannotated": False,  # Temporarily set it to false
        }
        if not update:
            gene_protein = GeneProtein.objects.create(**gene_protein_fields)
    except ObjectDoesNotExist as _nil_obj:
        print(f"Error importing gene with accession {record.id}")
        print("Inspect the file `gene_importation_error_log.jsonl` for further details")
        with open(
            "gene_importation_error_log.jsonl", "a", encoding="utf-8"
        ) as err_log_file:
            _err_dump = {
                "datetimeUTC": "",
            }
            err_log_file.write(f"{json.dumps(_err_dump)}\n")

    # gene_protein.save()

    # gene_protein_fields = {}
    # if "start_end" in parsed_fields:
    #    start_str, stop_str = parsed_fields["start_end"].split(":")
    #    start, stop = int(start_str), int(stop_str)
