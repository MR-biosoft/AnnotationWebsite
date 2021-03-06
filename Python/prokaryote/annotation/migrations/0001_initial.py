# Generated by Django 3.2.9 on 2021-11-27 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Annotation",
            fields=[
                (
                    "accession_number",
                    models.CharField(max_length=8, primary_key=True, serialize=False),
                ),
                ("gene_name", models.CharField(blank=True, max_length=5, null=True)),
                ("gene_symbol", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "gene_biotype",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
                (
                    "transcript_biotype",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
                ("function", models.CharField(blank=True, max_length=50, null=True)),
                ("status", models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                "db_table": "annotation",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="GeneProtein",
            fields=[
                (
                    "accession_number",
                    models.CharField(max_length=8, primary_key=True, serialize=False),
                ),
                ("dna_length", models.IntegerField(blank=True, null=True)),
                ("start_position", models.IntegerField(blank=True, null=True)),
                ("end_position", models.IntegerField(blank=True, null=True)),
                ("reading_frame", models.IntegerField(blank=True, null=True)),
                ("aa_length", models.IntegerField(blank=True, null=True)),
                ("isannotated", models.BooleanField(blank=True, null=True)),
            ],
            options={
                "db_table": "gene_protein",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Genome",
            fields=[
                (
                    "chromosome",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("specie", models.CharField(blank=True, max_length=20, null=True)),
                ("strain", models.CharField(blank=True, max_length=10, null=True)),
                ("sequence", models.TextField()),
                ("length", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "genome",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Member",
            fields=[
                (
                    "email",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("pwd", models.CharField(blank=True, max_length=50, null=True)),
                ("firstname", models.CharField(blank=True, max_length=30, null=True)),
                ("lastname", models.CharField(blank=True, max_length=30, null=True)),
                ("phone", models.CharField(blank=True, max_length=16, null=True)),
                ("role", models.CharField(blank=True, max_length=9, null=True)),
            ],
            options={
                "db_table": "member",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Decision",
            fields=[
                (
                    "accession_number",
                    models.OneToOneField(
                        db_column="accession_number",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="annotation.geneprotein",
                    ),
                ),
                ("attempt_number", models.IntegerField()),
                ("isapproved", models.BooleanField(blank=True, null=True)),
                ("comment", models.CharField(blank=True, max_length=1000, null=True)),
                ("timestamp", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "decision",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="GeneSeq",
            fields=[
                (
                    "accession_number",
                    models.OneToOneField(
                        db_column="accession_number",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="annotation.geneprotein",
                    ),
                ),
                ("sequence", models.CharField(max_length=6000)),
            ],
            options={
                "db_table": "gene_seq",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ProteinSeq",
            fields=[
                (
                    "accession_number",
                    models.OneToOneField(
                        db_column="accession_number",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="annotation.geneprotein",
                    ),
                ),
                ("sequence", models.CharField(max_length=2000)),
            ],
            options={
                "db_table": "protein_seq",
                "managed": False,
            },
        ),
    ]
