
-- minimal tests

INSERT INTO genome VALUES(
    'CHR', 'Escherichia Coli', 'CTF38', 'ANTCGNTNCA', 10
);

INSERT INTO gene_protein VALUES(
    'AAA33333', 3000, 1, 3000, 1, 1000, 'CHR', FALSE
);

INSERT INTO decision VALUES
    ('AAA33333', 1, TRUE, 'RAS'
);
