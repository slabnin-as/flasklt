import jenkins
from flask import current_app

class JenkinsService:
    def __init__(self):
        self.server = jenkins.Jenkins(
            current_app.config['JENKINS_URL'],
            username=current_app.config['JENKINS_USERNAME'],
            password=current_app.config['JENKINS_PASSWORD']
        )

    def start_job(self, job_name, parameters=None):
        """
        Запускает задачу Jenkins с указанными параметрами
        """
        try:
            next_build_number = self.server.get_job_info(job_name)['nextBuildNumber']
            self.server.build_job(job_name, parameters=parameters)
            return next_build_number
        except jenkins.JenkinsException as e:
            current_app.logger.error(f"Jenkins error: {str(e)}")
            raise

    def get_build_status(self, job_name, build_number):
        """
        Получает статус сборки
        """
        try:
            build_info = self.server.get_build_info(job_name, build_number)
            return {
                'status': build_info['result'],
                'url': build_info['url']
            }
        except jenkins.JenkinsException as e:
            current_app.logger.error(f"Jenkins error: {str(e)}")
            raise

    def is_job_running(self, job_name, build_number):
        """
        Проверяет, выполняется ли сборка в данный момент
        """
        try:
            build_info = self.server.get_build_info(job_name, build_number)
            return build_info['building']
        except jenkins.JenkinsException as e:
            current_app.logger.error(f"Jenkins error: {str(e)}")
            raise
