# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import re
import os

from fabric.api import env, run
from fabric.colors import yellow
from fabric.context_managers import cd, shell_env
from fabric.contrib.files import sed
from fabric.operations import local, put, sudo


PROJECT_NAME = 'almuersos'
GIT_REPO = 'git@github.com:ekauffmann/AlmuerSOS-API.git'


def development(tag):
    env.name = 'develop'
    env.hosts = ['develop.almuersos.cl']
    env.deploy_user = 'almuersos-api-dev'
    env.tag = tag
    env.migrate_db = True
    set_env_vars()


def production(tag):
    env.name = 'production'
    env.hosts = ['almuersos.cl']
    env.deploy_user = 'almuersos-api-prod'
    env.tag = tag
    env.migrate_db = True
    set_env_vars()


def set_env_vars():
    env.user = 'ubuntu'  # User with sudo
    env.home = '/home/{0:s}'.format(env.deploy_user)
    env.python_env_version = 'python3'
    env.python_env_path = os.path.join(env.home, 'envs', env.tag)

    env.git_repo_url = local('git config --get remote.origin.url', capture=True)
    env.git_repo_path = os.path.join(env.home, 'repos', env.tag)
    env.gunicorn_log_path = os.path.join(env.home, 'logs', env.tag)


def deploy():
    env.server_env_vars = _get_environ_vars()

    install_packages()
    prepare_environment()
    repo_update()
    repo_activate_version()
    install_dependencies()
    django_migrate_db()
    django_collect_static()
    config_gunicorn()
    restart_services()


def install_packages():
    print yellow('\nInstalling system packages')
    sudo('apt -y install ' + ' '.join(
        [
            'build-essential',
            'python3-dev',
            'python-pip',
            'python-virtualenv',
            'git-core',
            'postgresql-server-dev-all',
            'gunicorn',
            'nginx-full',
            'libffi-dev',
            'libssl-dev',
        ]
    ))


def prepare_environment():
    print(yellow('\nPreparing environment'))
    with shell_env(HOME=env.home), cd(env.home):
        sudo('mkdir -p envs logs repos', user=env.deploy_user)

        sudo(
            '[ ! -d {1:s} ] && virtualenv -p {0:s} {1:s} || echo "Python environment already exists"'.format(
                env.python_env_version,
                env.python_env_path
            ),
            user=env.deploy_user
        )
        sudo('{0:s}/bin/pip install -U pip'.format(env.python_env_path), user=env.deploy_user)
        _install_gunicorn()


def repo_update():
    print(yellow('\nUpdate repository'))
    with shell_env(HOME=env.home), cd('{0:s}/repos'.format(env.home)):
        sudo(
            '[ ! -d {0:s} ] && git clone {1:s} {0:s} || (cd {0:s} && git fetch)'.format(
                env.git_repo_path,
                GIT_REPO
            ),
            user=env.deploy_user
        )


def repo_activate_version():
    print(yellow('\nActivating repository version'))
    with shell_env(HOME=env.home), cd(env.git_repo_path):
        sudo(
            'git checkout {0:s}'.format(env.tag),
            user=env.deploy_user
        )
        sudo(
            'git pull'.format(env.tag),
            user=env.deploy_user
        )


def install_dependencies():
    print(yellow('\nInstalling dependencies'))
    with shell_env(HOME=env.home), cd(env.git_repo_path):
        sudo('{0:s}/bin/pip install -r requirements.txt'.format(env.python_env_path), user=env.deploy_user)


def django_migrate_db():
    if not env.migrate_db:
        return

    print yellow('\nDjango migrate DB')
    with shell_env(HOME=env.home, **env.server_env_vars), cd(env.git_repo_path):
        sudo('{0:s}/bin/python manage.py migrate'.format(env.python_env_path), user=env.deploy_user)


def django_collect_static():
    print yellow('\nDjango collect static')

    with shell_env(HOME=env.home, **env.server_env_vars), cd(env.git_repo_path):
        sudo(
            '{0:s}/bin/python manage.py collectstatic --noinput'.format(env.python_env_path),
            user=env.deploy_user
        )


def config_gunicorn():
    print yellow('\nCopying Gunicorn config file')

    remote_file = '/etc/gunicorn.d/{0:s}_{1:s}'.format(PROJECT_NAME, env.name)

    put('deploy/gunicorn.py', remote_file, use_sudo=True)

    replacements = (
        ('USER_HOME', env.home,),
        ('VIRTUALENV_PATH', env.python_env_path,),
        ('USER', env.deploy_user,),
        ('PROJECT_PATH', env.git_repo_path,),
        ('GUNICORN_LOG_PATH', env.gunicorn_log_path,),
        ('ENV_NAME', env.name,),
    )

    for replacement in replacements:
        sed(remote_file, '<{0:s}>'.format(replacement[0]), replacement[1], use_sudo=True)

    # Replace environment vars
    sed(remote_file, '<ENV_VARS>', json.dumps(env.server_env_vars), use_sudo=True)

    sudo('rm /etc/gunicorn.d/*.bak')


def restart_services():
    print(yellow('\nRestarting services'))
    sudo('service gunicorn restart', pty=False)


def _get_environ_vars():
    env_vars = sudo(
        'cat {0:s}'.format(os.path.join(env.home, 'configs', '{0:s}.json'.format(env.name))),
        user=env.deploy_user
    )
    return json.loads(env_vars)


def _install_gunicorn():
    gunicorn_version = run('gunicorn --version')
    gunicorn_version = re.sub('[^0-9\.]', '', gunicorn_version)
    sudo(
        '{0:s}/bin/pip install -U gunicorn=={1:s}'.format(env.python_env_path, gunicorn_version),
        user=env.deploy_user
    )
