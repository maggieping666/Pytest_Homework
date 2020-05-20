import json
import requests
import pytest

post_url = 'http://dummy.restapiexample.com/api/v1/create'
get_url = 'http://dummy.restapiexample.com/api/v1/employees'
delete_url = 'http://dummy.restapiexample.com/api/v1/delete/'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"
                  "/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Content-Type": "application/json;charset=utf-8",
}


@pytest.fixture(scope='function')
def create_user(get_user_data):
    post_resp = requests.post(url=post_url, data=json.dumps(get_user_data), headers=headers)
    resp_data = post_resp.json()['data']
    user_id = resp_data['id']
    cookies = post_resp.cookies
    yield [resp_data, cookies]
    delete_user(user_id, cookies)


def get_all_employees(cookie=None):
    if cookie is None:
        response = requests.get(url=get_url, headers=headers)
    else:
        response = requests.get(url=get_url, headers=headers, cookies=cookie)
    employees = response.json()['data']
    return employees


def delete_user(user_id, Cookies):
    url = delete_url + str(user_id)
    response = requests.delete(url, headers=headers, cookies=Cookies)
    if response.json()["status"] == "success":
        print(f"Delete user id: {user_id} successfully")
        return True
    else:
        print(f"Delete user id: {user_id} Failed")
        return False


def check_user_by_id(user_id, Cookies):
    employees = get_all_employees(Cookies)
    is_found = False
    for employee in employees:
        if employee['id'] == user_id:
            print("PASS: new created user is found")
            is_found = True
            break
    return is_found


def test_check_new_user(create_user):
    response_list = create_user
    user_id = response_list[0]['id']
    cookies = response_list[1]
    assert check_user_by_id(user_id, cookies) is True



