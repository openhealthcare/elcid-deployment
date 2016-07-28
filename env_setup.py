import os
from fabric.api import env
from deployment import get_release_name
from variables import PROJECTS


def setup_env(project_name, branch_name):
    env.project_name = project_name
    env.branch_name = branch_name
    env.release_name = get_release_name()
    env.github_url = PROJECTS[env.project_name]
    env.database_owner = "postgres"
    env.home_dir = os.path.abspath("../deployment_test")
    env.project_path = os.path.join(env.home_dir, env.release_name)
    env.app_owner = "ohc"
    env.app_password = "this is fake"
    env.db_name = env.release_name.replace("-", "").replace(".", "")
    env.app_name = env.project_name

    # not set up to begin with created by common.create_virtual_env
    env.virtual_env_path = "/home/{0}/.virtualenvs/{1}".format(
        env.app_owner, env.release_name
    )
    env.pg_version = (9, 3)
