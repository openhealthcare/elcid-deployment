from fabric.api import local, env, settings
from common import lexists, restart_database


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
    "python-psycopg2",

    # Python Dev
    "python-dev",
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
    local('/etc/init.d/nginx restart')


def install_postgres():
    hba_conf = "/etc/postgresql/{0}/main/pg_hba.conf".format(
        ".".join(str(i) for i in env.pg_version)
    )
    if lexists(hba_conf):
        local("sudo rm {}".format(hba_conf))
    local("sudo cp database/pg_hba.conf {0}".format(hba_conf))
    local("sudo chown postgres:postgres {0}".format(hba_conf))
    restart_database()


def create_directory(dir_name):
    if not lexists(dir_name):
        local("mkdir -p {}".format(dir_name))


def make_home_directory():
    if not lexists(env.home_dir):
        local("sudo mkdir -p {}".format(env.home_dir))
        local("sudo chown ohc:ohc {0}".format(env.home_dir))


def create_log_directory():
    log_dir = "/usr/local/ohc/log/supervisord"
    create_directory(log_dir)


def create_run_directory():
    run_dir = "/usr/local/ohc/var/run/"
    create_directory(run_dir)


def start_supervisord():
    local("{0}/bin/supervisord -c {1}/etc/production.conf".format(env.virtual_env_path, env.project_path))


def restart_gunicorn():
    local("{0}/bin/supervisorctl -c {1}/etc/production.conf restart gunicorn".format(
        env.virtual_env_path, env.project_path
    ))
