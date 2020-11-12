#!/usr/bin/env python
import os
import sys
import environ


if __name__ == "__main__":
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings.deployment')
    env = environ.Env(
        DEBUG=(bool, False)
    )
    environ.Env.read_env(envfile=os.path.join(os.getcwd(), '.env'))
    RUN_ENV = env.str('RUN_ENV', 'local')

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuration.settings.' + RUN_ENV)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # This allows easy placement of apps within the interior core directory.
    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(current_path, 'core'))

    execute_from_command_line(sys.argv)
