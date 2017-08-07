from crontab import CronTab
from fabric.api import env
from common import lexists
import os
import stat


class Cron(object):
    @classmethod
    def get_comment(cls):
        return "{} back up".format(env.app_name)

    @classmethod
    def setup_backup(cls):
        # currently using root, not nice but we su into postgres
        lexists(os.path)
        curr_dir = os.path.realpath(os.path.dirname(__file__))
        backup_script = os.path.join(curr_dir, "database_backup.sh")
        if not os.path.isfile(backup_script):
            raise ValueError(
                "Unable to find the file {}".format(backup_script)
            )

        os.chmod(backup_script, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)

        if not os.access(backup_script, os.X_OK):
            raise ValueError(
                "Unable to execute {}".format(backup_script)
            )

        comment = cls.get_comment()
        crontab = CronTab(user=True)
        crontab.remove_all(comment=comment)
        job = crontab.new(command=backup_script, comment=comment)

        # run every day
        job.every().dom()
        crontab.write()
