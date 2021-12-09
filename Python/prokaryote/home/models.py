"""
.Rhistory
"""

import string
from datetime import datetime
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class MissingMandatoryField(ValueError):
    pass


# Create your models here.
class CustomAccountManager(BaseUserManager):
    """Custom Account Manager got member"""

    def create_user(
        self,
        email,
        username,
        firstname,
        password,
        **other_fields,
    ):
        if not email:
            raise MissingMandatoryField("You must provide an email address")

        email = self.normalize_email(email)
        member = self.model(
            email=email,
            username=username,
            firstname=firstname,
            **other_fields,
        )
        member.set_password(password)
        member.save()
        return member

    def create_superuser(
        self,
        email,
        username,
        firstname,
        password,
        **other_fields,
    ):
        SUPER_USER_RIGHTS = ["is_staff", "is_superuser", "is_active"]
        for right in SUPER_USER_RIGHTS:
            other_fields.setdefault(right, True)

        for right in SUPER_USER_RIGHTS:
            if not other_fields.get(right):
                raise ValueError(f"Superuser must be have `{right} == True`")

        return self.create_user(email, username, firstname, password, **other_fields)


class Member(AbstractBaseUser, PermissionsMixin):
    """Custom User class to override django's basic model"""

    READER = "r"
    ANNOTATOR = "a"
    VALIDATOR = "v"
    ROLE_CHOICES = [
        (READER, "reader"),
        (ANNOTATOR, "annotator"),
        (VALIDATOR, "validator"),
    ]

    email = models.EmailField(primary_key=True, max_length=50)
    username = models.CharField(max_length=15, unique=True)
    # password = models.CharField(max_length=50, blank=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    start_date = models.DateTimeField(default=datetime.utcnow)
    phone = models.CharField(max_length=16, blank=True, null=True)
    role = models.CharField(max_length=9, choices=ROLE_CHOICES, blank=True, null=True)
    # default django
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    # Needed to be proper auth applications
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "firstname"]

    def __repr__(self):
        _role = string.capwords(self.role)
        _fn = self.firstname
        _ln = self.lastname
        return f"{self.__class__.__name__}({_role}, {_fn}, {_ln})"
