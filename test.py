from requests import get, post, put, delete

print(get('http://localhost:7000/api/v2/jobs').json())
print(get('http://localhost:7000/api/v2/jobs/2').json())
print(get('http://localhost:7000/api/v2/jobs/600').json())   # jobs 600 not found

print(post('http://localhost:5000/api/v2/jobs').json())
print(post("http://localhost:5000/api/v2/jobs", json={'team_leader': 2}).json())

print(post("http://localhost:5000/api/v2/jobs", json={'team_leader': 2,
                                                      'job': 'Работа на кухне(жарко)',
                                                      'work_size': '23',
                                                      'collaborators': '1, 2, 3',
                                                      'is_finished': True
                                                      }).json())

print(delete('http://localhost:5000/api/v2/jobs/1').json())
print(delete('http://localhost:5000/api/v2/jobs/600').json())





