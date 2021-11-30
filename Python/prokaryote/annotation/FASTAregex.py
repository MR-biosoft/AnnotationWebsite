"""
    Module providing implementations of regular expressions
    used to parse FASTA annotations.
"""


DEFAULT_CDS = {
    "chromosome": r"(?P<chromosome>(?<=chromosome:)[\d|\D]*(?=:Chromosome))",
}
