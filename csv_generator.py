import csv
from datetime import datetime
import pandas as pd
from collections import Counter
import numpy as np



def elaborate_dataset(house):
    for path_file in house:
        if ('ADLs' in path_file) or ('Sensors' in path_file):
            check_and_generate_csv(path_file)

    house_name = house[0]
    path_adls = house[2]
    path_sens = house[3]


def check_and_generate_csv(path_file):
    # print ('check file >> %s.txt <<' % path_file)
    file_input = open(path_file+'.txt').readlines()
    ### to count lines in file
    for i, l in enumerate(file_input):
        pass
    tot_detection = i-1

    list_detection = []
    error = False
    iter_detection = iter(file_input)
    try:
        ### two times next() to jump first and second line in file (header of tables)
        next(iter_detection)
        next(iter_detection)
        next_line = next(iter_detection)
        init_error = False
    except StopIteration:
        init_error = True
    if not init_error:
        for c in range(tot_detection):
            smart_line = []
            this_line = next_line.split('\t')
            for col in this_line:
                if col and not col.isspace():
                    col = col.strip()
                    smart_line.append(col)
            start = datetime.strptime(smart_line[0], '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(smart_line[1], '%Y-%m-%d %H:%M:%S')
            try:
                next_line = next(iter_detection)
                next_empty = False
            except StopIteration:
                next_empty = True
    if not error:
        with open(path_file + '.txt', 'r') as in_file:
            stripped = (line.strip() for line in in_file)
            lines = (line.split("") for line in stripped if line)
            with open(path_file + '.csv', 'w') as out_file:
                writer = csv.writer(out_file)
                writer.writerows(lines)


def merge_dataset(dataset,sensors):
    state = pd.read_csv(dataset, sep="\t\t")
    sensor = pd.read_csv(sensors, sep="\t")
    print("usssch")


