from pathlib import Path

from django.test import TestCase

# BioPython Utils
from Bio import SeqIO

# Imports from our module
from annotation.parsing import FASTAParser
from annotation.bioregex import DEFAULT_CDS, DEFAULT_PROTEIN, DEFAULT_GENOME
from annotation.devutils import get_env_value


class FASTAparserTest(TestCase):
    """Class defined to verify the robustness and
    integrity of the implemented FASTA parser."""

    @classmethod
    def setUpTestData(cls):
        """Setup all data"""
        # The env variable GITHUB_WORKSPACE was set in order to facilitate CI
        # via github actions. When running the tests on a local machine,
        # export the variable to be the project's root as follows:
        # $ GITHUB_WORKSPACE='/path/to/project/root' python manage.py test
        cls._data_dir = Path(get_env_value("GITHUB_WORKSPACE")).joinpath("Data")
        cls._cds_files = list(cls._data_dir.glob("*cds.fa"))
        cls._protein_files = list(cls._data_dir.glob("*pep.fa"))
        _genomes = list(cls._data_dir.glob("*.fa"))
        for i in cls._cds_files + cls._protein_files:
            _genomes.remove(i)
        cls._genome_files = _genomes
        cls.gene = next(SeqIO.parse(cls._cds_files[0], "fasta"))
        cls.protein = next(SeqIO.parse(cls._protein_files[0], "fasta"))
        cls.genome = next(SeqIO.parse(cls._genome_files[0], "fasta"))

    def test_gene_parsing_return_type(self):
        gene_parser = FASTAParser(DEFAULT_CDS)
        parsed_dict = gene_parser(self.gene)
        self.assertIsInstance(parsed_dict, dict)

    def test_gene_parsing_regex_matches_one(self):
        gene_parser = FASTAParser(DEFAULT_CDS)
        parsed_dict = gene_parser(self.gene)
        _expected = DEFAULT_CDS.keys()
        _observed = parsed_dict.keys()
        self.assertSequenceEqual(_observed, _expected)

    # def test_protein_parsing_regex_matches_one(self):
    #    gene_parser = FASTAParser(DEFAULT_PROTEIN)
    #    parsed_dict = gene_parser(self.protein)
    #    _expected = DEFAULT_PROTEIN.keys()
    #    _observed = parsed_dict.keys()
    #    self.assertEquals(set(_observed), set(_expected))
