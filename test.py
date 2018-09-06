import screenshot_detector
import os
import pandas as pd

# Test image from path
dir_path = 'images/test/'
lfile = os.listdir(dir_path)
input = [(i, dir_path + lfile[i], 'path') for i in range(len(lfile))]
screenshot_detector.detect(list_image=input, nprocess=4, output="output_path.tsv")

# Test image from link
input = []
df = pd.read_csv('input.csv',header=None)
for idx, row in df.iterrows():
    input.append((row[0], row[1], 'link'))
screenshot_detector.detect(list_image=input, nprocess=4, output="output_link.tsv")
