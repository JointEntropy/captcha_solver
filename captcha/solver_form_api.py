import urllib
import requests
import io
from PIL import Image
import json
from loguru import logger
from src.scrape_data.captcha.exceptions import CaptchaSolutionError


class CaptchaSolverForm:
    def __init__(self, response):
        self.response = response

    def fetch_img(self):
        captcha_data = self.response.json()
        captcha_img_path = captcha_data['captcha']['img-url']
        f = io.BytesIO(requests.get(captcha_img_path).content)
        img = Image.open(f)
        return img

    def solve(self, text):
        captcha_data = self.response.json()
        query_params = urllib.parse.urlparse(captcha_data['captcha']['captcha-page']).query
        data = dict([t.split('=') for t in query_params.split('&')])['retpath']
        solvecaptcha_dict = dict(
            key=captcha_data['captcha']['key'],
            retpath=urllib.parse.unquote(data),
            rep=text
        )
        params = list(solvecaptcha_dict.items())
        headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            #             'Referer': 'https://newssearch.yandex.ru/showcaptcha?retpath=https%3A//newssearch.yandex.ru/yandsearch%3Frpt%3Dnnews2%26nsrc%3D254129614%26showdups%3D1%26within%3D777%26from_day%3D1%26from_month%3D11%26from_year%3D2018%26to_day%3D16%26to_month%3D11%26to_year%3D2018%26p%3D1_fb9977928c593e69836df07d4c38608e&t=0/1602870557/1c7fcaf581ba966b848197e0bf97893e&s=2b3a11056dd622f54dad1ec605fa50e5',
            'Referer': self.response.url,
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        passcaptcha_url = 'https://newssearch.yandex.ru/checkcaptcha'
        response = requests.get(passcaptcha_url,
                                       headers=headers,
                                       params=params
        )
        if 'showcaptcha' in response.url:
            raise CaptchaSolutionError
        return response

    @staticmethod
    def is_captcha_response(response):
        try:
            response_type = json.loads(response.content).get('type', '')
            if response_type == 'captcha':
                return True
        except json.JSONDecodeError:
            pass
        return False
