# AnnotationWebsite

[![CI](https://github.com/MR-biosoft/AnnotationWebsite/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/MR-biosoft/AnnotationWebsite/actions/workflows/main.yml)
[![asd](https://github.com/MR-biosoft/AnnotationWebsite/actions/workflows/database.yml/badge.svg?branch=main)](https://github.com/MR-biosoft/AnnotationWebsite/actions/workflows/database.yml)

Website on genome annotation

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


To execute sql scripts use the command `dbexec`
For example to create all the necessary tables, use : 
```bash
cd Python/prokaryote
python manage.py dbexec ../../Database/create-schema.sql  
```
