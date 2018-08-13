from crontab import CronTab
from fabric.api import env
from common import lexists
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Cron(object):
    @classmethod
    def get_comment(cls):
        return "{} back up".format(env.app_name)

    @classmethod
    def setup_backup(cls):
        # currently using root, not nice but we su into postgres
        fabric_virtual_env = "cd {0} && /home/{1}/.virtualenvs/elcid-setup/bin/fab"
        fabric_virtual_env = fabric_virtual_env.format(BASE_DIR, env.nix_user)
        comment = cls.get_comment()
        crontab = CronTab(user=True)
        crontab.remove_all(comment=comment)
        command = "{} database_backup".format(fabric_virtual_env)
        job = crontab.new(command=command, comment=comment)

        # run every day
        job.every().dom()
        crontab.write()
