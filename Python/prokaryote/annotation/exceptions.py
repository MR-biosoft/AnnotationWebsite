class MissingChromosomeField(ValueError):
    """Custom exception to represent a parsing error."""


class InvalidFASTA(TypeError):
    """Custom exception to be thrown when encountering
    an invalid FASTA file
    """
