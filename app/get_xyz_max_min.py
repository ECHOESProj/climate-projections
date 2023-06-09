from app.utils.fs import get_files
import csv

def get_xyz_max_min(path):
    files = get_files(path + '/*')
    values = []

    for file in files:
        with open(file) as csvfile:
            data = list(csv.reader(csvfile, delimiter=' '))
            for row in data:
                if row[2] != 'nan':
                    values.append(float(row[2]))

    return min(values), max(values)
