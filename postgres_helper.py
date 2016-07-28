from fabric.api import local, env

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
