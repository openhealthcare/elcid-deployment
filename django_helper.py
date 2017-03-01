import os
from jinja2 import Environment, FileSystemLoader
from fabric.api import local, env
from fabric.context_managers import lcd
from fabric.operations import prompt
from common import lexists


TEMPLATE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "django")
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def run_management_command(some_command):
    with lcd(env.project_path):
        cmd = "{0}/bin/python manage.py {1}".format(
            env.virtual_env_path, some_command
        )
        local(cmd)


class Django(object):

    @classmethod
    def migrate(cls):
        run_management_command("migrate")

    @classmethod
    def load_lookup_lists(cls):
        run_management_command(
            "load_lookup_lists -f data/lookuplists/lookuplists.json"
        )

    @classmethod
    def collect_static(cls):
        run_management_command(
            "collectstatic --noinput"
        )

    @classmethod
    def create_local_settings(cls):
        env_values = {
            "db_name": env.db_name,
            "app_user": env.app_owner,
            "app_password": env.app_password
        }
        template = jinja_env.get_template('production_settings.py.jinja2')
        output = template.render(env_values)
        module_name = env.app_name
        if env.settings_module_name:
            module_name = env.settings_module_name
        local_settings_file = '{0}/{1}/local_settings.py'.format(env.project_path, module_name)

        if not lexists(local_settings_file):
            with open(local_settings_file, 'w+') as f:
                f.write(output)

    @classmethod
    def create_gunicorn_settings(cls):

        local_gunicorn = '{0}/etc/gunicorn.conf'.format(env.project_path)
        gunicorn_conf_exists = lexists(local_gunicorn)
        if gunicorn_conf_exists:
            result = prompt(
                'Local gunicorn exists, remove? (Y or N)',
                default="Y",
                validate=lambda x: x.upper() == "Y" or x.upper() == "N"
            )
            gunicorn_conf_exists = result == "N"

        if gunicorn_conf_exists:
            return

        env_values = {
            "env_name": env.virtual_env_path
        }
        template = jinja_env.get_template('gunicorn.conf.jinja2')
        output = template.render(env_values)

        with open(local_gunicorn, 'w') as f:
            f.write(output)

    @classmethod
    def deployment_tasks(cls):
        cls.create_local_settings()
        cls.migrate()
        cls.load_lookup_lists()
        cls.collect_static()
