import pandas as pd
import pandas as pd
import os
import numpy as np
import time
from PIL import Image
from scipy import signal
from scipy import misc

import urllib.request
from urllib.request import urlopen
from multiprocessing import Pool

def check_row(line):
    """
    Scan the elements on a row of image and check if they form a line.
    The return value is maximum length of line in th row.
    """
    max_length = 0
    cur_length = 0
    last_value = 0
    for v in line:
        if v > 0:
            if v == last_value:
                cur_length +=1
                if cur_length > max_length:
                    max_length = cur_length
            else:
                last_value = v
                cur_length = 1
    return max_length

def check_img (arr):
    """
    Scan all rows in the image and returns the number of row as a line.
    The row is a line if check_row value of the line = 1/3 length of the row.
    """
    res_index = []
    zeros = np.zeros(arr.shape)
    row_length = arr.shape[1]
    ones = np.ones(row_length)
    for idx, row in enumerate(arr):
        l = check_row(row)
        if 3*l > row_length:
            zeros[idx] = ones
            res_index.append(idx)
    return res_index

def horizontal_filter(tuple_input):
    index, path, type_file = tuple_input
    kernel = np.array([[-1,-1,-1],
                       [ 0, 0, 0],
                       [+1,+1,+1]])
    try:
        if type_file == 'link':
            with urlopen(path) as file:
                img = misc.imread(file, mode='L')
        elif type_file == 'path':
            img = misc.imread(path,mode='L')
        else:
            raise Exception('The type_file must be "link" or "path"')
        dst = signal.convolve2d(img, kernel, boundary='symm', mode='same')
        dst = np.absolute(dst)
        dst2 = np.interp(dst, (dst.min(), dst.max()), (0, 10)).astype(int)
        list_index = check_img(dst2)
        return (index, path, len(list_index))
    except Exception as e:
        print (e)
        pass
    return (index, path, 0)

def detect(list_image, nprocess=40, output="output.tsv"):
    """
    Compute the number of horizontal edge of each image.

    Apply kernel computing gradient of image.

    Parameters
    ----------
    list_image: list of tuple (index, image_path, type) with
                + index is index of the image.
                + image_path is path or url to the image we need to process.
                + type is type of image_path. The type must be "link" or "path".
    nprocess: int, default = 40
                Number of the processors.
    output: str, default = "output.tsv"
                Path to output file, defaul is output.tsv.
                The output file with 3 columns and seperate by a tab ('\t').
                The first column is index.
                The second column is image_path.
                The third column is number of horizontal line in this image.
    Examples
    --------
    >>> import screenshot_detector
    >>> input = [(1, 'images/test/img1.jpg', 'path'), (2, 'images/test/img2.png', 'path')]
    >>> screenshot_detector.detect(list_image=input, nprocess=4, output="output_path.tsv")
    >>>
    """
    p = Pool(nprocess)
    data = p.map(horizontal_filter, list_image)
    df = pd.DataFrame(data)
    df.to_csv(output, sep='\t', index=False)
