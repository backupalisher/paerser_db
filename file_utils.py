import os
import csv


def load_file(file_name, encod):
    data = []
    with open(file_name, 'r', newline='', encoding=encod) as file:
        line_read = csv.reader(file, delimiter=';', lineterminator='\n')
        for row in line_read:
            data.append(row)
    return data


def save_process(data):
    t_data = data
    for d in t_data:
        fn = f'auto_save.csv'
        with open(fn, 'w',
                  encoding='utf-8') as file:
            add_data = csv.writer(file, delimiter=';', lineterminator='\n')
            add_data.writerow(d)
