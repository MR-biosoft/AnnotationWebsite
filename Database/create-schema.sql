-- DROP DATABASE IF EXISTS GenesAnnotation;
-- CREATE DATABASE GenesAnnotation;

DROP SCHEMA IF EXISTS GenesAnnotation CASCADE;
-- The authorization scheme is a good idea once the site
-- will be operational and deployed.
-- For debug and development, we will keep it commented out.
CREATE SCHEMA IF NOT EXISTS GenesAnnotation; --AUTHORIZATION ubuntu;
SET search_path TO GenesAnnotation;

CREATE DOMAIN phone_number AS
    VARCHAR(16)
    CONSTRAINT check_E164_format CHECK (VALUE ~ '^\+\d{9,15}');

CREATE DOMAIN gene_name AS
    CHAR(8) NOT NULL
    CONSTRAINT check_norm_gene_name CHECK (VALUE ~ '^[A-Z]{3}\d{5}');

CREATE DOMAIN gene_sequence AS
    VARCHAR(6000) NOT NULL
    CONSTRAINT check_nucleotide_sequence CHECK (VALUE ~ '(ATG|GTG|TTG)((A|T|C|G){3})*(TAA|TAG|TGA)');

CREATE DOMAIN protein_sequence AS
    VARCHAR(2000) NOT NULL
    CONSTRAINT check_protein_sequence CHECK (VALUE ~ 'M(A|R|N|D|C|Q|E|G|H|I|L|K|M|F|P|S|T|W|Y|V)*');

CREATE TABLE IF NOT EXISTS member(
    email VARCHAR(50),
    pwd VARCHAR(50),
    firstname VARCHAR(30),
    lastname VARCHAR(30),
    phone phone_number,
    role VARCHAR(9),
    PRIMARY KEY (email),
    CONSTRAINT check_role_available CHECK (role IN ('reader','annotator','validator')));

CREATE TABLE IF NOT EXISTS annotation(
    id SERIAL,
    gene_symbol VARCHAR(10),
    gene_biotype VARCHAR(30),
    transcript_biotype VARCHAR(30),
    function VARCHAR(50),
    status VARCHAR(10),
    PRIMARY KEY (id),
    CONSTRAINT check_status_available CHECK (status IN ('ongoing','approved','rejected')));

CREATE TABLE IF NOT EXISTS genome(
    specie VARCHAR(20),
    strain VARCHAR(10),
    chromosome VARCHAR(20) CONSTRAINT Unique_chromosome UNIQUE,
    sequence TEXT,
    length INTEGER,
    PRIMARY KEY (specie,strain));

CREATE INDEX index_strain ON genome USING hash (strain);

CREATE TABLE IF NOT EXISTS gene_protein(
    name gene_name,
    gene_symbol VARCHAR(10),
    gene_biotype VARCHAR(30),
    length_dna INTEGER,
    start_position INTEGER,
    end_position INTEGER,
    reading_direction INTEGER,
    transcript_biotype VARCHAR(30),
    function VARCHAR(50),
    length_aa INTEGER,
    specie VARCHAR(20),
    strain VARCHAR(10),
    PRIMARY KEY (name),
    CONSTRAINT fkey_specie_strain FOREIGN KEY (specie,strain) REFERENCES genome(specie,strain));

CREATE TABLE IF NOT EXISTS gene_seq(
    name gene_name,
    sequence gene_sequence,
    PRIMARY KEY (name),
    CONSTRAINT fkey_gene_name FOREIGN KEY (name) REFERENCES gene_protein(name));

CREATE TABLE IF NOT EXISTS protein_seq(
    name gene_name,
    sequence protein_sequence,
    PRIMARY KEY (name),
    CONSTRAINT fkey_protein_name FOREIGN KEY (name) REFERENCES gene_protein(name));

CREATE TABLE IF NOT EXISTS annot(
    email VARCHAR(50),
    id BIGINT,
    name gene_name,
    PRIMARY KEY (email,id,name),
    FOREIGN KEY (email) REFERENCES member(email),
    FOREIGN KEY (id) REFERENCES annotation(id),
    FOREIGN KEY (name) REFERENCES gene_protein(name));
