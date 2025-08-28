import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(os.path.dirname(basedir), '.env'))

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Jenkins configuration
    JENKINS_URL = os.environ.get('JENKINS_URL')
    JENKINS_USERNAME = os.environ.get('JENKINS_USERNAME')
    JENKINS_PASSWORD = os.environ.get('JENKINS_PASSWORD')
    
    # Jira configuration
    JIRA_SERVER = os.environ.get('JIRA_SERVER')
    JIRA_USERNAME = os.environ.get('JIRA_USERNAME')
    JIRA_PASSWORD = os.environ.get('JIRA_PASSWORD')
    JIRA_PROJECT = os.environ.get('JIRA_PROJECT')
