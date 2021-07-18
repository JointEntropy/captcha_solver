from loguru import logger
from PIL import Image
import numpy as np
from captcha.utils import dump_pil_img
import os


class BaseSolver:
    name = 'BASE_SOLVER'

    def __init__(self, params):
        self.params = params

    def solve_image(self, x):
        logger.debug('')
        if isinstance(x, str):
            return self.solve_by_path(x)
        elif isinstance(x, Image.Image):
            image_pth = dump_pil_img(x)
            solution = self.solve_by_path(image_pth)
            os.remove(image_pth)
            return solution
        elif isinstance(x, np.array):
            raise NotImplementedError('Not implemented for numpy array.')
        else:
            raise ValueError('Unknown image type.')

    def solve_by_path(self, x):
        raise NotImplementedError