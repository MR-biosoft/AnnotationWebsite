"""
    Module providing implementations of regular expressions
    used to parse FASTA annotations.
"""

# Regex dictionnary for information contained in cds files (individual genes)
DEFAULT_CDS = {
    "chromosome": r"(?P<chromosome>(?<=chromosome:)\w+(?=:Chromosome))",
    "start_end": r"(?P<start_end>(?<=Chromosome:)\d+:\d+)",
    "reading_frame": r"(?P<reading_frame>(?<=:)\-?1(?=\s))",
    "gene_name": r"(?P<gene_name>(?<=gene:)[\d|\D]*(?=\s+gene_biotype))",
    "gene_biotype": r"(?P<gene_biotype>(?<=gene\_biotype:)\w+)",
    "transcript_biotype": r"(?P<transcript_biotype>(?<=transcript\_biotype:)\w+)",
    "gene_symbol": r"(?P<gene_symbol>(?<=gene\_symbol:)\w+(?=\sdescription))",
    "function": r"(?P<function>(?<=description:).+)",
}

DEFAULT_PROTEIN = {
    "chromosome": r"(?P<chromosome>(?<=chromosome:)[\d|\D]*(?=:Chromosome))",
    "start_end": r"(?P<start_end>(?<=Chromosome:)\d+:\d+(?=:[1|\-1]))",
    "gene_name": r"(?P<gene_name>(?<=gene:)[\d|\D]*(?=\s+gene_biotype))",
    "gene_biotype": r"(?P<gene_biotype>(?<=gene\_biotype:)\w+)",
    "transcript_biotype": r"(?P<transcript_biotype>(?<=transcript\_biotype:)\w+)",
    "gene_symbol": r"(?P<gene_symbol>(?<=gene\_symbol:)\w+)",
    "function": r"(?P<function>(?<=description:).+)",
}

DEFAULT_GENOME = {
    "chromosome": r"(?P<chromosome>(?<=chromosome:)[\d|\D]*(?=:Chromosome))",
    "start_end": r"(?P<start_end>(?<=Chromosome:)\d+:\d+(?=:[1|\-1]))",
}
