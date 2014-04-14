# -*- coding: utf-8 -*-

"""
Definition of database models.
"""

from mongoengine import (
    Document,
    EmailField,
    StringField,
    DateTimeField,
    ListField,
    FloatField,
    URLField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ReferenceField,
    BooleanField,
    connect)

connect('researchlbc', host='localhost', port=27017)


class Ad(EmbeddedDocument):

    """A simplified model of a Leboncoin ad."""

    title = StringField()
    price = FloatField()
    url = URLField()
    city = StringField()
    pubdate = DateTimeField()
    pro = BooleanField()


class User(Document):

    """The User model."""

    email = EmailField()


class Research(EmbeddedDocument):

    """A research on Leboncoin."""

    title = StringField()
    url = URLField()
    add_date = DateTimeField()
    end_date = DateTimeField()
    results = ListField(EmbeddedDocumentField(Ad))
    user = ReferenceField(User)
