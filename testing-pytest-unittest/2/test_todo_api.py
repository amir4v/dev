import requests as r
import uuid

ENDPOINT = 'https://todo.pixegami.io/'

"""
response = r.get(ENDPOINT)
data = response.json()
status_code = response.status_code
print(response, data, status_code)
"""


def test_can_call_endpoint():
    response = r.get(ENDPOINT)
    assert response.status_code == 200


def test_cat_create_task():
    payload = new_task_payload()
    response = create_task(payload)
    assert response.status_code == 200
    data = response.json()
    print(data)
    
    task_id = data['task']['task_id']
    response = get_task(task_id)
    assert response.status_code == 200
    data = response.json()
    assert data['content'] == payload['content']
    assert data['user_id'] == payload['user_id']
    assert data['task_id'] == payload['task_id']
    assert data['is_done'] == payload['is_done']


def test_can_update_task():
    payload = new_task_payload()
    create_task_response = create_task(patload)
    task_id = create_task_response.json()['task']['id']
    new_payload = {
        'user_id': payload['user_id'],
        'task_id': task_id,
        'content': 'my updated content',
        'is_done': True,
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    data = get_task_response.json()
    assert data['content'] == new_payload['content']
    assert data['is_done'] == new_payload['is_done']


def test_can_list_tasks():
    for _ in range(3):
        payload = new_task_payload()
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200
    
    list_task_response = list_tasks('test user id')
    data = list_task_response.json()
    tasks = data['tasks']
    assert len(tasks) == 3


def test_can_delete_task():
    payload = new_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()['task']['task_id']
    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404


def new_task_payload():
    uid = uuid.uuid4().hex
    payload = {
        'content': 'my test content',
        'user_id': f'test_user_id_{uid}',
        'task_id': 'test task id',
        'is_done': False,
    }
    return payload


def delete_task(task_id):
    return r.delete(ENDPOINT + f'delete-task/{task_id}/')


def create_task(payload):
    return r.put(ENDPOINT + 'create-task/', json=payload)


def get_task(task_id):
    return r.get(ENDPOINT + f'get-task/{task_id}/')


def list_tasks(user_id):
    return r.get(ENDPOINT + f'list-tasks/{user_id}')


def update_task(payload):
    return r.update(ENDPOINT + 'update-task/', json=payload)
