from django_helper import Django, run_management_command
from env_setup import setup_fab_env
from fabric.api import env, local
import deployment
import setup_server
from common import Git
from pip_helper import Pip
from postgres_helper import Postgres
from fabric.operations import put
from cron import Cron
from fabric.context_managers import lcd
from deployment import symlink_nginx, symlink_upstart


def dump_db():
    setup_fab_env()


def setup_cron():
    setup_fab_env()
    Cron.setup_backup()


def deploy_test():
    setup_fab_env()
    Pip.create_virtual_env()
    Git.checkout_branch()
    Pip.set_project_directory()
    with lcd(env.project_path):
        Pip.install_requirements()
    symlink_nginx()
    Postgres.create_user_and_database()
    symlink_upstart()
    Django.create_local_settings()
    if not env.db_dump_dir:
        print "no dump directory provided, not loading in any existing data"
    else:
        Postgres.load_data()
    Django.migrate()
    Django.collect_static()
    Django.create_gunicorn_settings()
    Django.create_celery_settings()
    setup_server.restart_app()
    setup_server.restart_nginx()


def deploy_prod():
    setup_fab_env()
    deployment.create_env()
    Django.create_local_settings()
    if not env.db_dump_dir:
        print "no dump directory provided, not loading in any existing data"
    else:
        Postgres.load_data()
    Django.migrate()
    Django.collect_static()
    Django.create_gunicorn_settings()
    Django.create_celery_settings()
    setup_cron()
    setup_server.restart_app()
    setup_server.restart_nginx()


def django_deploy():
    setup_fab_env()
    Django.create_local_settings()
    Django.migrate()
    Django.load_lookup_lists()
    Django.collect_static()


def load_ipfjes_data():
    run_management_command('import_soc_codes')


def server_setup():
    setup_fab_env()
    setup_server.create_users()
    setup_server.install_common()
    setup_server.install_nginx()
    setup_server.make_home_directory()
    setup_server.install_postgres()
    setup_server.create_log_directory()
    setup_server.create_run_directory()
    deployment.create_env()
    setup_fab_env()
    Django.create_local_settings()
    Django.create_gunicorn_settings()
    database_backup()
    Django.migrate()
    Django.load_lookup_lists()
    Django.collect_static()
    # the line below should only be run on the initial load or it will delete foriegn keys
    # load_ipfjes_data()
    setup_server.start_supervisord_or_restart_app()
    setup_server.restart_nginx()
    setup_cron()


def restart_nginx():
    setup_fab_env()
    setup_server.restart_nginx()


def restart_everything():
    setup_fab_env()
    setup_server.restart_app()
    setup_server.restart_nginx()

def start_supervisord():
    setup_fab_env()
    setup_server.start_supervisord_or_restart_app()

def symlink_upstart():
    setup_fab_env()
    deployment.symlink_upstart()

def create_database():
    setup_fab_env()
    Postgres.create_database()


def database_backup():
    setup_fab_env()
    file_dump = Postgres.dump_data()
    file_dump_enc = "{}.enc".format(file_dump)
    command = "openssl smime -encrypt -aes256 -binary -in {1} \
-out {2} -outform DER {0}"
    command = command.format(
        env.pem_key, file_dump, file_dump_enc
    )
    local(command)
    local("mv {0} {1}".format(file_dump_enc, env.out_file))

def postgres(method, *args, **kwargs):
    setup_fab_env()
    result = getattr(Postgres, method)(*args, **kwargs)
    print result
    return result


def pip(method, *args, **kwargs):
    setup_fab_env()
    result = getattr(Pip, method)(*args, **kwargs)
    print result
    return result
