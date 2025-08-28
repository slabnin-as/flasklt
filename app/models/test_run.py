from datetime import datetime
from app import db

class TestRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    jenkins_job = db.Column(db.String(128))
    jenkins_build_number = db.Column(db.Integer)
    jira_issue = db.Column(db.String(32))
    status = db.Column(db.String(32), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'jenkins_job': self.jenkins_job,
            'jenkins_build_number': self.jenkins_build_number,
            'jira_issue': self.jira_issue,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def update_status(self, status):
        self.status = status
        self.updated_at = datetime.utcnow()
        db.session.commit()