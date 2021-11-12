-- The authorization scheme is a good idea once the site
-- will be operational and deployed.
-- For debug and development, we will keep it commented out.
CREATE SCHEMA IF NOT EXISTS GenesAnnotation; --AUTHORIZATION ubuntu;
SET search_path TO GenesAnnotation;

CREATE DOMAIN phone_number AS
    VARCHAR(16)
    CONSTRAINT check_E164_format CHECK (VALUE ~ '^\+\d{9,15}');

CREATE DOMAIN AC AS
    CHAR(8) NOT NULL
    CONSTRAINT check_norm_accession_number CHECK (VALUE ~ '^[A-Z]{3}\d{5}');

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

CREATE TABLE IF NOT EXISTS genome(
    chromosome VARCHAR(20),
    specie VARCHAR(20),
    strain VARCHAR(10),
    sequence TEXT,
    length INTEGER,
    PRIMARY KEY (chromosome));

CREATE TABLE IF NOT EXISTS gene_protein(
    accession_number AC,
    dna_length INTEGER,
    start_position INTEGER,
    end_position INTEGER,
    reading_frame INTEGER,
    transcript_biotype VARCHAR(30),
    chromosome VARCHAR(20),
    isAnnotated BOOLEAN,
    PRIMARY KEY (accession_number),
    CONSTRAINT fkey_gene_protein_chromosome FOREIGN KEY (chromosome) REFERENCES genome(chromosome));

CREATE TABLE IF NOT EXISTS gene_seq(
    accession_number AC,
    sequence gene_sequence,
    PRIMARY KEY (accession_number),
    CONSTRAINT fkey_gene_ac FOREIGN KEY (accession_number) REFERENCES gene_protein(accession_number));

CREATE TABLE IF NOT EXISTS protein_seq(
    accession_number AC,
    sequence protein_sequence,
    PRIMARY KEY (accession_number),
    CONSTRAINT fkey_protein_ac FOREIGN KEY (accession_number) REFERENCES gene_protein(accession_number));

CREATE TABLE IF NOT EXISTS history_annot(
    id SERIAL UNIQUE,
    isAccepted BOOLEAN,
    comment VARCHAR(500),
    time TIMESTAMP,
    PRIMARY KEY (id, time));

CREATE TABLE IF NOT EXISTS annotation(
    accession_number AC,
    name CHAR(5),
    gene_symbol VARCHAR(10),
    gene_biotype VARCHAR(30),
    transcript_biotype VARCHAR(30),
    function VARCHAR(50),
    status VARCHAR(10),
    email VARCHAR(50),
    id BIGINT,
    PRIMARY KEY (accession_number),
    CONSTRAINT fkey_annotation_email FOREIGN KEY (email) REFERENCES member(email),
    CONSTRAINT check_status_available CHECK (status IN ('ongoing','approved','rejected')),
    CONSTRAINT fkey_annotation_id FOREIGN KEY (id) REFERENCES history_annot(id));

CREATE INDEX index_strain ON genome USING hash (strain);
