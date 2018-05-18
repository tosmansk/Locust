import random
import json
from locust import HttpLocust, TaskSet, task
import argparse


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        random_suffix = random.randint(1, 10)
        test_user_name_prefix = 'test_user'
        self.user_first_name = test_user_name_prefix + '_first_name_' + str(random_suffix)
        self.user_last_name = test_user_name_prefix + '_last_name_' + str(random_suffix)
        self.add_person()

    def add_person(self):
        self.client.post('/dodajNazwisko', json={"FirstName":  self.user_first_name, "LastName": self.user_last_name})

    @task(1)
    def change_person(self):
        self.user_last_name = self.user_last_name + '_mod'
        self.client.put('/ZmienNazwisko2', json={"FirstName":  self.user_first_name, "LastName": self.user_last_name},
                        name='change_person')

    @task(4)
    def get_person(self):
        self.client.get('/{}'.format(self.user_first_name), name='get_person')
            # x = response.json()
            # assert x['name'] == self.user_last_name, \
            # if x['name'] != self.user_last_name:
            #     response.failure("{}['name'] should be equal to {}".format(x, self.user_last_name))

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 0
    max_wait = 0