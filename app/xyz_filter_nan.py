import csv
import os

def xyz_filter_nan(file):
    tmpFile = file + '_modified'
    with open(file, 'r') as csvfile, open(tmpFile, 'w', newline='') as outFile:
        data = list(csv.reader(csvfile, delimiter=' '))
        writer = csv.writer(outFile, delimiter=' ')
        for row in data:
            if row[2] != 'nan':
                writer.writerow(row)
    os.remove(file)
    os.rename(tmpFile, file)
