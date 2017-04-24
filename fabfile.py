from django_helper import Django, run_management_command
from env_setup import setup_fab_env
from fabric.api import env, local
import deployment
import setup_server
from common import Git, Pip
from postgres_helper import Postgres
from fabric.operations import put
from cron import Cron

def dump_db():
    setup_fab_env()

def setup_cron():
    setup_fab_env()
    Cron.setup_backup()

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
    load_ipfjes_data()
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

def database_backup():
    setup_fab_env()
    Postgres.dump_data()
    command = " openssl smime -encrypt -binary -aes-256-cbc -in {1} \
-out {2} -outform DER {0}"
    command = command.format(
        env.pem_key, Postgres.get_recent_database_dump_path(), env.out_file
    )
    local(command)
    local("mv {0} {1}".format(env.out_file, env.other_dir))
