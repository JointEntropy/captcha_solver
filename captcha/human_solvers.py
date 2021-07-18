from twocaptcha import TwoCaptcha
from twocaptcha import api
from captcha.solvers_base import BaseSolver
from captcha.exceptions import CaptchaSolutionError
from loguru import logger
# from PIL import Image


class HandSolver(BaseSolver):
    name = 'HANDSOLVER'

    def solve_by_path(self, x):
        try:
            logger.debug(f'Solve image by path:\n{x}')
            answer = input()
        except api.ApiException:
            raise CaptchaSolutionError
        return answer


class RuCaptchaHumanSolver(BaseSolver):
    """
    https://rucaptcha.com/enterpage
    """
    name = 'RUCAPTCHA'

    def __init__(self, params):
        self.params = params
        self.solver = TwoCaptcha(params['API_KEY'])

    def solve_by_path(self, x):
        try:
            result = self.solver.normal(x)
            logger.debug(f'Solved {result["code"]}. Remain balance {self.solver.balance()}.')
        except api.ApiException:
            raise CaptchaSolutionError
        return result['code']

    def balance(self):
        return self.solver.balance()


if __name__ == '__main__':
    import json
    with open('config.json', 'r') as f:
        config = json.loads(f)
    solver = RuCaptchaHumanSolver(config['captcha'])
    print(solver.solve_by_path('../demo.png'))
    print(solver.balance())
    # img = Image.open('solve_me.png')
    # solver.solve_image(img)