from django_helper import Django
from env_setup import setup_fav_env
import deployment
import setup_server


def deploy():
    setup_fav_env()
    deployment.create_env()
    Django.create_local_settings()


def django_deploy():
    setup_fav_env()
    Django.create_local_settings()
    Django.migrate()
    Django.load_lookup_lists()
    Django.collect_static()


def server_setup():
    setup_fav_env()
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


def restart_nginx():
    setup_fav_env()
    setup_server.restart_nginx()


def restart_everything():
    setup_fav_env()
    setup_server.restart_app()
    setup_server.restart_nginx()


def start_supervisord():
    setup_fav_env()
    setup_server.start_supervisord_or_restart_app()


def symlink_upstart():
    setup_fav_env()
    deployment.symlink_upstart()
