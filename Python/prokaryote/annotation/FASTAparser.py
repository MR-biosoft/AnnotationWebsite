"""
    Helper module built around BioPython.SeqIO
    to load biological data into our prokaryote genome
    annotation tool.

    Parse BLAST files, extracting accessions, annotations (if any)
    and sequences.
"""

from typing import Dict
import regex
import Bio
from Bio import Seq, SeqIO  # , SeqRecord, SeqUtils

# regex.search(
#    r"(?P<my_group>(?<=chromosome:)[\d|\D]*(?=:Chromosome))", gene.description
# ).groupdict()


class FASTAParser:
    """FASTA parser to retrieve relevant fields
    from a Bio.SeqRecord.SeqRecord object (BioPython)
    once built with a dictionary mapping relevant field.

    An example of this dictionary is :
    {
        "chromosome": r"(?P<chromosome>(?<=chromosome:)[\d|\D]*(?=:Chromosome))"
    }
    """

    def __init__(self, parsing_regex_dict: Dict[str, str]):
        self._re_dict = parsing_regex_dict

    def __repr__(self):
        return f"FASTAParser({', '.join(self._re_dict.keys())})"

    def __call__(self, record: Bio.SeqRecord.SeqRecord):
        return None
