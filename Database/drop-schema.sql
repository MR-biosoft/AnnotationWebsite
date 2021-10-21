SET search_path TO GenesAnnotation;

DROP TABLE IF EXISTS annot, protein_seq, gene_seq, gene_protein, genome, annotation, member;
DROP DOMAIN IF EXISTS phone_number, gene_name, gene_sequence, protein_sequence;
DROP SCHEMA GenesAnnotation;
