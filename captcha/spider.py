from loguru import logger
import json
import requests
import io
from PIL import Image
import urllib


class CaptchaSolverForm:
    def fetch_img(self, response):
        captcha_data = response.json()
        captcha_img_path = captcha_data['captcha']['img-url']
        f = io.BytesIO(requests.get(captcha_img_path).content)
        img = Image.open(f)
        return img

    def solve(self, response, text):
        captcha_data = response.json()
        query_params = urllib.parse.urlparse(captcha_data['captcha']['captcha-page']).query
        data = dict([t.split('=') for t in query_params.split('&')])['retpath']
        solvecaptcha_dict = dict(
            key=captcha_data['captcha']['key'],
            retpath=urllib.parse.unquote(data),
            rep=text
        )
        passcaptcha_url = 'https://newssearch.yandex.ru/checkcaptcha'
        params = list(solvecaptcha_dict.items())
        passcaptcha_url_with_args = passcaptcha_url + '?' +urllib.parse.urlencode(params)
        return dict(url=passcaptcha_url_with_args)

