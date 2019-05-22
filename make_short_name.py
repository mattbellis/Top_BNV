import csv
import numpy as np

datasets = []

csvReader = csv.reader(open('Datasets.csv', newline=''), delimiter=' ', quotechar='|')
for row in csvReader:
    if len(row[0]) > 15:
        r = row[0].split('/')
        v = r[2].split('asymptotic_')
        short_name = r[1] + '_' + v[-1] 
        datasets.append([short_name,row[0][1:]])
