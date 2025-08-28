from flask import Blueprint, jsonify, request
from app.services.jira_service import JiraService
from app.services.jenkins_service import JenkinsService
from app.services.db_service import DatabaseService

# Create blueprint with URL prefix
bp = Blueprint('api', __name__, url_prefix='/api')

# Jira related endpoints
@bp.route('/jira/<jira_id>', methods=['GET'])
def get_jira_task(jira_id):
    try:
        jira_service = JiraService()
        issue_data = jira_service.get_issue(jira_id)
        
        return jsonify({
            'status': 'success',
            'data': issue_data
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/jira/<jira_id>/process', methods=['POST'])
def process_jira_task(jira_id):
    try:
        # Get Jira issue data
        jira_service = JiraService()
        issue_data = jira_service.get_issue(jira_id)

        # Save to database
        db_service = DatabaseService()
        task = db_service.get_task_by_jira_id(jira_id)
        
        if task:
            task = db_service.update_task(task, issue_data)
        else:
            task = db_service.create_task(issue_data)

        return jsonify({
            'status': 'success',
            'message': 'Jira task processed successfully',
            'task_id': task.id,
            'jira_id': jira_id
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Jenkins related endpoints
@bp.route('/jenkins/jobs/<job_name>', methods=['POST'])
def trigger_jenkins_job(job_name):
    try:
        parameters = request.json.get('parameters', {})
        jira_id = request.json.get('jira_id')

        jenkins_service = JenkinsService()
        build_number = jenkins_service.trigger_job(job_name, parameters)

        # If jira_id is provided, update the task in database
        if jira_id:
            db_service = DatabaseService()
            task = db_service.get_task_by_jira_id(jira_id)
            if task:
                db_service.update_task(task, {
                    'jenkins_job_name': job_name,
                    'jenkins_build_number': build_number
                })

        return jsonify({
            'status': 'success',
            'message': 'Jenkins job triggered successfully',
            'job_name': job_name,
            'build_number': build_number
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/jenkins/jobs/<job_name>/builds/<int:build_number>', methods=['GET'])
def get_jenkins_build_status(job_name, build_number):
    try:
        jenkins_service = JenkinsService()
        build_info = jenkins_service.get_build_status(job_name, build_number)

        return jsonify({
            'status': 'success',
            'data': build_info
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Combined workflow endpoint
@bp.route('/workflow/jira/<jira_id>/jenkins/<job_name>', methods=['POST'])
def process_complete_workflow(jira_id, job_name):
    try:
        # Get Jira issue data
        jira_service = JiraService()
        issue_data = jira_service.get_issue(jira_id)

        # Save to database
        db_service = DatabaseService()
        task = db_service.get_task_by_jira_id(jira_id)
        
        if task:
            task = db_service.update_task(task, issue_data)
        else:
            task = db_service.create_task(issue_data)

        # Trigger Jenkins job
        jenkins_service = JenkinsService()
        parameters = request.json.get('parameters', {})
        build_number = jenkins_service.trigger_job(job_name, parameters)
        
        # Update task with Jenkins information
        db_service.update_task(task, {
            'jenkins_job_name': job_name,
            'jenkins_build_number': build_number
        })

        return jsonify({
            'status': 'success',
            'message': 'Complete workflow processed successfully',
            'task_id': task.id,
            'jira_id': jira_id,
            'jenkins_job': job_name,
            'build_number': build_number
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
