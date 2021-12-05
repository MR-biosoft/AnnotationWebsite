"""
    Docstring
"""

import json
from pathlib import Path
from datetime import datetime

from django.test import TestCase, TransactionTestCase, tag

# BioPython Utils
from Bio import SeqIO, Seq

# Imports from our module
from annotation import models
from annotation.parsing import FASTAParser, save_genome
from annotation.bioregex import DEFAULT_CDS, DEFAULT_PROTEIN, DEFAULT_GENOME
from annotation.devutils import get_env_value

_LOGGING_DIR_NAME: str = "TestingLogs"


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

        # Specify project root
        cls._root_dir = Path(get_env_value("GITHUB_WORKSPACE"))

        # Set logging location (and create it if necessary)
        cls.logging_dir = cls._root_dir.joinpath(_LOGGING_DIR_NAME)
        if not cls.logging_dir.exists():
            cls.logging_dir.mkdir()

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

        cls.genome_data_dict = {
            "Escherichia_coli_cft073.fa": {
                "specie": "Escherichia coli",
                "strain": "cft073",
            },
            "Escherichia_coli_o157_h7_str_edl933.fa": {
                "specie": "Escherichia coli",
                "strain": "edl933",
            },
            "Escherichia_coli_str_k_12_substr_mg1655.fa": {
                "specie": "Escherichia coli",
                "strain": "k12",
            },
            "new_coli.fa": {
                "specie": None,
                "strain": None,
            },
        }

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
        # Check if at least one of the desired fields could be retrieved
        self.assertGreater(len(_observed), 0)
        # Check that the retrieved fields are a subset of the expected ones
        self.assertTrue(set(_expected).issuperset(set(_observed)))

    def regex_strict_matching_verifier(
        self, parsed_dict, bioregex_dict, fasta_file: Path, fasta_entry: Seq.Seq
    ):
        """Utility method used to detect anomalies in parsed FASTA
        files."""
        _expected = bioregex_dict.keys()
        _observed = parsed_dict.keys()
        try:
            self.assertSequenceEqual(_observed, _expected)
        except AssertionError as _ae:
            mismatch_len = len(_expected) - len(_observed)
            error_log = {
                "UTCdatetime": str(datetime.utcnow()),
                "FASTAHeader": fasta_entry.description,
                "MismatchLength": mismatch_len,
                "ExpectedKeys": list(_expected),
                "ObservedKeys": list(_observed),
                "MissingKeys": list(set(_expected).difference(set(_observed))),
            }
            logging_file = self.logging_dir.joinpath(
                f"{fasta_file.name}_parsing_errors.jsonl"
            )
            _modes = {True: "a", False: "w"}
            with open(
                logging_file, _modes[logging_file.exists()], encoding="utf-8"
            ) as _logfile:
                _logfile.write(f"{json.dumps(error_log)}\n")

    def full_iteration_regex_matcher(
        self, iterable_file_set, annotation_parser, reference_regex_dict
    ):
        """Utility method used to iterate over all files of
        a collection (like self.annotated_genomes), and nested
        iterating along all the fasta entries contained
        in each one of the files."""
        for _seq_file in iterable_file_set:
            print(f"\nParsing file {_seq_file.name}", end="...\t")
            with open(_seq_file, "r", encoding="utf-8") as _seq_handle:
                for fasta_entry in SeqIO.parse(_seq_handle, "fasta"):
                    _parsed = annotation_parser(fasta_entry)
                    self.regex_matching_verifier(_parsed, reference_regex_dict)
                    self.regex_strict_matching_verifier(
                        _parsed, reference_regex_dict, _seq_file, fasta_entry
                    )
            print("Done")

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
        self.full_iteration_regex_matcher(
            self.annotated_genomes, self.genome_parser, DEFAULT_GENOME
        )

    def test_protein_parsing_regex_matches_all_annotated(self):
        """Test protein regex matches all desired fields,
        on all files which we know beforehand are properly annotated."""
        self.full_iteration_regex_matcher(
            self.annotated_proteins, self.protein_parser, DEFAULT_PROTEIN
        )

    def test_gene_parsing_regex_matches_all_annotated(self):
        """Test gene regex matches all desired fields,
        on all files which we know beforehand are properly annotated."""
        self.full_iteration_regex_matcher(
            self.annotated_cds, self.gene_parser, DEFAULT_CDS
        )


class DatabaseIntegrationTest(AnnotationTest, TransactionTestCase):
    """Class defined to verify that parsed data can be imported
    into the site's database"""

    @tag("devel", "db")
    def test_save_genomes_to_db(self):
        """ """
        for genome in self._genome_files:
            with open(genome, "r", encoding="utf-8") as _genome_handle:
                _genome_entries = list(SeqIO.parse(_genome_handle, "fasta"))
                # Each genome file should contain at most one FASTA entry
                self.assertTrue(len(_genome_entries) == 1)
                save_genome(
                    _genome_entries[0],
                    specie=self.genome_data_dict[genome.name]["specie"],
                    strain=self.genome_data_dict[genome.name]["strain"],
                )

    @tag("devel", "ci-skip")
    def test_save_a_protein(self):
        """ """
        pass
