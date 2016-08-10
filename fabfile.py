from django_helper import Django
from env_setup import setup_env
import deployment
import setup_server


def deploy():
    setup_env()
    deployment.create_env()


def server_setup():
    setup_env()
    setup_server.create_users()
    setup_server.install_common()
    setup_server.install_nginx()
    setup_server.make_home_directory()
    setup_server.install_postgres()
    setup_server.create_log_directory()
    setup_server.create_run_directory()
    deploy()
    Django.deployment_tasks()
    setup_server.start_supervisord()
    setup_server.restart_nginx()


def django_deploy():
    setup_env()
    Django.deployment_tasks()


def restart_nginx():
    setup_env()
    setup_server.restart_nginx()


def restart_everything():
    setup_env()
    setup_server.restart_gunicorn()
    setup_server.restart_nginx()


def start_supervisord():
    setup_env()
    setup_server.start_supervisord()


def symlink_upstart():
    setup_env()
    deployment.symlink_upstart()
