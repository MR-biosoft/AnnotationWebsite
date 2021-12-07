# AnnotationWebsite

[![CI](https://github.com/MR-biosoft/AnnotationWebsite/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/MR-biosoft/AnnotationWebsite/actions/workflows/main.yml)
[![asd](https://github.com/MR-biosoft/AnnotationWebsite/actions/workflows/database.yml/badge.svg?branch=main)](https://github.com/MR-biosoft/AnnotationWebsite/actions/workflows/database.yml)

Website on genome annotation

## Configuration

### Dependencies

This website is built using [Django](https://www.djangoproject.com/)

* [Poetry](https://python-poetry.org/) for Python dependencies management.
* [PostgreSQL](https://www.postgresql.org/) for database management.


### Django

To use django the following environment variables should be properly set and exported:
```bash
export DJANGO_SECRET_KEY="a django secret key"
export PG_DBNAME="the database name"
export PG_USER="the postgres user who owns the database"
export PG_PASSWORD="PG_USER'S password"
```

To run the Unit tests an additional environment variable should be set:
<!-- https://docs.python.org/3.8/library/unittest.html -->
```bash
export GITHUB_WORKSPACE="/the/path/to/the/repo's/root/on/your/machine"
``` 

You can add the previous variable exports to your `~/.bashrc`, so
that the variables are automatically loaded each time you open a new terminal.

### PostgreSQL

```bash
sudo -u postgres psql --command="CREATE USER $PG_USER;"
sudo -u postgres psql --command="ALTER USER $PG_USER WITH ENCRYPTED PASSWORD '$PG_PASSWORD';"
sudo -u postgres psql --command="ALTER ROLE $PG_USER SET client_encoding TO 'utf8';"
sudo -u postgres psql --command="ALTER ROLE $PG_USER SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql --command="ALTER ROLE $PG_USER SET timezone TO 'UTC';"
sudo -u postgres psql --command="ALTER ROLE $PG_USER WITH CREATEDB;"
sudo -u postgres createdb --owner="$PG_USER" "$PG_DBNAME"
PGPASSWORD="$PG_PASSWORD" psql --username="$PG_USER" --host=localhost --list
```

## Usage

Running the server and performing administrative tasks such as 
importing new genomes, go into the project's `BASE_DIR`. 
This is the directory created when executing 
`django-admin startproject {{projectname}}`. In our case, that 
is the `Python/prokaryote` directory.

```bash
cd Python/prokaryote
```

There you will find an executable file named `manage.py`. 
That is django's swiss-army knife. All commands related to testing,
debugging, data import, and database management should be run via
`manage.py`.

`manage.y` can be run in either of the following ways (the `-h` option displays a list of available subcommands):
```bash
./manage.py -h      # way 1: direct invocation
python manage.py -h # way 2: via Python (poetry's virtual env should be activated)
poetry run python manage.py -h # way 3: no need to activate the venv
```

### Run tests (unit and integration)

```bash
# CAVEATS: This is still in development, do not execute
# --exclude-tag changes whilst in development
./manage.py test -v 2 --no-input --reverse # --exclude-tag strict 
```

### Create the database (via `dbexec`)
To execute sql scripts use the command `dbexec`
For example to create all the necessary tables, use : 

```bash
python manage.py dbexec $GITHUB_WORKSPACE/Database/create-schema.sql  
```

### Import data
In order to annotate genomes, we should have some genomes available, right? FASTA files can easily be imported via the command line.

#### Genomes (via `importgenome`)
ATTENTION: This subcommand is configured to import one genome at a time. If your file contains more than one FASTA entry 
(i.e. lines starting with `>`), the command will fail with an informative error message.

```bash
./manage.py importgenome $GITHUB_WORKSPACE/Data/Escherichia_coli_str_k_12_substr_mg1655.fa --specie "Escherichia coli" --strain k12
./manage.py importgenome $GITHUB_WORKSPACE/Data/Escherichia_coli_o157_h7_str_edl933.fa --specie "Escherichia coli" --strain edl933
./manage.py importgenome $GITHUB_WORKSPACE/Data/Escherichia_coli_cft073.fa --specie "Escherichia coli" --strain cft073
./manage.py importgenome $GITHUB_WORKSPACE/Data/new_coli.fa
```

#### Genes (via `importgenomes`)
```bash
./manage.py importgenes $GITHUB_WORKSPACE/Data/Escherichia_coli_str_k_12_substr_mg1655_cds.fa
./manage.py importgenes $GITHUB_WORKSPACE/Data/Escherichia_coli_o157_h7_str_edl933_cds.fa
./manage.py importgenes $GITHUB_WORKSPACE/Data/Escherichia_coli_cft073_cds.fa
./manage.py importgenes $GITHUB_WORKSPACE/Data/new_coli_cds.fa

```
