from flask import jsonify, Blueprint, make_response, request, Flask
from data import db_session
import json
from data.users import User
from data.jobs import Jobs


blueprint = Blueprint('jobs_api', __name__,
                      template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    job = session.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date',
                                    'is_finished', 'user.name'))
                 for item in job]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>')
def get_one_jobs(job_id):
    session = db_session.create_session()
    for j in session.query(Jobs).filter(Jobs.id == job_id):
        return jsonify(
            {
                job_id:
                    [item.to_dict(only=('team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date',
                                        'is_finished', 'user.name'))
                     for item in session.query(Jobs).filter(Jobs.id == job_id)]
            }
        )
    else:
        return jsonify({'error': 'not true id'})


@blueprint.route('/api/jobs', methods=['POST'])
def add_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    if session.query(Jobs).filter(Jobs.id == request.json['id']).first():
        return jsonify({'error': ' Id already exists'})

    job = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    session.add(job)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_news(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': '404'})
    session.delete(job)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def create_job(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': '404'})
    job.team_leader = request.json['team_leader']
    job.job = request.json['job']
    job.work_size = request.json['work_size']
    job.collaborators = request.json['collaborators']
    job.is_finished = request.json['is_finished']
    session.commit()
    return jsonify({'success': 'OK'})



