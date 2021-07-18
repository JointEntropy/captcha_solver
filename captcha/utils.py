from PIL import Image
import os
import numpy as np


def dump_pil_img(img, path='.'):
    name =  hash(np.array(img).data.tobytes())
    save_path = os.path.join(path, f'{name}.png')
    img.save(save_path)
    return save_path


if __name__ == '__main__':
    img = Image.open('solve_me.png')
    dump_pil_img(img)
