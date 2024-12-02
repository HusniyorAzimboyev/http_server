import os

import requests
import json


def check_get():

    response = requests.get("http://localhost:8001/data")

    print(response.status_code)
    print(response.json())

# check_get()
def check_post(i):
    new_item = {
        "name": f"User{i}",
        "email": f"user{i}@mail.ru"
    }

    response = requests.post(url="http://localhost:8000/data", data=json.dumps(new_item))

    print(response.status_code)


# check_post()

def check_put():
    new_item = {
        "name": "Azimboyev Husniyor",
        "email": "husniyor09@example.com"
    }

    response = requests.put("http://localhost:8000/data/7", data=json.dumps(new_item))

    print(response.status_code)


# check_put()


# ""
def check_delete(i):

    response = requests.delete(f"http://localhost:8000/data/{i}")

    print(response.status_code)
    # print(response.json())
# for i in [1,5,6,9,10,11]:
#     check_delete(i)
# check_get()
# for i in  range(5):
#     check_post(i=i)
# check_put()
# data = requests.get("http://localhost:8000/data").json()
# for i in data:
#     print(i)


def weather():
    import requests

    url = "https://weatherapi-com.p.rapidapi.com/current.json"

    querystring = {"q": "53.1,-0.13"}

    headers = {
        "x-rapidapi-key": "54048b746fmshda22903440ad421p1034c5jsn64cb525b2b1b",
        "x-rapidapi-host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())
weather()