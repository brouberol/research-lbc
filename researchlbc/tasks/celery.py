# -*- coding: utf-8 -*-

"""Definition of the Celery application."""
from __future__ import absolute_import

from researchlbc.tasks import celeryconfig

from celery import Celery

celery = Celery('researchlbc')
celery.config_from_object(celeryconfig)
