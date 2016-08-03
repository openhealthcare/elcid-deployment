import os
from fabric.api import env
from deployment import get_release_name
from variables import PROJECTS


def setup_env(project_name, branch_name):
    # Name of the project in the variables.PROJECTS dict
    # Also the name used for the directory to which we deploy
    env.project_name = project_name
    # The target release branch
    env.branch_name = branch_name
    # generated project+branch
    env.release_name = get_release_name()
    # Github URL from variables.PROJECTS
    env.github_url = PROJECTS[env.project_name]
    # OS user we should run database commands as
    env.database_owner = "postgres"
    # Directory to which we should deploy applications 
    # Typically /usr/lib/ohc
    env.home_dir = os.path.abspath("../deployment_test")
    env.project_path = os.path.join(env.home_dir, env.release_name)
    # Database user we would like to use. Created if new
    env.app_owner = "ohc"
    # Password for the database user above
    env.app_password = "this is fake"
    env.db_name = env.release_name.replace("-", "").replace(".", "")
    env.app_name = env.project_name

    # not set up to begin with created by common.create_virtual_env
    env.virtual_env_path = "/home/{0}/.virtualenvs/{1}".format(
        env.app_owner, env.release_name
    )
    env.pg_version = (9, 3)
