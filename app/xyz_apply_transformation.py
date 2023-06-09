import csv
import os

def xyz_apply_transformation(file, data_transform):
    tmpFile = file + '_modified'
    with open(file, 'r') as csvfile, open(tmpFile, 'w', newline='') as outFile:
        data = list(csv.reader(csvfile, delimiter=' '))
        writer = csv.writer(outFile, delimiter=' ')
        for row in data:
            if row[2] != 'nan':
                row[2] = data_transform(row[2])
                writer.writerow(row)
    os.remove(file)
    os.rename(tmpFile, file)
