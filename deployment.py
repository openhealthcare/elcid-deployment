import os
from fabric.api import local, env
from fabric.context_managers import prefix, lcd
from common import Pip, lexists
from postgres_helper import Postgres


def get_release_name():
    release_name = env.branch_name.replace(".", "")[1:]
    return "{0}{1}".format(env.project_name, release_name)


def install_requirements():
    Pip.install_requirements()


def create_env():
    """
        so we assume the branch name is something like v0.6.0
        we strip off the first letter and the .s so we expect
        the virtualenv name to be 060
    """
    Pip.create_virtual_env()
    with lcd(env.home_dir):
        if not lexists(env.release_name):
            local("git clone {0} {1}".format(env.github_url, env.release_name))
        with lcd(env.release_name):
            local("git fetch")
            local("git checkout {0}".format(env.branch_name))
            local("git pull origin {}".format(env.branch_name))

    Pip.set_project_directory()
    with lcd(env.project_path):
        Pip.install_requirements()
    symlink_nginx()
    create_database()
    symlink_upstart()


def create_database(file_name=None):
    """
        create a database with the appropriate name
    """
    Postgres.create_user()
    Postgres.create_database()


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
