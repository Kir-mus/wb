from flask import jsonify, Blueprint, make_response, request, Flask
from data import db_session
import json
from data.users import User
from data.jobs import Jobs


blueprint = Blueprint('jobs_api', __name__,
                      template_folder='templates')


@blueprint.route('/api/users')
def get_jobs():
    session = db_session.create_session()
    user = session.query(Jobs).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address',
                                    'email', 'modified_date'))
                 for item in user]
        }
    )


@blueprint.route('/api/users/<int:user_id>')
def get_one_user(user_id):
    session = db_session.create_session()
    for u in session.query(User).filter(User.id == user_id):
        return jsonify(
            {
                user_id:
                    [item.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address',
                                        'email', 'modified_date'))
                     for item in session.query(Jobs).filter(Jobs.id == user_id)]
            }
        )
    else:
        return jsonify({'error': 'not true id'})


@blueprint.route('/api/users', methods=['POST'])
def add_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    if session.query(User).filter(User.id == request.json['id']).first():
        return jsonify({'error': ' Id already exists'})
    user = User(
        id=request.json['id'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email']
    )
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_news(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': '404'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def create_user(users_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    session = db_session.create_session()
    user = session.query(User).get(users_id)
    if not user:
        return jsonify({'error': '404'})
    user.surname = request.json['surname']
    user.name = request.json['name']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.email = request.json['email']
    session.commit()
    return jsonify({'success': 'OK'})
