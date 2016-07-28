from django_helper import Django
from env_setup import setup_env
import deployment
import setup_server


def deploy(project_name, branch_name):
    setup_env(project_name, branch_name)
    deployment.create_env()


def server_setup(project_name, branch_name):
    setup_env(project_name, branch_name)
    setup_server.create_users()
    setup_server.install_common()
    setup_server.install_nginx()
    setup_server.make_home_directory()
    setup_server.install_postgres()
    setup_server.create_log_directory()
    setup_server.create_run_directory()
    deploy(project_name, branch_name)
    Django.deployment_tasks()
    setup_server.start_supervisord()
    setup_server.restart_nginx()


def django_deploy(project_name, branch_name):
    setup_env(project_name, branch_name)
    Django.deployment_tasks()


def restart_nginx(project_name, branch_name):
    setup_env(project_name, branch_name)
    setup_server.restart_nginx()


def restart_everything(project_name, branch_name):
    setup_env(project_name, branch_name)
    setup_server.restart_gunicorn()
    setup_server.restart_nginx()


def start_supervisord(project_name, branch_name):
    setup_env(project_name, branch_name)
    setup_server.start_supervisord()


def symlink_upstart(project_name, branch_name):
    setup_env(project_name, branch_name)
    deployment.symlink_upstart()
