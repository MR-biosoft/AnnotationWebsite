"""
    Docstring
"""
from pathlib import Path

from django.test import TestCase, TransactionTestCase

# from django.db import connection

# BioPython Utils
from Bio import SeqIO

# Imports from our module
from annotation import models
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
        cls.annotated_cds = [path for path in cls._cds_files if not "new" in path.name]
        cls.annotated_proteins = [
            path for path in cls._protein_files if not "new" in path.name
        ]
        cls.new_genomes = [path for path in cls._genome_files if "new" in path.name]
        cls.new_cds = [path for path in cls._cds_files if "new" in path.name]
        cls.new_proteins = [path for path in cls._protein_files if "new" in path.name]

        # Create single test sequences (first objects)
        cls.gene = next(SeqIO.parse(cls._cds_files[0], "fasta"))
        cls.protein = next(SeqIO.parse(cls._protein_files[0], "fasta"))
        cls.genome = next(SeqIO.parse(cls._genome_files[0], "fasta"))


class FASTAParserTest(AnnotationTest):
    """Class defined to verify the robustness and
    integrity of the implemented FASTA parser."""

    ## utility methods

    def regex_matching_verifier(self, parsed_dict, bioregex_dict):
        """Utility method used to reduce boilerplate in
        test_*_parsing_matches_* methods"""
        _expected = bioregex_dict.keys()
        _observed = parsed_dict.keys()
        self.assertSequenceEqual(_observed, _expected)

    ##

    def test_gene_parsing_return_type(self):
        """Test that the parser effectively returns a dictionary"""
        parsed_dict = self.gene_parser(self.gene)
        self.assertIsInstance(parsed_dict, dict)

    def test_gene_parsing_regex_matches_one(self):
        """Test gene regex matches all desired fields"""
        parsed_dict = self.gene_parser(self.gene)
        self.regex_matching_verifier(parsed_dict, DEFAULT_CDS)

    def test_protein_parsing_regex_matches_one(self):
        """Test protein regex matches all desired fields"""
        parsed_dict = self.protein_parser(self.protein)
        self.regex_matching_verifier(parsed_dict, DEFAULT_PROTEIN)

    def test_genome_parsing_regex_matches_one(self):
        """Test genome regex matches all desired fields"""
        parsed_dict = self.genome_parser(self.genome)
        self.regex_matching_verifier(parsed_dict, DEFAULT_GENOME)

    def test_genome_parsing_regex_matches_all_annotated(self):
        """Test genome regex matches all desired fields,
        on all files which we know beforehand are properly annotated."""
        for genome_file in self.annotated_genomes:
            with open(genome_file, "r", encoding="utf-8") as _genome_file:
                for genome in SeqIO.parse(_genome_file, "fasta"):
                    _parsed = self.genome_parser(genome)
                    self.regex_matching_verifier(_parsed, DEFAULT_GENOME)


class DatabaseIntegrationTest(AnnotationTest, TransactionTestCase):
    """Class defined to verify that parsed data can be imported
    into the site's database"""

    def test_save_a_genome(self):
        """ """
        save_genome(self.genome, specie="E. coli o157 h7", strain="edl933")

    def test_save_a_protein(self):
        """ """
        pass
