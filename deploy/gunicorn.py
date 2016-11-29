CONFIG = {
    'mode': 'wsgi',
    'python': '<VIRTUALENV_PATH>/bin/python',
    'user': '<USER>',
    'group': '<USER>',
    'working_dir': '<PROJECT_PATH>',
    'environment': <ENV_VARS>,
    'args': (
        '--error-logfile=<GUNICORN_LOG_PATH>',
        '--log-level=error',
        '--bind=unix:/var/run/almuersos_<ENV_NAME>.socket',
        '--workers=4',
        '--timeout=60',
        'almuersos.wsgi:application'
    ),
}
