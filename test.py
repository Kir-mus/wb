from requests import get, post, put, delete

print(get('http://localhost:7000/api/v2/users').json())
print(get('http://localhost:7000/api/v2/users/6').json())
print(get('http://localhost:7000/api/v2/users/600').json())   # USER 600 not found

print(post('http://localhost:5000/api/v2/users').json())
print(post("http://localhost:5000/api/v2/users", json={'name': 'Ева'}).json())

print(post("http://localhost:5000/api/v2/users", json={'name': 'Витя',
                                                       'position': 'Повор',
                                                       'surname': 'Сюрафов',
                                                       'age': 20, 'address': 'module_2',
                                                       'speciality': 'Нейрокухня',
                                                       'hashed_password': 'морковка228',
                                                       'email': 'vitatop@mail.ru'}).json())

print(delete('http://localhost:5000/api/v2/users/6').json())
print(delete('http://localhost:5000/api/v2/users/600').json())





