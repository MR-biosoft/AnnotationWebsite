-- psql -d public -U ubuntu -f create-schema.sql

-- The authorization scheme is a good idea once the site
-- will be operational and deployed.
-- For debug and development, we will keep it commented out.

-- G: I commented out the schema creation because using PostgreSQL
-- schemas does not work out of the box in Django. To save us 
-- time and possible bugs that could be caused by implementing a 
-- database router, I am modifying all scripts to use DATABASEs
-- instead of SCHEMAs.

-- CREATE SCHEMA IF NOT EXISTS GenesAnnotation; --AUTHORIZATION ubuntu;
-- SET search_path TO GenesAnnotation;

\c annotationsite;

CREATE DOMAIN PHONE_NUMBER AS
    VARCHAR(16)
    CONSTRAINT check_E164_format CHECK (VALUE ~ '^\+\d{9,15}');

CREATE DOMAIN AC AS
    CHAR(8) NOT NULL
    CONSTRAINT check_norm_accession_number CHECK (VALUE ~ '^[A-Z]{3}\d{5}');

CREATE DOMAIN GENOME_SEQUENCE AS
    TEXT NOT NULL
    CONSTRAINT check_genome_sequence CHECK (VALUE ~ '(A|T|C|G|N)*');

CREATE DOMAIN GENE_SEQUENCE AS
    VARCHAR(6000) NOT NULL
    CONSTRAINT check_nucleotide_sequence CHECK (VALUE ~ '(ATG|GTG|TTG)((A|T|C|G){3})*(TAA|TAG|TGA)');

CREATE DOMAIN PROTEIN_SEQUENCE AS
    VARCHAR(2000) NOT NULL
    CONSTRAINT check_protein_sequence CHECK (VALUE ~ 'M(A|R|N|D|C|Q|E|G|H|I|L|K|M|F|P|S|T|W|Y|V)*');

CREATE TABLE IF NOT EXISTS member(
    email VARCHAR(50),
    pwd VARCHAR(50),
    firstname VARCHAR(30),
    lastname VARCHAR(30),
    phone PHONE_NUMBER,
    role VARCHAR(9),
    PRIMARY KEY (email),
    CONSTRAINT check_role_available CHECK (role IN ('reader','annotator','validator')));

CREATE TABLE IF NOT EXISTS genome(
    chromosome VARCHAR(20),
    specie VARCHAR(20),
    strain VARCHAR(10),
    sequence GENOME_SEQUENCE,
    length INTEGER,
    PRIMARY KEY (chromosome));

CREATE TABLE IF NOT EXISTS gene_protein(
    accession_number AC,
    dna_length INTEGER,
    start_position INTEGER,
    end_position INTEGER,
    reading_frame INTEGER,
    aa_length INTEGER,
    chromosome VARCHAR(20),
    isAnnotated BOOLEAN,
    PRIMARY KEY (accession_number),
    CONSTRAINT fkey_gene_protein_chromosome FOREIGN KEY (chromosome) REFERENCES genome(chromosome));

CREATE TABLE IF NOT EXISTS gene_seq(
    accession_number AC,
    sequence GENE_SEQUENCE,
    PRIMARY KEY (accession_number),
    CONSTRAINT fkey_gene_ac FOREIGN KEY (accession_number) REFERENCES gene_protein(accession_number));

CREATE TABLE IF NOT EXISTS protein_seq(
    accession_number AC,
    sequence PROTEIN_SEQUENCE,
    PRIMARY KEY (accession_number),
    CONSTRAINT fkey_protein_ac FOREIGN KEY (accession_number) REFERENCES gene_protein(accession_number));

CREATE TABLE IF NOT EXISTS annotation(
    accession_number AC,
    gene_name CHAR(5),
    gene_symbol VARCHAR(10),
    gene_biotype VARCHAR(30),
    transcript_biotype VARCHAR(30),
    function VARCHAR(50),
    status VARCHAR(10),
    email VARCHAR(50),
    PRIMARY KEY (accession_number),
    CONSTRAINT fkey_annotation_email FOREIGN KEY (email) REFERENCES member(email),
    CONSTRAINT check_status_available CHECK (status IN ('ongoing','approved','rejected')));

CREATE TABLE IF NOT EXISTS decision(
    accession_number AC,
    attempt_number INTEGER,
    isApproved BOOLEAN,
    comment VARCHAR(1000),
    timestamp TIMESTAMP default CURRENT_TIMESTAMP,
    PRIMARY KEY (accession_number, attempt_number),
    CONSTRAINT fkey_decision_ac FOREIGN KEY (accession_number) REFERENCES gene_protein(accession_number));

CREATE INDEX index_strain ON genome USING hash (strain);

/*
INSERT INTO genome VALUES(
    'CHR', 'Escherichia Coli', 'CTF38', 'ANTCGNTNCA', 10
);

INSERT INTO gene_protein VALUES(
    'AAA33333', 3000, 1, 3000, 1, 1000, 'CHR', FALSE
);

INSERT INTO decision VALUES
    ('AAA33333', 1, TRUE, 'RAS'
);
*/
