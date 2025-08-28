from jira import JIRA
from flask import current_app

class JiraService:
    def __init__(self):
        self.jira = JIRA(
            server=current_app.config['JIRA_SERVER'],
            basic_auth=(
                current_app.config['JIRA_USERNAME'],
                current_app.config['JIRA_PASSWORD']
            )
        )
        self.project = current_app.config['JIRA_PROJECT']

    def create_issue(self, summary, description, issue_type='Task'):
        """
        Создает новую задачу в Jira
        """
        try:
            issue_dict = {
                'project': self.project,
                'summary': summary,
                'description': description,
                'issuetype': {'name': issue_type},
            }
            issue = self.jira.create_issue(fields=issue_dict)
            return issue.key
        except Exception as e:
            current_app.logger.error(f"Jira error: {str(e)}")
            raise

    def add_comment(self, issue_key, comment):
        """
        Добавляет комментарий к задаче
        """
        try:
            self.jira.add_comment(issue_key, comment)
        except Exception as e:
            current_app.logger.error(f"Jira error: {str(e)}")
            raise

    def update_status(self, issue_key, status_name):
        """
        Обновляет статус задачи
        """
        try:
            issue = self.jira.issue(issue_key)
            transitions = self.jira.transitions(issue)
            
            # Находим ID перехода для нужного статуса
            transition_id = None
            for t in transitions:
                if t['name'].lower() == status_name.lower():
                    transition_id = t['id']
                    break
            
            if transition_id:
                self.jira.transition_issue(issue, transition_id)
            else:
                raise ValueError(f"Status transition '{status_name}' not found")
        except Exception as e:
            current_app.logger.error(f"Jira error: {str(e)}")
            raise
