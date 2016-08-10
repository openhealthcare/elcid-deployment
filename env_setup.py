"""
Setup environment by reading configuration variables
"""
import os
import ConfigParser

from fabric.api import env

from deployment import get_release_name

config = ConfigParser.RawConfigParser()
config.read(os.environ.get('ELCID_ENV', 'settings.ini'))


def get(section, option, default=None):
    try:
        return env.http_proxy = config.get(section, option)
    except ConfigParser.NoOptionError:
        print 'No option for', section, option
        return default
    except ConfigParser.NoSectionError:
        print 'No section for', section, option
        return default

def setup_env():
    env.project_name = get('project', 'name')
    env.branch_name = get('project', 'branch')
    env.release_name = get_release_name()
    github_user = get('project', 'github_user')
    env.github_url = "https://github.com/{0}/{1}.git".format(
        github_user, env.project_name,
    )
    env.database_owner = get('db', 'os_user')
    env.home_dir = os.path.abspath(get('system', 'base_dir'))
    env.project_path = os.path.join(env.home_dir, env.release_name)
    env.app_owner = get('db', 'db_username')
    env.app_password = get('db', 'db_password')
    env.db_name = env.release_name.replace("-", "").replace(".", "")
    env.app_name = env.project_name
    env.http_proxy = get('system', 'http_proxy')
    # not set up to begin with created by common.create_virtual_env
    env.virtual_env_path = "/home/{0}/.virtualenvs/{1}".format(
        env.app_owner, env.release_name
    )
    env.pg_version = (9, 3)
