from fabric.api import local, env
from fabric.contrib.files import exists


class Apt(object):
    @staticmethod
    def install(*pkgs):
        local('apt-get install -y %s' % ' '.join(pkgs))

    @staticmethod
    def upgrade():
        local('apt-get update -y')
        local('apt-get upgrade -y')


DEPLOYMENT_PACKAGES = [
    # Database
    "postgresql",
    "libq-dev",
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

    # Dev tools
    "git",
    "rake",
    "nodejs",
]


def create_user():
    local("adduser {}".format(env.user))
    local("adduser {}".format(env.database_owner))


def install_common():
    Apt.upgrade()
    for deployment_package in DEPLOYMENT_PACKAGES:
        Apt.install("apt-get install {}".deployment_package)


def install_nginx():
    Apt.install('nginx')
    assert exists('/etc/nginx/sites-enabled')
    if exists('/etc/nginx/sites-enabled/default'):
        local("rm /etc/nginx/sites-enabled/default")


def restart_nginx():
    local('/etc/init.d/nginx restart')


def make_home_directory():
    local("mkdir -p {}".format(env.home_dir))
