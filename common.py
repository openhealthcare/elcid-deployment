from fabric.api import local, env, settings, hide
from fabric.context_managers import lcd
from fabric.contrib.files import _expand_path


def lexists(path):
    with settings(hide('everything'), warn_only=True):
        return not local('test -e {}'.format(_expand_path(path))).failed


class Pip(object):
    @classmethod
    def get_pip(cls):
        return "{}/bin/pip".format(
            env.virtual_env_path
        )

    @classmethod
    def install_virtualenvwrapper_if_necessary(cls):
        local("pip install virtualenv")

    @classmethod
    def create_virtual_env(cls):
        cls.install_virtualenvwrapper_if_necessary()
        if not lexists(env.virtual_env_path):
            local("virtualenv {0}".format(env.virtual_env_path))

    @classmethod
    def set_project_directory(cls):
        local("echo '{0}' > {1}/.project".format(
            env.home_dir, env.virtual_env_path
        ))

    @classmethod
    def install(cls, *pkgs):
        pip = cls.get_pip()
        for pkg in pkgs:
            local('{0} install -U {1}'.format(pip, pkg))

    @classmethod
    def install_requirements(cls):
        local("{0} install -r requirements.txt".format(cls.get_pip()))


def restart_database():
    if env.pg_version < (9, 0):
        local('sudo /etc/init.d/postgresql-8.4 restart || /etc/init.d/postgresql-8.4 start')
    else:
        local('sudo /etc/init.d/postgresql restart || /etc/init.d/postgresql start')
