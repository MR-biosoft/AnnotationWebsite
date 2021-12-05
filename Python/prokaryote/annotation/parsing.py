"""
    Helper module built around BioPython.SeqIO
    to load biological data into our prokaryote genome
    annotation tool.

    Parse BLAST files, extracting accessions, annotations (if any)
    and sequences.
"""

from typing import Dict
import regex
from Bio import Seq


# Imports from our module
from annotation.models import Genome
from annotation import bioregex


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


def save_genome(record: Seq.Seq, specie: str, strain: str):
    """Save a FASTA record (Bio.Seq.Seq) representing a Genome
    to the database. Specie and Strain are optional arguments
    as these might be unknown when saving a novel genome which
    has not been annotated.
    """
    parse = FASTAParser(bioregex.DEFAULT_GENOME)
    fields = parse(record)
    start_str, stop_str = fields["start_end"].split(":")
    _start, stop = int(start_str), int(stop_str)
    genome = Genome(
        chromosome=fields["chromosome"],
        specie=specie,
        strain=strain,
        sequence=str(record.seq),
        length=stop,
    )
    genome.save(force_insert=True)


def save_gene(record: Seq.Seq, only_if_chromosome_present: bool = True):
    """
    Save gene into the following tables (in order):

    """
    # parse the objects
    parse = FASTAParser(bioregex.DEFAULT_CDS)
    parsed_fields = parse(record)
    # create empty dicts for different tables
    gene_protein_fields = {}
    if "start_end" in parsed_fields:
        start_str, stop_str = parsed_fields["start_end"].split(":")
        start, stop = int(start_str), int(stop_str)
