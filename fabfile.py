from django_helper import Django
from env_setup import setup_fab_env
import deployment
import setup_server
from common import Git, Pip
from postgres_helper import Postgres


def deploy():
    setup_fab_env()
    deployment.create_env()
    Django.create_local_settings()


def django_deploy():
    setup_fab_env()
    Django.create_local_settings()
    Django.migrate()
    Django.load_lookup_lists()
    Django.collect_static()


def server_setup():
    setup_fab_env()
    setup_server.create_users()
    setup_server.install_common()
    setup_server.install_nginx()
    setup_server.make_home_directory()
    setup_server.install_postgres()
    setup_server.create_log_directory()
    setup_server.create_run_directory()
    deployment.create_env()
    django_deploy()
    setup_server.start_supervisord_or_restart_app()
    setup_server.restart_nginx()


def delete_environment():
    Postgres.drop_database()
    Pip.remove_virtualenv()
    Git.remove_code_dir()


def restart_nginx():
    setup_fab_env()
    setup_server.restart_nginx()


def restart_everything():
    setup_fab_env()
    setup_server.restart_app()
    setup_server.restart_nginx()


def start_supervisord():
    setup_fab_env()
    setup_server.start_supervisord_or_restart_app()


def symlink_upstart():
    setup_fab_env()
    deployment.symlink_upstart()
