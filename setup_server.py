import os
from fabric.api import local, env, settings
from common import lexists
from postgres_helper import Postgres


class Apt(object):
    @staticmethod
    def install(*pkgs):
        local('sudo apt-get install -y %s' % ' '.join(pkgs))

    @staticmethod
    def remove(pkg):
        local('sudo apt-get remove -y {}'.format(pkg))

    @staticmethod
    def upgrade():
        local('sudo apt-get update -y')
        local('sudo apt-get upgrade -y')


DEPLOYMENT_PACKAGES = [
    "postgresql",
    "postgresql-contrib",
    "python-psycopg2",

    # Python Dev
    "python-dev",
    "libffi-dev",
    "python-setuptools",
    "python-virtualenv",
    # Just nice"
    "screen",
    "vim",
    "emacs",
    "htop",
    "ack-grep",
    "virtualenvwrapper",
    "curl",
    "ipython",

    # Dev tools
    "git",
    "rake",
    "nodejs",
]

BASIC_PIP_PACKAGES = [

]


def create_users():
    users = [env.app_owner, env.database_owner]
    to_add = []

    with settings(abort_exception=ValueError):
        for user in users:
            try:
                if not local("id -u {}".format(user), capture=True):
                    to_add.append(user)
            except:
                pass

    for user in to_add:
        local("adduser {}".format(user))


def install_common():
    Apt.upgrade()
    Apt.install(*DEPLOYMENT_PACKAGES)


def install_nginx():
    Apt.install('nginx')
    assert lexists('/etc/nginx/sites-enabled')
    if lexists('/etc/nginx/sites-enabled/default'):
        local("sudo rm /etc/nginx/sites-enabled/default")


def restart_nginx():
    local('sudo /etc/init.d/nginx restart')


def install_postgres():
    hba_conf = "/etc/postgresql/{0}/main/pg_hba.conf".format(
        ".".join(str(i) for i in env.pg_version)
    )
    if lexists(hba_conf):
        local("sudo rm {}".format(hba_conf))
    local("sudo cp database/pg_hba.conf {0}".format(hba_conf))
    local("sudo chown postgres:postgres {0}".format(hba_conf))
    Postgres.restart_database()


def create_directory(dir_name):
    if not lexists(dir_name):
        local("mkdir -p {}".format(dir_name))


def make_home_directory():
    if not lexists(env.home_dir):
        local("sudo mkdir -p {}".format(env.home_dir))
    local("sudo chown {0}:{0} {1}".format(env.user, env.home_dir))


def create_log_directory():
    log_dir = os.path.join(env.home_dir, 'log/supervisord')
    create_directory(log_dir)


def create_run_directory():
    run_dir = os.path.join(env.home_dir, 'var/run')
    create_directory(run_dir)

def _restart_app_command():
    return "{0}/bin/supervisorctl -c {1}/etc/supervisord.conf restart all".format(
        env.virtual_env_path, env.project_path
    )

def restart_app():
    local(_restart_app_command())
    
def start_supervisord_or_restart_app():
    local("pgrep supervisord && {2} || {0}/bin/supervisord -c {1}/etc/production.conf".format(
        env.virtual_env_path, env.project_path, _restart_app_command()))

def restart_gunicorn():
    local("{0}/bin/supervisorctl -c {1}/etc/supervisord.conf restart gunicorn".format(
        env.virtual_env_path, env.project_path
    )
)
