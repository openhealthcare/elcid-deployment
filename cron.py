from crontab import CronTab
from fabric.api import env
from common import lexists


class Cron(object):
    @classmethod
    def get_comment(cls):
        return "{} back up".format(env.app_name)

    @classmethod
    def setup_backup(cls):
        # currently using root, not nice but we su into postgres
        fabric_virtual_env = "/home/{0}/.virtualenvs/elcid-setup/bin/fab"
        fabric_virtual_env = fabric_virtual_env.format(env.app_owner)
        comment = cls.get_comment()
        crontab = CronTab(user=True)
        crontab.remove_all(comment=comment)
        if not lexists(fabric_virtual_env):
            err = "Unable to find our virtual env for the contrab {}"
            err.format(fabric_virtual_env)
            raise err
        command = "{} database_backup".format(fabric_virtual_env)
        job = crontab.new(command=command, comment=comment)

        # run every day
        job.every().dom()
        crontab.write()
