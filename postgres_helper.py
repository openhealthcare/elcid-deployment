from fabric.api import local, env
from fabric.contrib.console import confirm
import os
import datetime

PREFACE = "sudo -u postgres psql --command"


class Postgres(object):
    @classmethod
    def database_cmd(cls, command, capture=False):
        """ Runs a database command via the command line
        """
        return local('{0} "{1}"'.format(PREFACE, command), capture=capture)

    @classmethod
    def create_database(cls):
        """ creates a database and user if they don't already exist.
            the db_name is created from the release name
        """
        database_exists = "1" in local(
            "sudo -u postgres psql -l | grep '{}' | wc -l".format(env.db_name),
            capture=True
        )

        if not database_exists:
            cls.database_cmd("CREATE DATABASE {0}".format(env.db_name))
            cls.database_cmd("GRANT ALL PRIVILEGES ON DATABASE {0} TO {1}".format(
                env.db_name, env.app_owner
            ))

    @classmethod
    def create_user(cls):
        """ the user is creates a user if it doesn't exist
            the user name is taken from settings.db.db_name
        """
        user_exists = 'found' in cls.database_cmd(
            "SELECT 'found' FROM pg_roles WHERE rolname='{}'".format(env.app_owner),
            capture=True
        )

        if not user_exists:
            cls.database_cmd("CREATE USER {}".format(env.app_owner))
            cls.database_cmd("ALTER USER {0} WITH PASSWORD {1}".format(
                env.app_owner, env.app_password
            ))

    @classmethod
    def restart_database(cls):
        if env.pg_version < (9, 0):
            local('sudo /etc/init.d/postgresql-8.4 restart || /etc/init.d/postgresql-8.4 start')
        else:
            local('sudo /etc/init.d/postgresql restart || /etc/init.d/postgresql start')

    @classmethod
    def drop_database(cls):
        cls.database_cmd("DROP DATABASE {0}".format(env.db_name))

    @classmethod
    def create_user_and_database(cls):
        cls.create_user()
        cls.create_database()

    @classmethod
    def get_dump_name(cls, dt=None):
        if not dt:
            dt = datetime.datetime.now()
        str_dt = dt.strftime("%d.%m.%y")
        return "back.sql.{}".format(str_dt)

    @classmethod
    def extract_date_from_dump_name(cls, dump_name):
        if "back.sql." not in dump_name:
            raise "incorrect date format, we expect back.sql.%d.%m.%y"
        expected_str_format = "back.sql.%d.%m.%y"
        return datetime.datetime.strptime(dump_name, expected_str_format)

    @classmethod
    def refresh_database(cls):
        user_confirm = """This will drop the database {0} and restore it from"
        {1} are you sure you wish to continue?
        """
        user_confirm = user_confirm.format(
            env.db_name, cls.get_recent_database_dump_path()
        )
        confirmed = confirm(user_confirm, default=False)

        if confirmed:
            cls.drop_database()
            cls.create_database()
            cls.load_data()

    @classmethod
    def get_recent_database_dump_path(cls):
        dumps = local("ls {}".format(env.db_dump_dir), capture=True)
        dumps = dumps.splitlines()
        dumps = [dump for dump in dumps if dump.startswith("back.sql")]
        date_to_dump = (
            cls.extract_date_from_dump_name(dump) for dump in dumps
        )
        latest = sorted(date_to_dump)[-1]
        dump_name = cls.get_dump_name(latest)
        return os.path.join(
            env.db_dump_dir, dump_name
        )

    @classmethod
    def load_data(cls):
        full_file_name = cls.get_recent_database_dump_path()
        load_str = "sudo -u postgres psql -d {0} -f {1}".format(
            env.db_name,
            full_file_name
        )
        local(load_str)

    @classmethod
    def dump_data(cls):
        # presumes you've set up your ~/.pgpass
        full_file_name = os.path.join(env.db_dump_dir, cls.get_dump_name())
        dump_str = "pg_dump -d {0} -U {1} > {2}"
        local(dump_str.format(env.db_name, env.app_owner, full_file_name))
        return full_file_name
