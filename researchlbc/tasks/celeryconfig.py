# -*- coding: utf-8 -*-

"""Configuration of the Celery application."""

BROKER_URL = 'mongodb://localhost:27017/celery'

# Result backend related settings
CELERY_RESULT_BACKEND = 'mongodb://localhost:27017'
CELERY_MONGODB_BACKEND_SETTINGS = {
    'database': 'celery',
    'taskmeta_collection': 'task_results',
}

# Time related settings
CELERY_TIMEZONE = 'Europe/Paris'
CELERY_ENABLE_UTC = True

# Tasks related settings
CELERY_INCLUDE = [
    "researchlbc.tasks.crawl"
]

# Queue related settings
CELERY_CREATE_MISSING_QUEUES = True
CELERY_ROUTES = {
}

# Human related settings
ADMINS = [('Balthazar Rouberol', 'brouberol@imap.cc'), ]
