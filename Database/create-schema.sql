
-- BEGIN DOMAIN DEFINITION
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
    TEXT NOT NULL
    CONSTRAINT check_nucleotide_sequence CHECK (VALUE ~ '(ATG|GTG|TTG)((A|T|C|G){3})*(TAA|TAG|TGA)');

CREATE DOMAIN PROTEIN_SEQUENCE AS
    TEXT NOT NULL
    CONSTRAINT check_protein_sequence CHECK (VALUE ~ 'M(A|R|N|D|C|Q|E|G|H|I|L|K|M|F|P|S|T|W|Y|V)*');
-- END DOMAIN DEFINITION

-- BEGIN TABLES DEFINITION
CREATE TABLE IF NOT EXISTS member(
    email VARCHAR(50),
    pwd VARCHAR(50),
    firstname VARCHAR(30),
    lastname VARCHAR(30),
    phone PHONE_NUMBER,
    role VARCHAR(9),
    PRIMARY KEY (email),
    CONSTRAINT check_role_available CHECK (role IN ('reader','annotator','validator'))
);

CREATE TABLE IF NOT EXISTS genome(
    chromosome VARCHAR(20),
    specie VARCHAR(20),
    strain VARCHAR(10),
    sequence GENOME_SEQUENCE,
    length INTEGER,
    PRIMARY KEY (chromosome)
);

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
    CONSTRAINT fkey_gene_protein_chromosome FOREIGN KEY (chromosome) REFERENCES genome(chromosome)
);

CREATE TABLE IF NOT EXISTS gene_seq(
    accession_number AC,
    sequence GENE_SEQUENCE,
    PRIMARY KEY (accession_number),
    CONSTRAINT fkey_gene_ac FOREIGN KEY (accession_number) REFERENCES gene_protein(accession_number)
);

CREATE TABLE IF NOT EXISTS protein_seq(
    accession_number AC,
    sequence PROTEIN_SEQUENCE,
    PRIMARY KEY (accession_number),
    CONSTRAINT fkey_protein_ac FOREIGN KEY (accession_number) REFERENCES gene_protein(accession_number)
);

CREATE TABLE IF NOT EXISTS annotation(
    accession_number AC,
    gene_name CHAR(5),
    gene_symbol VARCHAR(10),
    gene_biotype VARCHAR(30),
    transcript_biotype VARCHAR(30),
    function VARCHAR(200),
    status VARCHAR(10),
    email VARCHAR(50),
    PRIMARY KEY (accession_number),
    CONSTRAINT fkey_annotation_ac FOREIGN KEY (accession_number) REFERENCES gene_protein(accession_number),
    CONSTRAINT fkey_annotation_email FOREIGN KEY (email) REFERENCES member(email),
    CONSTRAINT check_status_available CHECK (status IN ('ongoing','approved','rejected'))
);

CREATE TABLE IF NOT EXISTS decision(
    accession_number AC,
    attempt_number INTEGER,
    isApproved BOOLEAN,
    comment VARCHAR(1000),
    timestamp TIMESTAMP default CURRENT_TIMESTAMP,
    PRIMARY KEY (accession_number, attempt_number),
    CONSTRAINT fkey_decision_ac FOREIGN KEY (accession_number) REFERENCES gene_protein(accession_number)
);
-- END TABLES DEFINITION

-- BEGIN INDEX CREATION
CREATE INDEX index_strain ON genome USING hash (strain);
-- END INDEX CREATION
