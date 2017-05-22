import os
from fabric.api import local, env
from fabric.context_managers import lcd
from common import Pip, lexists, Git
from postgres_helper import Postgres


def install_requirements():
    Pip.install_requirements()


def create_env():
    """
        so we assume the branch name is something like v0.6.0
        we strip off the first letter and the .s so we expect
        the virtualenv name to be 060
    """
    Pip.nix_user()
    Git.checkout_branch()
    Pip.set_project_directory()
    with lcd(env.project_path):
        Pip.install_requirements()
    symlink_nginx()
    Postgres.create_user_and_database()
    symlink_upstart()


def symlink_nginx():
    absPathNginxConf = os.path.join(env.project_path, "etc/nginx.conf")
    if not lexists(absPathNginxConf):
        raise ValueError("we expect an nginx conf to exist")

    symlink_name = '/etc/nginx/sites-enabled/{}'.format(env.project_name)
    if lexists(symlink_name):
        local("sudo rm {}".format(symlink_name))

    local('sudo ln -s {0} {1}'.format(absPathNginxConf, symlink_name))


def symlink_upstart():
    absPathUpstartConf = os.path.join(env.project_path, "etc/upstart.conf")
    if not lexists(absPathUpstartConf):
        raise ValueError("we expect an upstart conf to exist")

    symlink_name = '/etc/init/{}.conf'.format(env.project_name)
    if lexists(symlink_name):
        local("sudo rm {}".format(symlink_name))

    local('sudo ln -s {0} {1}'.format(absPathUpstartConf, symlink_name))
