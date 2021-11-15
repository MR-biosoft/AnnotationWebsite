
CREATE DATABASE AnnotationSite WITH OWNER djangoannot;

ALTER ROLE djangoannot SET client_encoding TO 'utf8';
ALTER ROLE djangoannot SET default_transaction_isolation TO 'read committed';
ALTER ROLE djangoannot SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE AnnotationSite TO djangoannot;
--GRANT ALL PRIVILEGES ON DATABASE AnnotationSite TO gml;
--GRANT ALL PRIVILEGES ON DATABASE AnnotationSite TO ubuntu;