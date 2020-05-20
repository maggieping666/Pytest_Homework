import json
import pytest


def get_users():
    file = open("userlist.json", "r",  encoding='utf-8')
    user_list = json.load(file)
    return user_list


@pytest.fixture(scope='session', params=get_users())
def get_user_data(request):
    return request.param




