from fabric.api import local, env
import os
import datetime

PREFACE = "sudo -u postgres psql --command"


class Postgres(object):
    @classmethod
    def database_cmd(cls, command, capture=False):
        return local('{0} "{1}"'.format(PREFACE, command), capture=capture)

    @classmethod
    def create_database(cls):
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
    def restart_database():
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
    def get_dump_name(cls, now=None):
        if not now:
            now = datetime.datetime.now()
        var_now = now.strftime("%d.%m.%y")
        return "back.sql.{}".format(var_now)

    @classmethod
    def extract_date_from_dump_name(cls, dump_name):
        if "back.sql." not in dump_name:
            raise "incorrect date format, we expect back.sql.%d.%m.%y"
        expected_str_format = "back.sql.%d.%m.%y"
        return datetime.datetime.strptime(dump_name, expected_str_format)

    @classmethod
    def get_most_recent_database_dump(cls):
        dumps = local("ls {}".format(env.db_dump_dir), capture=True)
        dumps = dumps.splitlines()
        dumps = [dump for dump in dumps if dump.startswith("back.sql")]
        date_to_dump = (
            cls.extract_date_from_dump_name(dump) for dump in dumps
        )
        latest = sorted(date_to_dump)[-1]
        return cls.get_dump_name(latest)

    @classmethod
    def load_data(cls):
        full_file_name = os.path.join(
            env.db_dump_dir, cls.get_most_recent_database_dump()
        )
        load_str = "sudo -u postgres psql -d {0} -f {1}".format(
            env.db_name,
            full_file_name
        )
        local(load_str)
