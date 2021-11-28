# AnnotationWebsite

[![CI](https://github.com/MR-biosoft/AnnotationWebsite/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/MR-biosoft/AnnotationWebsite/actions/workflows/main.yml)
[![asd](https://github.com/MR-biosoft/AnnotationWebsite/actions/workflows/database.yml/badge.svg?branch=main)](https://github.com/MR-biosoft/AnnotationWebsite/actions/workflows/database.yml)

Website on genome annotation

To execute sql scripts use the command `dbexec`
For example to create all the necessary tables, use : 
```bash
cd Python/prokaryote
python manage.py dbexec ../../Database/create-schema.sql  
```
