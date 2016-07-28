import os
from fabric.api import local, env
from fabric.context_managers import prefix, lcd
from fabric.contrib.files import exists


def get_release_name():
    release_name = env.branch_name.replace(".", "")[1:]
    return "{0}{1}".format(env.project_name, release_name)


def install_requirements():
    with prefix("source ~/.bashrc"):
        with prefix("workon {}".format(env.release_name)):
            local("pip install -r requirements.txt")


def create_virtual_env():
    """
        so we assume the branch name is something like v0.6.0
        we strip off the first letter and the .s so we expect
        the virtualenv name to be 060
    """
    with lcd(env.home_dir):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            local("mkvirtualenv {}".format(env.release_name))
            local("git clone {0} {1}".format(env.github_url, env.release_name))
            with lcd(env.release_name):
                local("setvirtualenvproject .")
                local("git fetch")
                local("git checkout {0}".format(env.branch_name))


def remove_virtual_env():
    """
        the opposite of create virtual env
    """
    with lcd(env.home_dir):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            local("rmvirtualenv {}".format(env.release_name))
            local("rm -rf {}".format(env.release_name))


def create_database(file_name):
    """
        create a database with the appropriate name
    """
    with prefix("sudo -u postgres psql --command"):
        local("CREATE DATABASE {}".format(env.release_name))
        local("GRANT ALL PRIVILEGES ON DATABASE {} TO ohc;".format(env.release_name))

    local("sudo -u postgres psql {0} -f {1}".format(env.release_name, file_name))
    print "=" * 20
    print "CREATED DATABASE {}".format(env.release_name)
    print "PLEASE UPDATE YOUR LOCAL SETTINGS ACCORDINGLY"
    print "=" * 20


def drop_database():
    with prefix("sudo -u postgres psql --command"):
        local("DROP DATABASE {}".format(env.release_name))


def symlink_nginx():
    absPathNginxConf = os.abspath(
        os.path.join(env.home_dir, env.release_name, "etc/nginx.conf")
    )
    if not exists(absPathNginxConf):
        raise ValueError("we expect an nginx conf to exist")

    symlink_name = '/etc/nginx/sites-enabled/{}'.env.project_name
    if exists(symlink_name):
        local("rm {}".format(symlink_name))

    local('ln -s /etc/nginx/sites-enabled/'.format(env.project_name, absPathNginxConf))
