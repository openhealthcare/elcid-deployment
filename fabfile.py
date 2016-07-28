from fabric.api import local, env
from variables import PROJECTS
from deployment import get_release_name, create_virtual_env, remove_virtual_env
from setup import create_user, install_common, install_nginx, restart_ningx


def setup_env(project_name, branch_name):
    existing_requirements = local("pip freeze", capture=True)

    if "virtualenvwrapper" not in existing_requirements:
        raise Exception("Virtual env wrapper not installed")

    env.project_name = project_name
    env.branch_name = branch_name
    env.release_name = get_release_name()
    env.github_url = PROJECTS[env.project_name]
    env.database_owner = "postgres"
    env.home_dir = "../deployment_test"
    env.user = "ohc"


def deploy(project_name, branch_name):
    setup_env(project_name, branch_name)
    create_virtual_env()


def setUp(project_name, branch_name):
    create_user()
    install_common()
    install_nginx()
    restart_ningx()
    deploy(project_name, branch_name)


def remove(project_name, branch_name):
    setup_env(project_name, branch_name)
    remove_virtual_env()
