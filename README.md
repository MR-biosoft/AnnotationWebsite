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

To execute sql scripts use the command `dbexec`
For example to create all the necessary tables, use : 
```bash
cd Python/prokaryote
python manage.py dbexec ../../Database/create-schema.sql  
```
