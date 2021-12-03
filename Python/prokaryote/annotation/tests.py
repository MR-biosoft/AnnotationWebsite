from pathlib import Path

from django.test import TestCase, TransactionTestCase

# from django.db import connection

# BioPython Utils
from Bio import SeqIO

# Imports from our module
from annotation.parsing import FASTAParser, save_genome
from annotation.bioregex import DEFAULT_CDS, DEFAULT_PROTEIN, DEFAULT_GENOME
from annotation.devutils import get_env_value


class AnnotationTest(TestCase):
    """
    Parent class to define the following class methods:
        * setUpTestData
    """

    @classmethod
    def setUpTestData(cls):
        """Setup all data"""
        # The env variable GITHUB_WORKSPACE was set in order to facilitate CI
        # via github actions. When running the tests on a local machine,
        # export the variable to be the project's root as follows:
        # $ GITHUB_WORKSPACE='/path/to/project/root' python manage.py test

        # Create three parsers
        cls.gene_parser = FASTAParser(DEFAULT_CDS)
        cls.protein_parser = FASTAParser(DEFAULT_PROTEIN)
        cls.genome_parser = FASTAParser(DEFAULT_GENOME)

        # Create auxiliary data locations and file lists
        cls._data_dir = Path(get_env_value("GITHUB_WORKSPACE")).joinpath("Data")
        cls._cds_files = list(cls._data_dir.glob("*cds.fa"))
        cls._protein_files = list(cls._data_dir.glob("*pep.fa"))
        _genomes = list(cls._data_dir.glob("*.fa"))
        for i in cls._cds_files + cls._protein_files:
            _genomes.remove(i)
        cls._genome_files = _genomes

        # Create semantically consistent groups
        cls.annotated_genomes = [
            path for path in cls._genome_files if not "new" in path.name
        ]

        # Create single test sequences (first objects)
        cls.gene = next(SeqIO.parse(cls._cds_files[0], "fasta"))
        cls.protein = next(SeqIO.parse(cls._protein_files[0], "fasta"))
        cls.genome = next(SeqIO.parse(cls._genome_files[0], "fasta"))


class FASTAParserTest(AnnotationTest):
    """Class defined to verify the robustness and
    integrity of the implemented FASTA parser."""

    def test_gene_parsing_return_type(self):
        """Test that the parser effectively returns a dictionary"""
        parsed_dict = self.gene_parser(self.gene)
        self.assertIsInstance(parsed_dict, dict)

    def test_gene_parsing_regex_matches_one(self):
        """Test gene regex matches all desired fields"""
        parsed_dict = self.gene_parser(self.gene)
        _expected = DEFAULT_CDS.keys()
        _observed = parsed_dict.keys()
        self.assertSequenceEqual(_observed, _expected)

    def test_protein_parsing_regex_matches_one(self):
        """Test protein regex matches all desired fields"""
        parsed_dict = self.protein_parser(self.protein)
        _expected = DEFAULT_PROTEIN.keys()
        _observed = parsed_dict.keys()
        self.assertSequenceEqual(_observed, _expected)

    def test_genome_parsing_regex_matches_one(self):
        """Test genome regex matches all desired fields"""
        parsed_dict = self.genome_parser(self.genome)
        _expected = DEFAULT_GENOME.keys()
        _observed = parsed_dict.keys()
        self.assertSequenceEqual(_observed, _expected)


class DatabaseIntegrationTest(AnnotationTest, TransactionTestCase):
    """Class defined to verify that parsed data can be imported
    into the site's database"""

    def test_save_a_genome(self):
        """ """
        save_genome(self.genome, specie="E. coli o157 h7", strain="edl933")

    def test_save_a_protein(self):
        """ """
        pass
