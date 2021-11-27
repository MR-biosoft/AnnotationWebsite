# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#       DONE
#   * Make sure each model has one field with primary_key=True
#       DONE
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#       DONE
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
#       will not be done
# Feel free to rename the models, but don't rename db_table values or field names.

# We will now test this configuration
#

from django.db import models


class Member(models.Model):
    email = models.CharField(primary_key=True, max_length=50)
    pwd = models.CharField(max_length=50, blank=True, null=True)
    firstname = models.CharField(max_length=30, blank=True, null=True)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    role = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "member"


class Genome(models.Model):
    chromosome = models.CharField(primary_key=True, max_length=20)
    specie = models.CharField(max_length=20, blank=True, null=True)
    strain = models.CharField(max_length=10, blank=True, null=True)
    sequence = models.TextField()
    length = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "genome"


class GeneProtein(models.Model):
    accession_number = models.CharField(primary_key=True, max_length=8)
    dna_length = models.IntegerField(blank=True, null=True)
    start_position = models.IntegerField(blank=True, null=True)
    end_position = models.IntegerField(blank=True, null=True)
    reading_frame = models.IntegerField(blank=True, null=True)
    aa_length = models.IntegerField(blank=True, null=True)
    chromosome = models.ForeignKey(
        "Genome", models.DO_NOTHING, db_column="chromosome", blank=True, null=True
    )
    isannotated = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "gene_protein"


class GeneSeq(models.Model):
    accession_number = models.OneToOneField(
        GeneProtein, models.DO_NOTHING, db_column="accession_number", primary_key=True
    )
    sequence = models.CharField(max_length=6000)

    class Meta:
        managed = False
        db_table = "gene_seq"


class ProteinSeq(models.Model):
    accession_number = models.OneToOneField(
        GeneProtein, models.DO_NOTHING, db_column="accession_number", primary_key=True
    )
    sequence = models.CharField(max_length=2000)

    class Meta:
        managed = False
        db_table = "protein_seq"


class Annotation(models.Model):
    accession_number = models.CharField(primary_key=True, max_length=8)
    gene_name = models.CharField(max_length=5, blank=True, null=True)
    gene_symbol = models.CharField(max_length=10, blank=True, null=True)
    gene_biotype = models.CharField(max_length=30, blank=True, null=True)
    transcript_biotype = models.CharField(max_length=30, blank=True, null=True)
    function = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    email = models.ForeignKey(
        "Member", models.DO_NOTHING, db_column="email", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "annotation"


class Decision(models.Model):
    accession_number = models.OneToOneField(
        "GeneProtein", models.DO_NOTHING, db_column="accession_number", primary_key=True
    )
    attempt_number = models.IntegerField()
    isapproved = models.BooleanField(blank=True, null=True)
    comment = models.CharField(max_length=1000, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "decision"
        unique_together = (("accession_number", "attempt_number"),)
