import json
import requests
from django.conf import settings
from algo360_constants import ALGO360_UPWARDS_MAPPING, CREDENTIALS_FILE


class Algo360(object):

    def __init__(self, algo360_user_id):
        self.credentials_file = CREDENTIALS_FILE
        self.algo360_user_id = algo360_user_id
        self.credentials = self.__get_credentials()

    def __set_credentials(self, credentials):
        self.credentials = credentials

    def __get_credentials(self):
        credentials = None
        with open(self.credentials_file) as credentials_file:
            credentials = json.load(credentials_file)
        return credentials

    def __update_credentials_json(self, credentials_dict):
        with open(self.credentials_file, 'w') as credentials_file:
            json.dump(credentials_dict, credentials_file)

    def __get_new_credentials(self):
        credentials_url = settings.ALGO360.get('credentials_url')
        post_data = {
            'client_id': settings.ALGO360.get('client_id'),
            'client_secret': settings.ALGO360.get('client_secret'),
            'grant_type': settings.ALGO360.get('grant_type', {}).get('refresh_token'),
            'refresh_token': self.credentials.get('refresh_token')
        }
        response = requests.post(credentials_url, post_data)
        credentials = {
            'access_token': None,
            'refresh_token': None
        }
        for credential_key in credentials:
            credentials[credential_key] = response.json().get(credential_key)
        return credentials

    def __fetch_user_data(self):
        data_url = settings.ALGO360.get('user_data_url').format(
            algo360_user_id=self.algo360_user_id)
        print data_url
        headers = {
            'Authorization': 'Bearer {access_token}'.format(access_token=self.credentials.get('access_token'))
        }
        response = requests.get(data_url, headers=headers)
        return response

    def get_user_data(self):
        user_data = {}
        user_data_response = self.__fetch_user_data()
        if user_data_response.status_code == 401:
            new_credentials = self.__get_new_credentials()
            self.__update_credentials_json(new_credentials)
            self.__set_credentials(new_credentials)
            user_data_response = self.__fetch_user_data()
        if user_data_response.status_code == 200:
            user_data = user_data_response.json().get(
                'result', {}).get('data')
        return user_data

    def get_model_data(self):
        model_data = {}
        user_data_list = self.get_user_data()
        for user_data in user_data_list:
            for data_key in ALGO360_UPWARDS_MAPPING.keys():
                if data_key in user_data:
                    model_data[ALGO360_UPWARDS_MAPPING[
                        data_key]] = user_data.get(data_key)
        return model_data