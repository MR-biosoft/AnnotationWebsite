# Setup database
echo -n 'Database setup... '
./manage.py dbexec $GITHUB_WORKSPACE/Database/drop-schema.sql
./manage.py dbexec $GITHUB_WORKSPACE/Database/create-schema.sql
echo 'Done'
# Import genomes
echo -n 'Genome importation... '
./manage.py importgenome $GITHUB_WORKSPACE/Data/Escherichia_coli_str_k_12_substr_mg1655.fa --specie "Escherichia coli" --strain k12
./manage.py importgenome $GITHUB_WORKSPACE/Data/Escherichia_coli_o157_h7_str_edl933.fa --specie "Escherichia coli" --strain edl933
./manage.py importgenome $GITHUB_WORKSPACE/Data/Escherichia_coli_cft073.fa --specie "Escherichia coli" --strain cft073
./manage.py importgenome $GITHUB_WORKSPACE/Data/new_coli.fa
echo 'Done'
echo 'Genes importation... '
./manage.py importgenes $GITHUB_WORKSPACE/Data/Escherichia_coli_str_k_12_substr_mg1655_cds.fa 
./manage.py importgenes $GITHUB_WORKSPACE/Data/Escherichia_coli_o157_h7_str_edl933_cds.fa
./manage.py importgenes $GITHUB_WORKSPACE/Data/Escherichia_coli_cft073_cds.fa
./manage.py importgenes $GITHUB_WORKSPACE/Data/new_coli_cds.fa
echo 'Done'
echo 'Proteins importation... '
./manage.py importproteins $GITHUB_WORKSPACE/Data/Escherichia_coli_str_k_12_substr_mg1655_pep.fa 
./manage.py importproteins $GITHUB_WORKSPACE/Data/Escherichia_coli_o157_h7_str_edl933_pep.fa
./manage.py importproteins $GITHUB_WORKSPACE/Data/Escherichia_coli_cft073_pep.fa
./manage.py importproteins $GITHUB_WORKSPACE/Data/new_coli_pep.fa
echo 'Done'
