SET search_path TO GenesAnnotation;

DROP TABLE IF EXISTS annotation, history_annot, protein_seq, gene_seq, gene_protein, genome, member;
DROP DOMAIN IF EXISTS PHONE_NUMBER, AC, GENE_SEQUENCE, PROTEIN_SEQUENCE;
DROP SCHEMA IF EXISTS GenesAnnotation;
