"""
Setup environment by reading configuration variables
"""
import os
import ConfigParser

from fabric.api import env

from deployment import get_release_name

def setup_env():
    config = ConfigParser.RawConfigParser()
    config.read(os.environ.get('ELCID_ENV', 'settings.ini'))
    env.project_name = config.get('project', 'name')
    env.branch_name = config.get('project', 'branch')
    env.release_name = get_release_name()
    github_user = config.get('project', 'github_user')
    env.github_url = "https://github.com/{0}/{1}.git".format(
        env.project_name, github_user
    )
    env.database_owner = config.get('db', 'os_user')
    env.home_dir = os.path.abspath(config.get('system', 'base_dir'))
    env.project_path = os.path.join(env.home_dir, env.release_name)
    env.app_owner = config.get('db', 'db_username')
    env.app_password = config.get('db', 'db_password')
    env.db_name = env.release_name.replace("-", "").replace(".", "")
    env.app_name = env.project_name

    # not set up to begin with created by common.create_virtual_env
    env.virtual_env_path = "/home/{0}/.virtualenvs/{1}".format(
        env.app_owner, env.release_name
    )
    env.pg_version = (9, 3)
