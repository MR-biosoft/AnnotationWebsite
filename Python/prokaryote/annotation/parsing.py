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

# from Bio import SeqIO  # Seq, SeqRecord, SeqUtils


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

    def __call__(self, record: Bio.SeqRecord.SeqRecord):
        hits = {}
        for _regex in self._re_dict.values():
            _match = regex.search(_regex, record.description)
            if _match:
                hits.update(_match.groupdict())
        return hits