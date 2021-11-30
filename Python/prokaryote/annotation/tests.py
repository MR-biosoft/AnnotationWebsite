from pathlib import Path

from django.test import TestCase

# BioPython Utils
from Bio import SeqIO, Seq

# Imports from our module
from annotation.FASTAparser import FASTAParser
from annotation.FASTAregex import DEFAULT_CDS
from annotation.devutils import get_env_value


class FASTAparserTest(TestCase):
    """Class defined to verify the robustness and
    integrity of the implemented FASTA parser."""

    @classmethod
    def setUpTestData(cls):
        """Setup all data"""
        cls._data_dir = Path(get_env_value("GITHUB_WORKSPACE")).joinpath("Data")
        cls._cds_files = list(cls._data_dir.glob("*cds.fa"))
        cls._protein_files = list(cls._data_dir.glob("*pep.fa"))
        _genomes = list(cls._data_dir.glob("*.fa"))
        for i in cls._cds_files + cls._protein_files:
            _genomes.remove(i)
        cls._genome_files = _genomes
        cls.gene = next(SeqIO.parse(cls._cds_files[0], "fasta"))
        cls.prot = next(SeqIO.parse(cls._protein_files[0], "fasta"))
        cls.genome = next(SeqIO.parse(cls._genome_files[0], "fasta"))

    def test_gene_parsing(self):
        gene_parser = FASTAParser(DEFAULT_CDS)
        parsed_dict = gene_parser(self.gene)
        self.assertIsInstance(parsed_dict, None)
