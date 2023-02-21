import requests
from decouple import config


class WiseService:
    def __init__(self):
        self.main_url = "..."
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config('WISE_TOKEN')}"
        }
        self.profile_id = self._get_profile_id()

    def _get_profile_id(self):
        url = "https://api.sandbox.transferwise.tech/v1/profiles"
        response = requests.get(url, headers=self.headers)
        print(response.status_code)
        a = 5


if __name__ == '__main__':
    print('1')
