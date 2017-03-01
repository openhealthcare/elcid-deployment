from fabric.api import local, env, settings, hide
from fabric.contrib.files import _expand_path
from fabric.context_managers import lcd


def lexists(path):
    with settings(hide('everything'), warn_only=True):
        return not local('test -e {}'.format(_expand_path(path))).failed


class Pip(object):
    @classmethod
    def get_pip(cls):
        return "{}/bin/pip".format(
            env.virtual_env_path
        )

    @classmethod
    def install_virtualenv(cls):
        local("pip install virtualenv")

    @classmethod
    def create_virtual_env(cls):
        cls.install_virtualenv()
        if not lexists(env.virtual_env_path):
            local("/usr/local/bin/virtualenv {0}".format(env.virtual_env_path))

    @classmethod
    def remove_virtualenv(cls):
        local("rm -rf /usr/bin/virtualenv/{}".format(env.project_name))

    @classmethod
    def set_project_directory(cls):
        local("echo '{0}' > {1}/.project".format(
            env.project_path, env.virtual_env_path
        ))

    @classmethod
    def install(cls, *pkgs):
        pip = cls.get_pip()
        for pkg in pkgs:
            if env.http_proxy:
                local('{0} install -U {1}'.format(pip, pkg))
            else:
                local('{0} install --proxy {2} -U {1}'.format(pip, pkg, env.http_proxy))

    @classmethod
    def install_requirements(cls):
        if env.http_proxy:
            local("{0} install -r requirements.txt --proxy {1}".format(
                cls.get_pip(), env.http_proxy
            ))
        else:
            local("{0} install -r requirements.txt".format(cls.get_pip()))


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
