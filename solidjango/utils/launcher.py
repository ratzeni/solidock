import subprocess
import shlex

from utils.logging import Logging


class Launcher(object):
    def __init__(self, loglevel='INFO'):
        self.logger = Logging(self.__class__.__name__, level=loglevel).get_logger()

    def create_profile(self, pipeline, profile):
        params = dict(pipeline=pipeline,
                      profile=profile)
        cmd = self.__get_cmd(self.create_profile.__name__, params)
        self.__run(cmd=cmd)

    def deploy_project(self, pipeline, profile, host, user, connection):
        params = dict(pipeline=pipeline,
                      profile=profile,
                      host=host,
                      user=user,
                      connection=connection)
        cmd = self.__get_cmd(self.deploy_project.__name__, params)
        self.__run(cmd=cmd)

    def __get_cmd(self, cmd, params):
        cmds = dict(
            create_profile=["solida setup",
                            "-l {}".format(params.get('pipeline')),
                            "-p {}".format(params.get('profile')),
                            "--create-profile"],

            deploy_project=["solida setup",
                            "-l {}".format(params.get('pipeline')),
                            "-p {}".format(params.get('profile')),
                            "--deploy",
                            "--host {}".format(params.get('host')),
                            "--remote-user {}".format(params.get('user')),
                            "--connection {}".format(params.get('connection'))],

        )

        return cmds.get(cmd)

    def __run(self, cmd):
        try:
            # subprocess.check_output(cmd)
            cmd = shlex.split(' '.join(cmd))
            process = subprocess.Popen(cmd,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
            output = process.communicate()[0]
            ret = process.wait()
            return True

        except subprocess.CalledProcessError as e:
            self.logger.info(e)
            if e.output:
                self.logger.info("command output: %s", e.output)
            else:
                self.logger.info("no command output available")
            return False
