from os import getenv

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'test_task_skyeng': {
            'format': '[%(asctime)s] %(levelname)s %(module)s %(process)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'test_task_skyeng',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
    'root': {
        'handlers': ['console'],
        'level': getenv('DJANGO_LOG_LEVEL', 'INFO'),
    },
}
