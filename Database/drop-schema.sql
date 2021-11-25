--SET search_path TO GenesAnnotation;

--\c annotationsite;

DROP TABLE IF EXISTS decision, annotation, protein_seq, gene_seq, gene_protein, genome, member;
DROP DOMAIN IF EXISTS PHONE_NUMBER, AC, GENOME_SEQUENCE, GENE_SEQUENCE, PROTEIN_SEQUENCE;
--DROP SCHEMA IF EXISTS GenesAnnotation;

--\c postgres;

