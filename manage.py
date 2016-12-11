#!/usr/bin/env python3
import json
import os
import sys


def set_deploy_config():
    deploy_config_path = os.environ.get('DEPLOY_CONFIG')
    if deploy_config_path is None or not os.path.isfile(deploy_config_path):
        return

    with open(deploy_config_path) as file_:
        data = json.load(file_)
        for env_var, value in data.items():
            os.environ.setdefault(env_var, value)


if __name__ == "__main__":
    set_deploy_config()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "almuersos.settings.local")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
