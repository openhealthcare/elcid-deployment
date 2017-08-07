from fabric.api import local, env, settings, hide
from fabric.contrib.files import _expand_path
from fabric.context_managers import lcd


def lexists(path):
    with settings(hide('everything'), warn_only=True):
        return not local('test -e {}'.format(_expand_path(path))).failed


class Git(object):
    @classmethod
    def checkout_branch(cls):
        with lcd(env.home_dir):
            if not lexists(env.release_name):
                local("git clone {0} {1}".format(env.github_url, env.release_name))
            with lcd(env.release_name):
                local("git fetch")
                local("git checkout {0}".format(env.branch_name))
                local("git pull origin {}".format(env.branch_name))

    @classmethod
    def remove_code_dir(cls):
        with lcd(env.home_dir):
            local("rm -rf {}".format(env.release_name))
